# Merigate Entry — API Documentation

## Overview

Merigate Entry is a Frappe-based application that receives invoice and gate entry data from the Merigate system and stores it in the ERP. Authentication is session-based — login once, and Frappe's `sid` cookie handles all subsequent requests automatically.

---

## Base URL

```
https://staging.microcrispr.com
```

---

## Authentication Flow

```
Step 1: Login → Frappe sets sid cookie automatically
Step 2: Send sid cookie with every subsequent request
```

---

## API Endpoints

---

### 1. Login

**Endpoint**

```
POST /api/method/merigate_entry.merigate_entry.api.merigate_api.login_user
```

**Headers**

```
Content-Type: application/json
```

**Request Body**

```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Success Response**

```json
{
  "message": {
    "status": "success",
    "message": "Login successful.",
    "user": "user@example.com",
    "full_name": "John Doe"
  }
}
```

> After a successful login, Frappe automatically sets a `sid` cookie in the response. This cookie must be included in all subsequent API calls.

**Error Responses**

_User not found_

```json
{
  "message": {
    "status": "error",
    "message": "User not found. Contact admin."
  }
}
```

_Invalid credentials_

```json
{
  "message": {
    "status": "error",
    "message": "Invalid credentials."
  }
}
```

_No role assigned_

```json
{
  "message": {
    "status": "error",
    "message": "Access not assigned. Contact admin."
  }
}
```

---

### 2. Create / Update Merigate Entry

**Endpoint**

```
POST /api/method/merigate_entry.merigate_entry.api.merigate_api.create_merigate_entry
```

**Headers**

```
Content-Type: application/json
Cookie: sid=<your_sid_from_login>
```

**Request Body (Example)**

```json
{
  "docname": "MG-TEST-002",
  "category": "General Purchase",
  "inward_location": "Meril Main Gate",
  "gate_no": "Gate 1",
  "scan_barcode": "BC001",
  "gate_entry_no": "GE-001",
  "gate_entry_date": "2026-04-11",
  "company": "Micro Life Science Pvt Ltd",
  "name_of_supplier": "Test Supplier",
  "supplier_gst": "27AABCU9603R1ZX",
  "supplier_address": "Mumbai, Maharashtra",
  "purchase_order_no": "PO-001",
  "purchase_order_date": "2026-04-01",
  "challan_invoice_no": "INV-001",
  "challan_invoice_date": "2026-04-05",
  "bill_of_entry_no": "BOE-001",
  "bill_of_entry_date": "2026-04-06",
  "material_description": "Test Material",
  "qty_as_per_inv_challan": "10",
  "eway_bill_no": "EWB-001",
  "eway_bill_date": "2026-04-05",
  "transport_courier": "DTDC",
  "lr_airway_bill_no": "LR-001",
  "lr_airway_bill_date": "2026-04-05",
  "vehicle_type": "Truck",
  "vehicle_no": "MH-01-AB-1234",
  "driver_name": "Ramesh Kumar",
  "driver_mobile_no": "9876543210",
  "invoice_value": 125000,
  "created_by_mg": "Balamurali Selvam",
  "created_date": "2026-04-11",
  "remark": "Test entry",
  "status": "Open"
}
```

**Success Response**

```json
{
  "message": {
    "status": "success",
    "docname": "MG-TEST-002",
    "message": "Merigate Entry saved successfully"
  }
}
```

**Error Responses**

_Not logged in_

```json
{
  "message": {
    "status": "error",
    "message": "Not logged in. Please login first."
  }
}
```

_Access denied_

```json
{
  "message": {
    "status": "error",
    "message": "Access denied. Contact admin."
  }
}
```

_Missing docname_

```json
{
  "message": {
    "status": "error",
    "message": "Merigate Doc Name is required"
  }
}
```

---

### 3. Logout

**Endpoint**

```
POST /api/method/merigate_entry.merigate_entry.api.merigate_api.logout_user
```

**Headers**

```
Cookie: sid=<your_sid>
```

**Success Response**

```json
{
  "message": {
    "status": "success",
    "message": "Logged out successfully."
  }
}
```

---

## How to Use the sid Cookie

### In Postman

1. Call `login_user` — Postman stores the `sid` cookie automatically
2. In subsequent requests go to **Headers** tab and add:
   ```
   Key:   Cookie
   Value: sid=<value from Cookies tab>
   ```

### In Code (Python example)

```python
import requests

