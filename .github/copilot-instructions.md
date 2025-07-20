<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# NAYAG EDGE - ERPNext Custom Loan Management Module

## Project Context
This is a custom ERPNext application built by NAYAG using the Frappe framework for managing local finance business operations, specifically:

1. **Loan Management**: Flat interest rate loans and EMI-based loans
2. **Customer Management**: Comprehensive customer profiles and credit tracking
3. **Payment Tracking**: Payment collection and overdue management
4. **BMC Shop Integration**: Future support for inventory and customer credit management

## Framework Guidelines
- This project uses **Frappe Framework v15+** conventions
- All DocTypes follow ERPNext naming and structure conventions
- Use `frappe.get_doc()` for document operations
- Follow Frappe's validation and event patterns
- Use `frappe.throw()` for error handling
- Implement proper permissions using roles

## Code Style Guidelines
- Follow PEP 8 for Python code formatting
- Use descriptive variable names reflecting business context
- Add comprehensive docstrings for all functions
- Include validation logic in document classes
- Use Frappe utilities for date/currency calculations

## Business Logic
- **Flat Interest**: Total Interest = Principal × Rate × Tenure
- **EMI Calculation**: Use reducing balance method
- **Payment Allocation**: Penalty → Interest → Principal
- **Status Management**: Draft → Active → Closed/Overdue
- **Customer Types**: Individual, Business, Self Help Group

## Key Components
- **DocTypes**: Loan Customer, Loan Application, Loan, Loan Payment, Interest Setting
- **Reports**: Portfolio summary, overdue tracking, customer statements
- **Utilities**: Interest calculations, payment schedules, SMS reminders

## Integration Points
- ERPNext Customer management (future)
- SMS gateway for reminders
- Payment gateway integration (future)
- Accounting entry integration (future)

When working on this project, prioritize:
1. Data validation and error handling
2. Business rule compliance
3. User experience in Frappe UI
4. Performance for large datasets
5. Extensibility for future BMC shop features
