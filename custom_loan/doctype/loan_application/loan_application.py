# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime


class LoanApplication(Document):
	def validate(self):
		self.validate_amounts()
		self.set_interest_rate()
		self.validate_status_changes()
	
	def validate_amounts(self):
		"""Validate loan amounts"""
		if self.requested_amount <= 0:
			frappe.throw("Requested amount must be greater than 0")
		
		if self.approved_amount and self.approved_amount <= 0:
			frappe.throw("Approved amount must be greater than 0")
	
	def set_interest_rate(self):
		"""Set interest rate based on selected setting"""
		if self.interest_setting and not self.interest_rate:
			setting = frappe.get_doc("Interest Setting", self.interest_setting)
			self.interest_rate = setting.get_applicable_rate(self.requested_amount)
	
	def validate_status_changes(self):
		"""Validate status changes and set required fields"""
		if self.status == "Approved":
			if not self.approved_amount:
				self.approved_amount = self.requested_amount
			if not self.approved_rate:
				self.approved_rate = self.interest_rate
			if not self.approved_by:
				self.approved_by = frappe.session.user
			if not self.approval_date:
				self.approval_date = datetime.now()
		
		elif self.status == "Rejected" and not self.rejection_reason:
			frappe.throw("Rejection reason is required when rejecting application")
	
	def create_loan(self):
		"""Create loan document from approved application"""
		if self.status != "Approved":
			frappe.throw("Only approved applications can be converted to loans")
		
		# Check if loan already exists
		existing_loan = frappe.db.get_value("Loan", {"loan_application": self.name}, "name")
		if existing_loan:
			frappe.throw(f"Loan {existing_loan} already exists for this application")
		
		# Create new loan
		loan = frappe.get_doc({
			"doctype": "Loan",
			"loan_application": self.name,
			"customer": self.customer,
			"loan_type": self.loan_type,
			"loan_amount": self.approved_amount,
			"interest_rate": self.approved_rate,
			"tenure_months": self.tenure_months,
			"purpose": self.purpose,
			"status": "Active"
		})
		
		loan.insert()
		
		# Update application status
		self.status = "Disbursed"
		self.save()
		
		return loan.name


@frappe.whitelist()
def approve_application(application_name, approved_amount=None, approved_rate=None):
	"""Approve loan application"""
	doc = frappe.get_doc("Loan Application", application_name)
	
	doc.status = "Approved"
	if approved_amount:
		doc.approved_amount = approved_amount
	if approved_rate:
		doc.approved_rate = approved_rate
	
	doc.save()
	
	return doc.name


@frappe.whitelist()
def reject_application(application_name, rejection_reason):
	"""Reject loan application"""
	doc = frappe.get_doc("Loan Application", application_name)
	
	doc.status = "Rejected"
	doc.rejection_reason = rejection_reason
	
	doc.save()
	
	return doc.name


@frappe.whitelist()
def convert_to_loan(application_name):
	"""Convert approved application to loan"""
	doc = frappe.get_doc("Loan Application", application_name)
	return doc.create_loan()