session = requests.Session()

# Step 1: Login
session.post(
    "https://staging.microcrispr.com/api/method/merigate_entry.merigate_entry.api.merigate_api.login_user",
    json={"email": "user@example.com", "password": "yourpassword"}
)

# Step 2: Send data — session cookie is sent automatically
response = session.post(
    "https://staging.microcrispr.com/api/method/merigate_entry.merigate_entry.api.merigate_api.create_merigate_entry",
    json={"docname": "MG-TEST-001", "category": "General Purchase", ...}
)
```

---

## Request Fields Reference

| Field                  | Type     | Required | Description                     |
| ---------------------- | -------- | -------- | ------------------------------- |
| docname                | Data     | Yes      | Unique document name            |
| category               | Select   | Yes      | General Purchase / Non Business |
| company                | Data     | Yes      | Company name                    |
| inward_location        | Data     | No       | Inward location                 |
| gate_no                | Data     | No       | Gate number                     |
| scan_barcode           | Data     | No       | Barcode                         |
| gate_entry_no          | Data     | No       | Entry number                    |
| gate_entry_date        | Date     | No       | YYYY-MM-DD                      |
| name_of_supplier       | Data     | No       | Supplier name                   |
| supplier_gst           | Data     | No       | GST number                      |
| supplier_address       | Data     | No       | Supplier address                |
| purchase_order_no      | Data     | No       | PO number                       |
| purchase_order_date    | Date     | No       | YYYY-MM-DD                      |
| challan_invoice_no     | Data     | No       | Invoice number                  |
| challan_invoice_date   | Date     | No       | YYYY-MM-DD                      |
| bill_of_entry_no       | Data     | No       | BOE number                      |
| bill_of_entry_date     | Date     | No       | YYYY-MM-DD                      |
| material_description   | Text     | No       | Material details                |
| qty_as_per_inv_challan | Data     | No       | Quantity                        |
| eway_bill_no           | Data     | No       | E-way bill                      |
| eway_bill_date         | Date     | No       | YYYY-MM-DD                      |
| transport_courier      | Data     | No       | Transport name                  |
| lr_airway_bill_no      | Data     | No       | LR/AWB number                   |
| lr_airway_bill_date    | Date     | No       | YYYY-MM-DD                      |
| vehicle_type           | Data     | No       | Vehicle type                    |
| vehicle_no             | Data     | No       | Vehicle number                  |
| driver_name            | Data     | No       | Driver name                     |
| driver_mobile_no       | Data     | No       | Mobile number                   |
| invoice_value          | Currency | No       | Amount                          |
| created_by_mg          | Data     | No       | Created by                      |
| created_date           | Date     | No       | YYYY-MM-DD                      |
| remark                 | Text     | No       | Remarks                         |
| status                 | Select   | No       | Open / Closed / Cancelled       |
| file_url               | Data     | No       | File URL                        |

---

## User Flow

```
Login (email + password)
  → Frappe authenticates → sets sid cookie
  → Send data with sid cookie
  → Server validates session → checks role → saves entry
```

---

## Role Setup

Admin must assign the role manually in ERP:

```
ERP → Users → [Select User] → Roles → Add "Merigate Entry User"
```

Without this role:

- Login will return "Access not assigned"
- Data cannot be saved

---

## App Information

| Field        | Value                           |
| ------------ | ------------------------------- |
| App Name     | merigate_entry                  |
| Publisher    | Shivam Singh                    |
| Email        | shivam.singh@microcrispr.com    |
| License      | MIT                             |
| ERP Base URL | https://staging.microcrispr.com |

---

## Summary

- Session-based authentication using Frappe's native `sid` cookie
- No token generation or management required
- Role-based access control via `Merigate Entry User` role
- Supports both create and update of Merigate Entry documents



Login (email + password)
  → Input validation (email + password required)
  → User existence check
  → Frappe authenticates → sets sid cookie
  → Role check (Merigate Entry User / System Manager)
  → If role missing → auto logout → return error
  → Send data with sid cookie
  → Server validates session → checks role → saves entry
  → Logout → clears session