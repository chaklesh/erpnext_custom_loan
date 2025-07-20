# ERPNext Bench Installation Guide

## Prerequisites
- ERPNext bench setup (local installation)
- Your custom_loan app directory
- Site already created in bench

## Installation Steps

### Step 1: Locate Your Bench Directory
```bash
# Usually located at:
cd ~/frappe-bench
# or
cd /opt/bench/frappe-bench
```

### Step 2: Copy App to Bench Apps Directory
```bash
# Option A: Copy your app directory directly
cp -r /path/to/your/custom_loan ~/frappe-bench/apps/

# Option B: Use bench get-app with local path
bench get-app custom_loan /path/to/your/custom_loan
```

### Step 3: Install App on Site
```bash
# Replace 'your-site-name' with your actual site name
bench --site your-site-name install-app custom_loan
```

### Step 4: Run Database Migration
```bash
# This creates all DocType tables in database
bench --site your-site-name migrate
```

### Step 5: Restart Services
```bash
# Restart to load new app
bench restart

# Or if using supervisor
sudo supervisorctl restart all
```

### Step 6: Verify Installation
```bash
# Check if app is installed
bench --site your-site-name list-apps

# Should show custom_loan in the list
```

## Alternative: Manual Installation

### 1. Copy Files Manually
```bash
# Copy app to apps directory
cp -r custom_loan ~/frappe-bench/apps/

# Set correct permissions
sudo chown -R frappe:frappe ~/frappe-bench/apps/custom_loan
```

### 2. Edit sites/apps.txt
```bash
# Add custom_loan to apps list
echo "custom_loan" >> ~/frappe-bench/sites/your-site-name/apps.txt
```

### 3. Install and Migrate
```bash
bench --site your-site-name migrate
bench restart
```

## Troubleshooting

### Common Issues:

1. **Permission Denied:**
```bash
sudo chown -R $(whoami):$(whoami) ~/frappe-bench/apps/custom_loan
```

2. **App Already Exists:**
```bash
# Remove existing app first
rm -rf ~/frappe-bench/apps/custom_loan
# Then reinstall
```

3. **Migration Errors:**
```bash
# Check error logs
bench --site your-site-name console
# Or
tail -f ~/frappe-bench/logs/frappe.log
```

4. **Import Errors:**
```bash
# Clear cache and try again
bench --site your-site-name clear-cache
bench --site your-site-name migrate
```

### Verification Steps:

1. **Check App List:**
```bash
bench --site your-site-name list-apps
```

2. **Access ERPNext:**
- Login to your site
- Go to Awesome Bar and search "Loan Customer"
- Should appear if installed correctly

3. **Check Modules:**
- Go to Modules page
- Look for "Custom Loan" module

## Post-Installation Setup

### 1. Create User Roles
```bash
# Access your site
bench --site your-site-name console
```
```python
# In console:
import frappe
frappe.get_doc("Role", {"role_name": "Loan Manager"}).insert(ignore_if_duplicate=True)
```

### 2. Set Permissions
- Go to: Setup → Role Permission Manager
- Search for "Loan" doctypes
- Assign permissions to "Loan Manager" role

### 3. Create Initial Data
- Create Interest Settings
- Add first customer
- Test loan creation

## Development Mode

For development, enable developer mode:
```bash
bench --site your-site-name set-config developer_mode 1
bench --site your-site-name clear-cache
```

## Commands Reference

```bash
# Essential bench commands for app management
bench get-app [app-name] [git-url]           # Get app from repository
bench install-app [app-name] --site [site]   # Install app on site  
bench uninstall-app [app-name] --site [site] # Uninstall app
bench migrate --site [site]                  # Run database migrations
bench restart                               # Restart all services
bench clear-cache --site [site]            # Clear cache
bench list-apps --site [site]              # List installed apps
```

Good luck with your loan management system! 🎉
