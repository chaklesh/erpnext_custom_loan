# NAYAG EDGE - Custom Loan Management for ERPNext 15

✅ **ERPNext 15 Compatible** - A comprehensive loan management system designed for local finance businesses, fully compatible with ERPNext 15 and the latest Frappe framework.

**Developed by:** Chaklesh Yadav - NAYAG  
**Product:** NAYAG EDGE (edge.nayag.com)  
**Company:** NAYAG

## Features

### 🏦 Loan Management
- **Multiple Loan Types**: Support for flat interest rate loans and EMI-based loans
- **Flexible Interest Calculation**: Configurable interest rates with amount-based slabs
- **Automated Payment Schedules**: Generate repayment schedules automatically
- **Payment Tracking**: Record and track all loan payments with detailed allocation

### 👥 Customer Management
- **Comprehensive Customer Profiles**: Store customer details, contact information, and documentation
- **Credit Assessment**: Track customer credit history and payment behavior
- **KYC Management**: Store ID proof and other verification documents
- **Customer Classification**: Support for individual, business, and self-help group customers

### 📋 Application Workflow
- **Loan Applications**: Structured loan application process with approval workflow
- **Credit Assessment**: Built-in tools for evaluating loan applications
- **Approval Management**: Multi-level approval process with rejection tracking
- **Document Management**: Attach and manage loan-related documents

### 💰 Payment & Collection
- **Payment Recording**: Easy payment entry with automatic allocation
- **Multiple Payment Methods**: Support for cash, bank transfer, UPI, etc.
- **Overdue Management**: Automatic identification of overdue payments
- **Penalty Calculation**: Configurable penalty rates for late payments

### 📊 Reporting & Analytics
- **Portfolio Summary**: Complete overview of loan portfolio
- **Overdue Reports**: Track and manage overdue loans
- **Customer Statements**: Detailed payment history for customers
- **Collection Reports**: Monitor payment collection efficiency

### 🔧 BMC Shop Integration (Future)
- **Inventory Management**: Track cement, sand, gravel, hardware, paints, sanitary items
- **Customer Credit (Udhari)**: Manage shop customer credit transactions
- **Purchase & Sales**: Complete shop management functionality

## Installation

### Prerequisites
- ERPNext v15.0 or higher
- Frappe Framework v15.0 or higher
- Python 3.10+

### Installation Steps

1. **Navigate to your ERPNext bench directory:**
   ```bash
   cd /path/to/your/erpnext/bench
   ```

2. **Get the app:**
   ```bash
   bench get-app custom_loan https://github.com/yourusername/custom_loan.git
   ```

3. **Install the app on your site:**
   ```bash
   bench --site your-site-name install-app custom_loan
   ```

4. **Restart bench:**
   ```bash
   bench restart
   ```

## Configuration

### Initial Setup

1. **Create Interest Settings:**
   - Go to: Loan Management → Interest Setting
   - Create settings for different loan types (Flat Rate, EMI)
   - Configure interest rates and penalty rates

2. **Set up Customer Categories:**
   - Configure customer types and verification requirements
   - Set up default settings for different customer categories

3. **Configure Payment Methods:**
   - Set up available payment methods
   - Configure reference number requirements

### User Roles

The app comes with a predefined role:
- **Loan Manager**: Full access to all loan management features

You can assign this role to users who need to manage loans.

## Usage Guide

### Creating a Customer

1. Go to: **Loan Management → Loan Customer**
2. Click **New**
3. Fill in customer details:
   - Basic information (name, mobile, email)
   - Address details
   - ID verification details
   - Business/occupation information
4. Save the customer

### Processing a Loan Application

1. **Create Application:**
   - Go to: **Loan Management → Loan Application**
   - Select customer and loan details
   - Specify loan amount, type, and tenure

2. **Review and Approve:**
   - Review application details
   - Update status to "Approved" or "Rejected"
   - Set approved amount and interest rate

3. **Create Loan:**
   - Use "Convert to Loan" button on approved applications
   - System will automatically generate repayment schedule

### Recording Payments

1. Go to: **Loan Management → Loan Payment**
2. Select the loan and enter payment details
3. System will automatically allocate payment to principal, interest, and penalties
4. Submit the payment entry

### Monitoring Portfolio

Use the built-in reports to monitor your loan portfolio:
- **Loan Portfolio Summary**: Overall portfolio status
- **Overdue Loans**: Loans with pending payments
- **Customer Statements**: Individual customer payment history

## Customization

### Interest Rate Configuration

The system supports flexible interest rate configuration:

```python
# Example: Configure different rates based on loan amount
Amount Slab 1: Rs. 1,000 - Rs. 10,000 @ 3% per month
Amount Slab 2: Rs. 10,001 - Rs. 50,000 @ 2.5% per month
Amount Slab 3: Rs. 50,001+ @ 2% per month
```

### Calculation Methods

**Flat Interest Rate:**
- Total Interest = Principal × Rate × Tenure
- Monthly Payment = (Principal + Total Interest) ÷ Tenure

**EMI (Reducing Balance):**
- EMI = [P × r × (1+r)^n] ÷ [(1+r)^n - 1]
- Where P = Principal, r = monthly rate, n = tenure

## API Endpoints

The app provides several API endpoints for integration:

### Loan Calculator
```python
frappe.call({
    method: "custom_loan.utils.get_loan_calculator_data",
    args: {
        loan_type: "Flat Rate",
        principal: 10000,
        rate_per_month: 3,
        tenure_months: 12
    }
})
```

### Customer Summary
```python
frappe.call({
    method: "custom_loan.custom_loan.doctype.loan_customer.loan_customer.get_customer_summary",
    args: {
        customer: "CUST-001"
    }
})
```

## Troubleshooting

### Common Issues

1. **Interest not calculating correctly:**
   - Check Interest Setting configuration
   - Ensure active settings are properly configured

2. **Payments not updating loan balance:**
   - Ensure payment entry is submitted
   - Check if loan status allows payments

3. **Repayment schedule not generating:**
   - Verify loan amount and tenure are valid
   - Check if loan type is properly set

### Support

For support and custom development:
- Email: admin@yourcompany.com
- Documentation: [Your Documentation URL]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Roadmap

### Version 0.2.0 (Upcoming)
- Mobile app for field officers
- SMS integration for payment reminders
- Advanced reporting with charts
- Bulk payment import

### Version 0.3.0 (Future)
- BMC shop inventory management
- Customer credit (udhari) tracking
- Purchase and sales management
- Multi-location support

## Acknowledgments

Built with ❤️ using:
- [Frappe Framework](https://frappeframework.com/)
- [ERPNext](https://erpnext.com/)

---

**Note:** This is a beta version. Please test thoroughly before using in production.
