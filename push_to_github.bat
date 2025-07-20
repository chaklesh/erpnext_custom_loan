@echo off
echo.
echo ========================================
echo   NAYAG EDGE - GitHub Push Script
echo   Developer: Chaklesh Yadav @ NAYAG
echo ========================================
echo.

echo Step 1: Initializing Git Repository...
git init

echo.
echo Step 2: Adding all files...
git add .

echo.
echo Step 3: Creating initial commit...
git commit -m "Initial commit: NAYAG EDGE Loan Management System

- Custom ERPNext app for local finance business
- Supports flat interest and EMI calculations  
- Complete customer and payment management
- Comprehensive reporting and dashboard
- Future BMC shop integration ready
- Developed by Chaklesh Yadav @ NAYAG
- Product: NAYAG EDGE (edge.nayag.com)"

echo.
echo Step 4: Adding GitHub remote...
git remote add origin https://github.com/chaklesh/custom_loan.git

echo.
echo Step 5: Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo   SUCCESS! Your app is now on GitHub
echo   Repository: github.com/chaklesh/custom_loan
echo ========================================
echo.
echo Next steps:
echo 1. Go to your ERPNext server
echo 2. Run: bench get-app custom_loan https://github.com/chaklesh/custom_loan.git
echo 3. Run: bench --site your-site-name install-app custom_loan
echo 4. Run: bench --site your-site-name migrate
echo 5. Run: bench restart
echo.
pause
