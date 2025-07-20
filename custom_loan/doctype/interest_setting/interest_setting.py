# Copyright (c) 2025, Your Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InterestSetting(Document):
	def validate(self):
		self.validate_rates()
		self.set_default_if_active()
	
	def validate_rates(self):
		"""Validate interest rates"""
		if self.default_rate <= 0:
			frappe.throw("Default rate must be greater than 0")
		
		if self.penalty_rate < 0:
			frappe.throw("Penalty rate cannot be negative")
		
		# Validate amount slabs
		if self.amount_slabs:
			prev_max = 0
			for slab in self.amount_slabs:
				if slab.min_amount <= prev_max:
					frappe.throw("Amount slabs should not overlap")
				if slab.max_amount and slab.max_amount <= slab.min_amount:
					frappe.throw("Maximum amount should be greater than minimum amount")
				prev_max = slab.max_amount or float('inf')
	
	def set_default_if_active(self):
		"""Set other settings as non-default if this one is active and default"""
		if self.is_active:
			# Set other settings of same type as non-active
			frappe.db.sql("""
				UPDATE `tabInterest Setting`
				SET is_active = 0
				WHERE interest_type = %s AND name != %s
			""", (self.interest_type, self.name))
	
	def get_applicable_rate(self, amount):
		"""Get applicable interest rate for given loan amount"""
		if not self.amount_slabs:
			return self.default_rate
		
		for slab in self.amount_slabs:
			if amount >= slab.min_amount:
				if not slab.max_amount or amount <= slab.max_amount:
					return slab.interest_rate
		
		return self.default_rate


@frappe.whitelist()
def get_active_settings():
	"""Get all active interest settings"""
	return frappe.get_all("Interest Setting",
						  filters={"is_active": 1},
						  fields=["name", "setting_name", "interest_type", "default_rate"],
						  order_by="interest_type")


@frappe.whitelist()
def get_setting_for_loan_type(interest_type):
	"""Get active setting for specific loan type"""
	return frappe.get_doc("Interest Setting", 
						  {"interest_type": interest_type, "is_active": 1})
