"""
Utility functions for loan calculations and management
"""

import frappe
from frappe.utils import flt, cint, add_months, get_datetime
import math
from datetime import datetime, date


def calculate_flat_interest(principal, rate_per_month, tenure_months):
    """
    Calculate flat interest loan details
    
    Args:
        principal (float): Principal loan amount
        rate_per_month (float): Interest rate per month (as percentage)
        tenure_months (int): Loan tenure in months
    
    Returns:
        dict: Loan calculation details
    """
    rate = flt(rate_per_month) / 100
    principal = flt(principal)
    tenure = cint(tenure_months)
    
    total_interest = principal * rate * tenure
    total_amount = principal + total_interest
    monthly_payment = total_amount / tenure
    
    return {
        "principal": principal,
        "total_interest": total_interest,
        "total_amount": total_amount,
        "monthly_payment": monthly_payment,
        "interest_per_month": principal * rate
    }


def calculate_emi(principal, rate_per_month, tenure_months):
    """
    Calculate EMI using reducing balance method
    
    Args:
        principal (float): Principal loan amount
        rate_per_month (float): Interest rate per month (as percentage)
        tenure_months (int): Loan tenure in months
    
    Returns:
        dict: EMI calculation details
    """
    rate = flt(rate_per_month) / 100
    principal = flt(principal)
    tenure = cint(tenure_months)
    
    if rate == 0:
        emi = principal / tenure
        total_amount = principal
        total_interest = 0
    else:
        emi = (principal * rate * math.pow(1 + rate, tenure)) / (math.pow(1 + rate, tenure) - 1)
        total_amount = emi * tenure
        total_interest = total_amount - principal
    
    return {
        "principal": principal,
        "emi": emi,
        "total_amount": total_amount,
        "total_interest": total_interest,
        "interest_rate": rate_per_month
    }


def generate_payment_schedule(loan_type, principal, rate_per_month, tenure_months, start_date):
    """
    Generate payment schedule for a loan
    
    Args:
        loan_type (str): "Flat Rate" or "EMI"
        principal (float): Principal amount
        rate_per_month (float): Interest rate per month
        tenure_months (int): Tenure in months
        start_date (date): Loan start date
    
    Returns:
        list: Payment schedule
    """
    schedule = []
    
    if loan_type == "Flat Rate":
        calc = calculate_flat_interest(principal, rate_per_month, tenure_months)
        monthly_payment = calc["monthly_payment"]
        monthly_principal = principal / tenure_months
        monthly_interest = calc["interest_per_month"]
        
        for month in range(1, tenure_months + 1):
            due_date = add_months(start_date, month)
            schedule.append({
                "installment_number": month,
                "due_date": due_date,
                "installment_amount": monthly_payment,
                "principal_amount": monthly_principal,
                "interest_amount": monthly_interest,
                "remaining_balance": principal - (monthly_principal * month)
            })
    
    elif loan_type == "EMI":
        calc = calculate_emi(principal, rate_per_month, tenure_months)
        emi = calc["emi"]
        remaining_principal = principal
        rate = flt(rate_per_month) / 100
        
        for month in range(1, tenure_months + 1):
            due_date = add_months(start_date, month)
            interest_amount = remaining_principal * rate
            principal_amount = emi - interest_amount
            
            if principal_amount > remaining_principal:
                principal_amount = remaining_principal
                emi_adjusted = principal_amount + interest_amount
            else:
                emi_adjusted = emi
            
            remaining_principal -= principal_amount
            
            schedule.append({
                "installment_number": month,
                "due_date": due_date,
                "installment_amount": emi_adjusted,
                "principal_amount": principal_amount,
                "interest_amount": interest_amount,
                "remaining_balance": max(0, remaining_principal)
            })
    
    return schedule


def get_overdue_loans():
    """Get all overdue loans"""
    today = frappe.utils.today()
    
    return frappe.db.sql("""
        SELECT DISTINCT l.name, l.customer, l.customer_name, l.loan_amount, 
               l.outstanding_amount, l.mobile_number,
               COUNT(lrs.name) as overdue_installments,
               SUM(lrs.installment_amount) as overdue_amount,
               MIN(lrs.due_date) as first_overdue_date
        FROM `tabLoan` l
        INNER JOIN `tabLoan Repayment Schedule` lrs ON lrs.parent = l.name
        WHERE l.status = 'Active' 
        AND lrs.status = 'Pending' 
        AND lrs.due_date < %s
        GROUP BY l.name
        ORDER BY first_overdue_date ASC
    """, (today,), as_dict=True)


def calculate_penalty(overdue_amount, overdue_days, penalty_rate_per_month=1):
    """
    Calculate penalty for overdue payments
    
    Args:
        overdue_amount (float): Overdue amount
        overdue_days (int): Number of overdue days
        penalty_rate_per_month (float): Penalty rate per month (as percentage)
    
    Returns:
        float: Penalty amount
    """
    if overdue_days <= 0:
        return 0
    
    penalty_rate = flt(penalty_rate_per_month) / 100
    penalty = overdue_amount * penalty_rate * (overdue_days / 30)  # Pro-rated for days
    
    return penalty


def get_customer_loan_summary(customer):
    """Get comprehensive loan summary for a customer"""
    customer_doc = frappe.get_doc("Loan Customer", customer)
    
    # Get all loans
    loans = frappe.get_all("Loan",
                          filters={"customer": customer},
                          fields=["name", "loan_amount", "outstanding_amount", "status", 
                                 "loan_date", "loan_type", "interest_rate"])
    
    # Get recent payments
    payments = frappe.get_all("Loan Payment",
                             filters={"customer": customer, "docstatus": 1},
                             fields=["name", "payment_date", "amount", "loan"],
                             order_by="payment_date desc",
                             limit=10)
    
    # Calculate totals
    total_borrowed = sum(loan.loan_amount for loan in loans)
    total_outstanding = sum(loan.outstanding_amount for loan in loans if loan.status != "Closed")
    active_loans = len([loan for loan in loans if loan.status == "Active"])
    
    return {
        "customer_details": customer_doc.as_dict(),
        "loans": loans,
        "recent_payments": payments,
        "summary": {
            "total_borrowed": total_borrowed,
            "total_outstanding": total_outstanding,
            "active_loans": active_loans,
            "closed_loans": len([loan for loan in loans if loan.status == "Closed"])
        }
    }


@frappe.whitelist()
def get_loan_calculator_data(loan_type, principal, rate_per_month, tenure_months):
    """API endpoint for loan calculator"""
    if loan_type == "Flat Rate":
        return calculate_flat_interest(principal, rate_per_month, tenure_months)
    elif loan_type == "EMI":
        return calculate_emi(principal, rate_per_month, tenure_months)
    else:
        frappe.throw("Invalid loan type")


@frappe.whitelist()
def bulk_sms_reminder():
    """Send SMS reminders to customers with overdue payments"""
    overdue_loans = get_overdue_loans()
    sent_count = 0
    
    for loan in overdue_loans:
        try:
            message = f"Dear {loan.customer_name}, your loan payment of Rs.{loan.overdue_amount} is overdue. Please pay immediately. Contact us for details."
            
            # This would integrate with your SMS service
            # For now, just log the message
            frappe.log_error(f"SMS to {loan.mobile_number}: {message}", "SMS Reminder")
            sent_count += 1
            
        except Exception as e:
            frappe.log_error(f"Failed to send SMS to {loan.customer_name}: {str(e)}", "SMS Error")
    
    return {"sent": sent_count, "total": len(overdue_loans)}
