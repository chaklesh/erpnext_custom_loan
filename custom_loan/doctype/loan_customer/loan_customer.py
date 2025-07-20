# Copyright (c) 2025, Chaklesh Yadav - NAYAG and contributors
# For license information, please see license.txt
# NAYAG EDGE - Loan Management System

import frappe
from frappe.model.document import Document


class LoanCustomer(Document):
	def validate(self):
		self.validate_mobile_number()
		self.set_full_name()
	
	def validate_mobile_number(self):
		"""Validate mobile number format and check for duplicates"""
		if self.mobile_number:
			# Remove spaces and special characters
			mobile = self.mobile_number.replace(" ", "").replace("-", "").replace("+", "")
			
			# Check if it's a valid 10-digit mobile number
			if not mobile.isdigit() or len(mobile) != 10:
				frappe.throw("Please enter a valid 10-digit mobile number")
			
			# Check for duplicate mobile numbers
			existing = frappe.db.get_value("Loan Customer", 
											{"mobile_number": self.mobile_number, "name": ["!=", self.name]}, 
											"name")
			if existing:
				frappe.throw(f"Mobile number {self.mobile_number} already exists for customer {existing}")
	
	def set_full_name(self):
		"""Set full name if not provided"""
		if not self.customer_name:
			self.customer_name = f"Customer-{self.mobile_number}"
	
	def get_active_loans(self):
		"""Get all active loans for this customer"""
		return frappe.get_all("Loan", 
							  filters={"customer": self.name, "status": ["in", ["Active", "Approved"]]},
							  fields=["name", "loan_amount", "outstanding_amount", "interest_rate", "status"])
	
	def get_total_outstanding(self):
		"""Get total outstanding amount across all loans"""
		result = frappe.db.sql("""
			SELECT SUM(outstanding_amount) as total_outstanding
			FROM `tabLoan`
			WHERE customer = %s AND status IN ('Active', 'Approved')
		""", (self.name,), as_dict=True)
		
		return result[0].total_outstanding if result and result[0].total_outstanding else 0
	
	def get_payment_history(self, limit=10):
		"""Get recent payment history for this customer"""
		return frappe.get_all("Loan Payment",
							  filters={"customer": self.name},
							  fields=["name", "payment_date", "amount", "loan", "payment_type"],
							  order_by="payment_date desc",
							  limit=limit)


@frappe.whitelist()
def get_customer_summary(customer):
	"""Get customer summary including loans and payments"""
	doc = frappe.get_doc("Loan Customer", customer)
	
	return {
		"customer_details": doc.as_dict(),
		"active_loans": doc.get_active_loans(),
		"total_outstanding": doc.get_total_outstanding(),
		"recent_payments": doc.get_payment_history()
	}
