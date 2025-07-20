# NAYAG EDGE - GitHub Setup & Bench Installation Guide

## 🏢 Company: NAYAG
## 👨‍💻 Developer: Chaklesh Yadav  
## 🌐 Product: NAYAG EDGE (edge.nayag.com)
## 📱 GitHub: github.com/chaklesh

---

## 🚀 Step 1: Push to Your GitHub

Run these commands in your terminal:

```bash
# Navigate to your project directory
cd d:\Dev\Python\ERPnext-custom-loan

# Initialize git repository
git init

# Add all files
git add .

# First commit with your signature
git commit -m "Initial commit: NAYAG EDGE Loan Management System

- Custom ERPNext app for local finance business
- Supports flat interest and EMI calculations  
- Complete customer and payment management
- Developed by Chaklesh Yadav @ NAYAG
- Product: NAYAG EDGE (edge.nayag.com)"

# Add your GitHub repository as origin
git remote add origin https://github.com/chaklesh/custom_loan.git

# Push to GitHub (main branch)
git push -u origin main
```

## 🔧 Step 2: Install via Bench (Your ERPNext Server)

Once pushed to GitHub, install on your ERPNext site:

```bash
# Navigate to your bench directory
cd ~/frappe-bench

# Get the app from your GitHub
bench get-app custom_loan https://github.com/chaklesh/custom_loan.git

# Install on your site (replace 'your-site-name' with actual site)
bench --site your-site-name install-app custom_loan

# Run migrations to create database tables
bench --site your-site-name migrate

# Restart services
bench restart

# Clear cache for good measure
bench --site your-site-name clear-cache
```

## ✅ Step 3: Verify Installation

```bash
# Check if app is installed
bench --site your-site-name list-apps

# Should show custom_loan in the list
```

## 🎯 Step 4: Access Your Loan Management System

1. **Login to your ERPNext site**
2. **Search for "Loan Customer"** in the awesome bar
3. **Go to Modules** → Look for **"NAYAG EDGE Loan Management"**
4. **Start using:**
   - Create Interest Settings
   - Add customers
   - Process loan applications

## 📋 Quick Test Checklist

- [ ] Create a Loan Customer
- [ ] Set up Interest Settings (3% flat rate, 2.5% EMI)
- [ ] Create a Loan Application
- [ ] Convert to Active Loan
- [ ] Record a Payment
- [ ] Check Portfolio Summary report

## 🔄 For Future Updates

When you make changes to your app:

```bash
# In your local directory
git add .
git commit -m "Update: [describe your changes]"
git push origin main

# On your server, update the app
cd ~/frappe-bench
bench update --app custom_loan
bench --site your-site-name migrate
bench restart
```

## 🆘 Troubleshooting

**If installation fails:**
```bash
# Check logs
tail -f ~/frappe-bench/logs/frappe.log

# Try clearing cache
bench --site your-site-name clear-cache
bench restart

# Re-run migration
bench --site your-site-name migrate
```

**Permission issues:**
```bash
sudo chown -R frappe:frappe ~/frappe-bench/apps/custom_loan
```

## 📞 Support

- **Developer:** Chaklesh Yadav @ NAYAG
- **Product:** NAYAG EDGE
- **Website:** edge.nayag.com
- **GitHub:** github.com/chaklesh/custom_loan

---

## 🎉 Ready to Go!

Your NAYAG EDGE Loan Management System is ready for action! This professional-grade solution will help streamline your brother's local finance business with:

- ✅ Complete customer management
- ✅ Flexible loan calculations (flat & EMI)
- ✅ Payment tracking & collection
- ✅ Comprehensive reporting
- ✅ Future BMC shop integration ready

**Built with ❤️ by NAYAG Team**
