import frappe

# ─────────────────────────────────────────────
# Global Config
# ─────────────────────────────────────────────
ERP_BASE_URL = "https://staging.microcrispr.com"
ALLOWED_ROLES = ["Merigate Entry User", "System Manager"]


# ─────────────────────────────────────────────
# Helper: Role Check
# ─────────────────────────────────────────────
def has_merigate_access(user_email):
    roles = frappe.get_roles(user_email)
    return any(role in roles for role in ALLOWED_ROLES)


# ─────────────────────────────────────────────
# 1. Login
# ─────────────────────────────────────────────
@frappe.whitelist(allow_guest=True)
def login_user(email, password):
    try:
        # Input validation
        if not email or not password:
            return {"status": "error", "message": "Email and password are required."}

        # User existence check
        if not frappe.db.exists("User", email):
            return {"status": "error", "message": "User not found. Contact admin."}

        # Authenticate
        from frappe.auth import LoginManager
        try:
            lm = LoginManager()
            lm.authenticate(user=email, pwd=password)
            lm.post_login()
            frappe.db.commit()
        except Exception:
            return {"status": "error", "message": "Invalid credentials."}

        # Role check after login
        if not has_merigate_access(email):
            frappe.local.login_manager.logout()
            frappe.db.commit()
            return {"status": "error", "message": "Access not assigned. Contact admin."}

        # Remove Frappe default response fields
        frappe.response.pop("home_page", None)
        frappe.response.pop("full_name", None)

        return {
            "status": "success",
            "message": "Login successful.",
            "user": email,
            "full_name": frappe.db.get_value("User", email, "full_name")
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "login_user Error")
        return {"status": "error", "message": str(e)}


# ─────────────────────────────────────────────
# 2. Create / Update Merigate Entry
# ─────────────────────────────────────────────
@frappe.whitelist(allow_guest=True)
def create_merigate_entry(**kwargs):
    SKIP_FIELDS = {"name", "doctype", "owner", "creation", "modified"}

    # Session check
    if frappe.session.user == "Guest":
        return {"status": "error", "message": "Not logged in. Please login first."}

    # Role check
    if not has_merigate_access(frappe.session.user):
        return {"status": "error", "message": "Access denied. Contact admin."}

    # Input validation — before try block so frappe.throw works properly
    docname = kwargs.get("docname")
    if not docname:
        return {"status": "error", "message": "Merigate Doc Name is required."}

    try:
        # Create or update doc
        if frappe.db.exists("Merigate Entry", {"docname": docname}):
            doc = frappe.get_doc("Merigate Entry", {"docname": docname})
        else:
            doc = frappe.new_doc("Merigate Entry")
            doc.docname = docname

        # Map fields
        for key, value in kwargs.items():
            if key not in SKIP_FIELDS and hasattr(doc, key):
                setattr(doc, key, value)

        # Defaults
        if not doc.category:
            doc.category = "General Purchase"

        if not doc.status:
            doc.status = "Open"

        doc.save(ignore_permissions=True)
        frappe.db.commit()

        return {
            "status": "success",
            "docname": doc.docname,
            "message": "Merigate Entry saved successfully."
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "create_merigate_entry Error")
        return {"status": "error", "message": str(e)}


# ─────────────────────────────────────────────
# 3. Logout
# ─────────────────────────────────────────────
@frappe.whitelist(allow_guest=True)
def logout_user():
    try:
        # Check if session is already expired
        if frappe.session.user == "Guest":
            return {"status": "error", "message": "No active session to logout."}

        frappe.local.login_manager.logout()
        frappe.db.commit()
        return {"status": "success", "message": "Logged out successfully."}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "logout_user Error")
        return {"status": "error", "message": "Logout failed. Session may already be expired."}