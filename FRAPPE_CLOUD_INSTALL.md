# Installation Guide for Frappe Cloud

## Prerequisites
- Frappe Cloud account with a site
- GitHub account (free)
- Git installed on your local machine

## Step-by-Step Installation

### 1. Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and create a new repository
2. Name it `custom_loan` or `erpnext-custom-loan`
3. Make it public (required for Frappe Cloud free plans)

### 2. Upload Your App to GitHub

Open terminal/command prompt in your project folder and run:

```bash
cd d:\Dev\Python\ERPnext-custom-loan

# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit: Custom Loan Management App for ERPNext"

# Add your GitHub repository as origin
git remote add origin https://github.com/YOUR_USERNAME/custom_loan.git

# Push to GitHub
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### 3. Install via Frappe Cloud Dashboard

1. **Login to Frappe Cloud:**
   - Go to [frappecloud.com](https://frappecloud.com)
   - Login to your account

2. **Navigate to Your Site:**
   - Select your site from the dashboard

3. **Install Custom App:**
   - Go to "Apps" section
   - Click "Install App" or "Add App"
   - Enter your repository URL: `https://github.com/YOUR_USERNAME/custom_loan`
   - Click "Install"

4. **Wait for Installation:**
   - The installation may take a few minutes
   - You'll receive a notification when complete

### 4. Alternative Method: Support Request

If the above method doesn't work:

1. **Create a Support Ticket:**
   - Go to Frappe Cloud support
   - Mention you want to install a custom app
   - Provide your GitHub repository URL
   - Include app details:
     - App Name: custom_loan
     - Description: Custom loan management system
     - Repository: https://github.com/YOUR_USERNAME/custom_loan

### 5. Verify Installation

1. **Check in ERPNext:**
   - Login to your ERPNext site
   - Go to "Awesome Bar" (search)
   - Type "Loan Customer" - it should appear
   - Or check: Settings → Apps → Installed Apps

2. **Access the Module:**
   - Go to main dashboard
   - Look for "Custom Loan Management" module
   - Or access via: Modules → Custom Loan

## Initial Setup After Installation

### 1. Create Interest Settings
```
Go to: Custom Loan → Interest Setting
Create settings like:
- Name: Standard Flat Rate
- Type: Flat Rate  
- Rate: 3% per month
- Mark as Active
```

### 2. Set User Permissions
```
Go to: Settings → Role Permission Manager
Search for: Loan Manager role
Assign to users who will manage loans
```

### 3. Create Your First Customer
```
Go to: Custom Loan → Loan Customer
Fill in customer details and save
```

## Troubleshooting

### Common Issues:

1. **App not appearing after installation:**
   - Clear cache: Settings → Reload
   - Check if installation completed successfully

2. **Permission errors:**
   - Ensure user has "Loan Manager" role
   - Check role permissions

3. **Import errors:**
   - Check if all dependencies are satisfied
   - Contact Frappe Cloud support

### Getting Help:

1. **Frappe Cloud Support:** support@frappe.io
2. **Community Forum:** discuss.erpnext.com
3. **GitHub Issues:** Create issue in your repository

## Important Notes:

- **Free Plans:** Only public repositories work
- **Paid Plans:** Private repositories are supported
- **Updates:** Push changes to GitHub and reinstall app
- **Backup:** Always backup your site before installing custom apps

## Sample Repository Structure:

Your GitHub repository should look like:
```
custom_loan/
├── __init__.py
├── hooks.py
├── setup.py
├── requirements.txt
├── README.md
├── MANIFEST.in
├── custom_loan/
│   ├── __init__.py
│   ├── utils.py
│   └── doctype/
│       ├── loan_customer/
│       ├── loan/
│       └── ...
└── config/
    └── desktop.py
```

Good luck with your loan management system! 🎉
