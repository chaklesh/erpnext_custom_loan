"""
Installation and setup functions for NAYAG EDGE Loan Management App
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_install():
    """Setup function called after app installation"""
    setup_custom_role()
    create_interest_settings()
    setup_default_data()
    print("✅ NAYAG EDGE Loan Management App installed successfully!")

def setup_custom_role():
    """Create Loan Manager role if it doesn't exist"""
    if not frappe.db.exists("Role", "Loan Manager"):
        role_doc = frappe.get_doc({
            "doctype": "Role",
            "role_name": "Loan Manager",
            "desk_access": 1,
            "search_bar": 1
        })
        role_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print("✅ Created Loan Manager role")

def create_interest_settings():
    """Create default interest settings"""
    if not frappe.db.exists("Interest Setting", "Default"):
        interest_setting = frappe.get_doc({
            "doctype": "Interest Setting",
            "name": "Default",
            "setting_name": "Default Interest Rates",
            "is_active": 1,
            "interest_rate_slabs": [
                {
                    "min_amount": 0,
                    "max_amount": 50000,
                    "interest_rate": 3.0,
                    "loan_type": "Flat Rate"
                },
                {
                    "min_amount": 50001,
                    "max_amount": 100000,
                    "interest_rate": 2.5,
                    "loan_type": "Flat Rate"
                },
                {
                    "min_amount": 0,
                    "max_amount": 50000,
                    "interest_rate": 2.0,
                    "loan_type": "EMI"
                },
                {
                    "min_amount": 50001,
                    "max_amount": 100000,
                    "interest_rate": 1.8,
                    "loan_type": "EMI"
                }
            ]
        })
        interest_setting.insert(ignore_permissions=True)
        frappe.db.commit()
        print("✅ Created default interest settings")

def setup_default_data():
    """Setup any other default data required"""
    # Add default workspace if not exists
    if not frappe.db.exists("Workspace", "Loan Management"):
        workspace = frappe.get_doc({
            "doctype": "Workspace",
            "name": "Loan Management",
            "title": "NAYAG EDGE - Loan Management",
            "icon": "loan",
            "module": "Custom Loan",
            "public": 1
        })
        workspace.insert(ignore_permissions=True)
        frappe.db.commit()
        print("✅ Created Loan Management workspace")

def before_uninstall():
    """Cleanup function called before app uninstallation"""
    print("🔄 Cleaning up NAYAG EDGE Loan Management data...")
    
def after_uninstall():
    """Final cleanup after app uninstallation"""
    print("✅ NAYAG EDGE Loan Management App uninstalled successfully!")