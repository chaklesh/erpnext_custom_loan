# Copyright (c) 2025, Your Company and Contributors
# See license.txt

import frappe
import unittest

class TestLoanCustomer(unittest.TestCase):
	def setUp(self):
		"""Set up test data"""
		self.test_customer_data = {
			"customer_name": "Test Customer",
			"mobile_number": "9876543210",
			"customer_type": "Individual",
			"status": "Active"
		}
	
	def test_customer_creation(self):
		"""Test basic customer creation"""
		customer = frappe.get_doc("Loan Customer", self.test_customer_data)
		customer.insert()
		
		self.assertEqual(customer.customer_name, "Test Customer")
		self.assertEqual(customer.mobile_number, "9876543210")
		
		# Clean up
		customer.delete()
	
	def test_mobile_validation(self):
		"""Test mobile number validation"""
		# Test invalid mobile number
		invalid_data = self.test_customer_data.copy()
		invalid_data["mobile_number"] = "123"
		
		customer = frappe.get_doc("Loan Customer", invalid_data)
		
		with self.assertRaises(frappe.ValidationError):
			customer.insert()
	
	def test_duplicate_mobile(self):
		"""Test duplicate mobile number validation"""
		# Create first customer
		customer1 = frappe.get_doc("Loan Customer", self.test_customer_data)
		customer1.insert()
		
		# Try to create second customer with same mobile
		duplicate_data = self.test_customer_data.copy()
		duplicate_data["customer_name"] = "Duplicate Customer"
		
		customer2 = frappe.get_doc("Loan Customer", duplicate_data)
		
		with self.assertRaises(frappe.ValidationError):
			customer2.insert()
		
		# Clean up
		customer1.delete()
	
	def tearDown(self):
		"""Clean up test data"""
		try:
			frappe.db.delete("Loan Customer", {"mobile_number": "9876543210"})
		except:
			pass
