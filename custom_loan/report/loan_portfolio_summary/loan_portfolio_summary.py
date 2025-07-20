# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt, cint


def execute(filters=None):
    columns, data = [], []
    
    columns = get_columns()
    data = get_data(filters)
    
    return columns, data


def get_columns():
    return [
        {
            "label": "Loan ID",
            "fieldname": "loan_id",
            "fieldtype": "Link",
            "options": "Loan",
            "width": 120
        },
        {
            "label": "Customer",
            "fieldname": "customer_name",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Mobile",
            "fieldname": "mobile_number",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Loan Type",
            "fieldname": "loan_type",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": "Loan Date",
            "fieldname": "loan_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": "Principal",
            "fieldname": "loan_amount",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": "Interest Rate",
            "fieldname": "interest_rate",
            "fieldtype": "Percent",
            "width": 100
        },
        {
            "label": "Total Amount",
            "fieldname": "total_amount",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": "Paid Amount",
            "fieldname": "paid_amount",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": "Outstanding",
            "fieldname": "outstanding_amount",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": "Status",
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": "Last Payment",
            "fieldname": "last_payment_date",
            "fieldtype": "Date",
            "width": 120
        }
    ]


def get_data(filters):
    conditions = get_conditions(filters)
    
    data = frappe.db.sql(f"""
        SELECT 
            name as loan_id,
            customer_name,
            mobile_number,
            loan_type,
            loan_date,
            loan_amount,
            interest_rate,
            total_amount,
            paid_amount,
            outstanding_amount,
            status,
            last_payment_date
        FROM `tabLoan`
        WHERE 1=1 {conditions}
        ORDER BY loan_date DESC
    """, filters, as_dict=1)
    
    return data


def get_conditions(filters):
    conditions = ""
    
    if filters.get("customer"):
        conditions += " AND customer = %(customer)s"
    
    if filters.get("status"):
        conditions += " AND status = %(status)s"
    
    if filters.get("loan_type"):
        conditions += " AND loan_type = %(loan_type)s"
    
    if filters.get("from_date"):
        conditions += " AND loan_date >= %(from_date)s"
    
    if filters.get("to_date"):
        conditions += " AND loan_date <= %(to_date)s"
    
    return conditions
