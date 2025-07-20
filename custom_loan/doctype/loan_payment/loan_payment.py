# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class LoanPayment(Document):
	def validate(self):
		self.validate_amount()
		self.set_balance_amounts()
		self.allocate_payment()
	
	def on_submit(self):
		self.update_loan_balance()
		self.update_repayment_schedule()
	
	def validate_amount(self):
		"""Validate payment amount"""
		if self.amount <= 0:
			frappe.throw("Payment amount must be greater than 0")
		
		# Get loan outstanding amount
		loan = frappe.get_doc("Loan", self.loan)
		if self.amount > loan.outstanding_amount:
			if self.payment_type not in ["Prepayment", "Adjustment"]:
				frappe.throw(f"Payment amount cannot exceed outstanding amount of {loan.outstanding_amount}")
	
	def set_balance_amounts(self):
		"""Set balance before and after payment"""
		loan = frappe.get_doc("Loan", self.loan)
		self.balance_before_payment = loan.outstanding_amount
		self.balance_after_payment = max(0, self.balance_before_payment - self.amount)
	
	def allocate_payment(self):
		"""Allocate payment to principal, interest, and penalty"""
		if not (self.principal_paid or self.interest_paid or self.penalty_paid):
			# Auto-allocate payment
			loan = frappe.get_doc("Loan", self.loan)
			remaining_amount = flt(self.amount)
			
			# First pay penalty if any
			penalty_due = self.get_penalty_due()
			if penalty_due > 0:
				self.penalty_paid = min(penalty_due, remaining_amount)
				remaining_amount -= self.penalty_paid
			
			# Then pay interest
			interest_due = self.get_interest_due()
			if interest_due > 0 and remaining_amount > 0:
				self.interest_paid = min(interest_due, remaining_amount)
				remaining_amount -= self.interest_paid
			
			# Finally pay principal
			if remaining_amount > 0:
				self.principal_paid = remaining_amount
	
	def get_penalty_due(self):
		"""Calculate penalty due for overdue payments"""
		# Get overdue installments and calculate penalty
		loan = frappe.get_doc("Loan", self.loan)
		overdue_amount = loan.get_overdue_amount()
		
		# Simple penalty calculation - 1% of overdue amount per month
		if overdue_amount > 0:
			# This is a simplified penalty calculation
			return overdue_amount * 0.01
		
		return 0
	
	def get_interest_due(self):
		"""Get outstanding interest amount"""
		loan = frappe.get_doc("Loan", self.loan)
		
		# Calculate based on repayment schedule
		interest_due = 0
		for schedule in loan.repayment_schedule:
			if schedule.status in ["Pending", "Partial"]:
				interest_due += schedule.interest_amount - (schedule.paid_amount or 0)
		
		return interest_due
	
	def update_loan_balance(self):
		"""Update loan outstanding amount"""
		loan = frappe.get_doc("Loan", self.loan)
		loan.paid_amount = (loan.paid_amount or 0) + self.amount
		loan.outstanding_amount = loan.total_amount - loan.paid_amount
		loan.last_payment_date = self.payment_date
		
		# Update status
		if loan.outstanding_amount <= 0:
			loan.status = "Closed"
		elif loan.is_overdue():
			loan.status = "Overdue"
		else:
			loan.status = "Active"
		
		loan.save()
	
	def update_repayment_schedule(self):
		"""Update repayment schedule with payment allocation"""
		loan = frappe.get_doc("Loan", self.loan)
		remaining_payment = flt(self.amount)
		
		# Update schedule starting from oldest pending installment
		for schedule in loan.repayment_schedule:
			if schedule.status in ["Pending", "Partial"] and remaining_payment > 0:
				outstanding_for_installment = schedule.installment_amount - (schedule.paid_amount or 0)
				
				if remaining_payment >= outstanding_for_installment:
					# Full payment for this installment
					schedule.paid_amount = schedule.installment_amount
					schedule.paid_date = self.payment_date
					schedule.status = "Paid"
					remaining_payment -= outstanding_for_installment
				else:
					# Partial payment
					schedule.paid_amount = (schedule.paid_amount or 0) + remaining_payment
					schedule.status = "Partial"
					remaining_payment = 0
		
		loan.save()


@frappe.whitelist()
def create_payment(loan, amount, payment_date=None, payment_type="Regular Payment"):
	"""Create a loan payment"""
	payment = frappe.get_doc({
		"doctype": "Loan Payment",
		"loan": loan,
		"amount": amount,
		"payment_date": payment_date or frappe.utils.today(),
		"payment_type": payment_type
	})
	
	payment.insert()
	return payment.name


@frappe.whitelist()
def get_payment_suggestion(loan):
	"""Get suggested payment amount for next installment"""
	loan_doc = frappe.get_doc("Loan", loan)
	
	# Find next pending installment
	for schedule in loan_doc.repayment_schedule:
		if schedule.status == "Pending":
			return {
				"suggested_amount": schedule.installment_amount,
				"due_date": schedule.due_date,
				"installment_number": schedule.installment_number
			}
	
	return {"suggested_amount": loan_doc.outstanding_amount}
