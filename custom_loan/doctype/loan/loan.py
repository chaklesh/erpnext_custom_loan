# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_months, flt, cint
import math
from datetime import datetime, timedelta


class Loan(Document):
	def validate(self):
		self.validate_amounts()
		self.calculate_loan_amounts()
		self.update_outstanding_amount()
	
	def on_submit(self):
		self.generate_repayment_schedule()
		self.status = "Active"
		self.save()
	
	def validate_amounts(self):
		"""Validate loan amounts"""
		if self.loan_amount <= 0:
			frappe.throw("Loan amount must be greater than 0")
		
		if self.interest_rate <= 0:
			frappe.throw("Interest rate must be greater than 0")
		
		if self.tenure_months <= 0:
			frappe.throw("Tenure must be greater than 0")
	
	def calculate_loan_amounts(self):
		"""Calculate total interest, total amount, and EMI"""
		principal = flt(self.loan_amount)
		rate = flt(self.interest_rate) / 100
		tenure = cint(self.tenure_months)
		
		if self.loan_type == "Flat Rate":
			# Flat interest calculation
			self.total_interest = principal * rate * tenure
			self.total_amount = principal + self.total_interest
			self.emi_amount = self.total_amount / tenure
		
		elif self.loan_type == "EMI":
			# EMI calculation using reducing balance
			monthly_rate = rate / 12 if self.payment_frequency == "Monthly" else rate
			
			if monthly_rate == 0:
				self.emi_amount = principal / tenure
				self.total_interest = 0
			else:
				self.emi_amount = (principal * monthly_rate * math.pow(1 + monthly_rate, tenure)) / \
								  (math.pow(1 + monthly_rate, tenure) - 1)
			
			self.total_amount = self.emi_amount * tenure
			self.total_interest = self.total_amount - principal
		
		# Set outstanding amount if not set
		if not self.outstanding_amount:
			self.outstanding_amount = self.total_amount
	
	def update_outstanding_amount(self):
		"""Update outstanding amount based on payments"""
		if self.name:
			paid_amount = frappe.db.sql("""
				SELECT COALESCE(SUM(amount), 0) as total_paid
				FROM `tabLoan Payment`
				WHERE loan = %s AND docstatus = 1
			""", (self.name,), as_dict=True)[0].total_paid
			
			self.paid_amount = paid_amount
			self.outstanding_amount = self.total_amount - paid_amount
			
			# Update status based on outstanding amount
			if self.outstanding_amount <= 0:
				self.status = "Closed"
			elif self.is_overdue():
				self.status = "Overdue"
			else:
				self.status = "Active"
	
	def generate_repayment_schedule(self):
		"""Generate repayment schedule based on loan type"""
		self.repayment_schedule = []
		
		start_date = self.loan_date
		principal = flt(self.loan_amount)
		remaining_principal = principal
		
		for month in range(1, self.tenure_months + 1):
			due_date = add_months(start_date, month)
			
			if self.loan_type == "Flat Rate":
				# Flat rate - same amount each month
				installment_amount = flt(self.total_amount / self.tenure_months)
				principal_amount = flt(self.loan_amount / self.tenure_months)
				interest_amount = installment_amount - principal_amount
			
			elif self.loan_type == "EMI":
				# EMI - reducing balance
				installment_amount = flt(self.emi_amount)
				interest_amount = remaining_principal * (flt(self.interest_rate) / 100)
				principal_amount = installment_amount - interest_amount
				
				if principal_amount > remaining_principal:
					principal_amount = remaining_principal
					installment_amount = principal_amount + interest_amount
			
			remaining_principal -= principal_amount
			
			schedule_row = {
				"installment_number": month,
				"due_date": due_date,
				"installment_amount": installment_amount,
				"principal_amount": principal_amount,
				"interest_amount": interest_amount,
				"remaining_balance": max(0, remaining_principal),
				"status": "Pending"
			}
			
			self.append("repayment_schedule", schedule_row)
	
	def is_overdue(self):
		"""Check if loan has overdue payments"""
		if not self.repayment_schedule:
			return False
		
		today = datetime.now().date()
		
		for schedule in self.repayment_schedule:
			if schedule.status == "Pending" and schedule.due_date < today:
				return True
		
		return False
	
	def get_next_due_date(self):
		"""Get next payment due date"""
		if not self.repayment_schedule:
			return None
		
		for schedule in self.repayment_schedule:
			if schedule.status == "Pending":
				return schedule.due_date
		
		return None
	
	def get_overdue_amount(self):
		"""Get total overdue amount"""
		if not self.repayment_schedule:
			return 0
		
		today = datetime.now().date()
		overdue_amount = 0
		
		for schedule in self.repayment_schedule:
			if schedule.status == "Pending" and schedule.due_date < today:
				overdue_amount += schedule.installment_amount
		
		return overdue_amount


@frappe.whitelist()
def get_loan_summary(customer=None):
	"""Get loan summary for customer or all loans"""
	filters = {"status": ["!=", "Closed"]}
	if customer:
		filters["customer"] = customer
	
	loans = frappe.get_all("Loan",
						   filters=filters,
						   fields=["name", "customer", "customer_name", "loan_amount", 
								  "outstanding_amount", "status", "loan_date"])
	
	total_principal = sum(loan.loan_amount for loan in loans)
	total_outstanding = sum(loan.outstanding_amount for loan in loans)
	
	return {
		"loans": loans,
		"summary": {
			"total_loans": len(loans),
			"total_principal": total_principal,
			"total_outstanding": total_outstanding,
			"collection_rate": ((total_principal - total_outstanding) / total_principal * 100) if total_principal else 0
		}
	}


@frappe.whitelist()
def close_loan(loan_name):
	"""Close a loan"""
	loan = frappe.get_doc("Loan", loan_name)
	loan.status = "Closed"
	loan.outstanding_amount = 0
	loan.save()
	
	return loan.name
