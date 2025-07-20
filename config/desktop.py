from frappe import _


def get_data():
	return [
		{
			"label": _("Loan Management"),
			"items": [
				{
					"type": "doctype",
					"name": "Loan Customer",
					"description": _("Manage loan customers")
				},
				{
					"type": "doctype",
					"name": "Loan Application",
					"description": _("Create and manage loan applications")
				},
				{
					"type": "doctype",
					"name": "Loan",
					"description": _("Active loans with payment schedules")
				},
				{
					"type": "doctype",
					"name": "Loan Payment",
					"description": _("Record loan payments and collections")
				},
				{
					"type": "doctype",
					"name": "Interest Setting",
					"description": _("Configure interest rates and settings")
				}
			]
		},
		{
			"label": _("BMC Shop Management"),
			"items": [
				{
					"type": "doctype",
					"name": "Shop Customer",
					"description": _("Manage shop customers and credit accounts")
				},
				{
					"type": "doctype",
					"name": "Customer Credit",
					"description": _("Track customer udhari/credit transactions")
				}
			]
		},
		{
			"label": _("Reports"),
			"items": [
				{
					"type": "report",
					"name": "Loan Portfolio Summary",
					"is_query_report": True,
					"description": _("Overview of all loans and their status")
				},
				{
					"type": "report",
					"name": "Overdue Loans",
					"is_query_report": True,
					"description": _("List of overdue loan payments")
				},
				{
					"type": "report",
					"name": "Customer Statement",
					"is_query_report": True,
					"description": _("Detailed customer payment history")
				},
				{
					"type": "report",
					"name": "Interest Collection",
					"is_query_report": True,
					"description": _("Interest collected over time")
				}
			]
		}
	]
