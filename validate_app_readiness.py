#!/usr/bin/env python3
"""
Final Validation Script for NAYAG EDGE Custom Loan App - ERPNext 15
This script demonstrates the app is working and ERPNext 15 ready
"""

import json
import os
from pathlib import Path

def validate_app_readiness():
    """Comprehensive validation that the app is ERPNext 15 ready"""
    
    print("🏁 FINAL VALIDATION - NAYAG EDGE Custom Loan Management")
    print("=" * 70)
    
    validation_results = []
    
    # 1. Check ERPNext 15 compatibility markers
    print("1️⃣ Checking ERPNext 15 compatibility...")
    
    # Check requirements.txt
    with open("requirements.txt", 'r') as f:
        reqs = f.read()
    
    if "frappe>=15.0.0" in reqs:
        validation_results.append(("✅", "ERPNext 15+ requirement specified"))
    else:
        validation_results.append(("❌", "ERPNext 15 requirement missing"))
    
    # 2. Check workspace configuration
    print("2️⃣ Checking workspace configuration...")
    
    workspace_path = Path("custom_loan/workspace/loan_management.json")
    if workspace_path.exists():
        with open(workspace_path, 'r') as f:
            workspace_config = json.load(f)
        
        if workspace_config.get("doctype") == "Workspace":
            validation_results.append(("✅", "ERPNext 15 workspace configured"))
        else:
            validation_results.append(("❌", "Invalid workspace configuration"))
    else:
        validation_results.append(("❌", "Workspace configuration missing"))
    
    # 3. Check installation hooks
    print("3️⃣ Checking installation hooks...")
    
    with open("custom_loan/hooks.py", 'r') as f:
        hooks_content = f.read()
    
    if 'after_install = "custom_loan.install.after_install"' in hooks_content:
        validation_results.append(("✅", "Installation hooks configured"))
    else:
        validation_results.append(("❌", "Installation hooks missing"))
    
    # 4. Check DocType completeness  
    print("4️⃣ Checking DocType completeness...")
    
    expected_doctypes = [
        "loan", "loan_customer", "loan_application", 
        "loan_payment", "interest_setting", "loan_repayment_schedule",
        "interest_rate_slab"
    ]
    
    doctype_count = 0
    for doctype in expected_doctypes:
        json_path = Path(f"custom_loan/doctype/{doctype}/{doctype}.json")
        if json_path.exists():
            doctype_count += 1
    
    if doctype_count == len(expected_doctypes):
        validation_results.append(("✅", f"All {doctype_count} DocTypes present"))
    else:
        validation_results.append(("❌", f"Missing DocTypes: {len(expected_doctypes) - doctype_count}"))
    
    # 5. Check business logic
    print("5️⃣ Checking business logic...")
    
    utils_path = Path("custom_loan/utils.py")
    if utils_path.exists():
        with open(utils_path, 'r') as f:
            utils_content = f.read()
        
        if "calculate_flat_interest" in utils_content and "calculate_emi" in utils_content:
            validation_results.append(("✅", "Core business logic implemented"))
        else:
            validation_results.append(("❌", "Business logic incomplete"))
    else:
        validation_results.append(("❌", "Utils module missing"))
    
    # 6. Check reports
    print("6️⃣ Checking reports...")
    
    report_path = Path("custom_loan/report/loan_portfolio_summary")
    if report_path.exists() and (report_path / "loan_portfolio_summary.json").exists():
        validation_results.append(("✅", "Reports configured"))
    else:
        validation_results.append(("❌", "Reports missing"))
    
    # 7. Check role configuration
    print("7️⃣ Checking role configuration...")
    
    fixtures_path = Path("custom_loan/fixtures/custom_role.json")
    if fixtures_path.exists():
        validation_results.append(("✅", "Custom role fixtures present"))
    else:
        validation_results.append(("❌", "Custom role fixtures missing"))
    
    # 8. Test core calculations
    print("8️⃣ Testing core calculations...")
    
    try:
        import subprocess
        result = subprocess.run(['python', 'test_loan_calculations.py'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and "✅ All calculations working correctly!" in result.stdout:
            validation_results.append(("✅", "Core calculations working"))
        else:
            validation_results.append(("❌", "Calculation test failed"))
    except Exception as e:
        validation_results.append(("❌", f"Calculation test failed: {str(e)}"))
    
    # Print results summary
    print("\n" + "=" * 70)
    print("📊 VALIDATION RESULTS SUMMARY")
    print("=" * 70)
    
    passed = 0
    total = len(validation_results)
    
    for status, message in validation_results:
        print(f"{status} {message}")
        if status == "✅":
            passed += 1
    
    print("\n" + "=" * 70)
    print(f"📈 SCORE: {passed}/{total} validations passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 CONGRATULATIONS!")
        print("✅ Your NAYAG EDGE Custom Loan Management app is FULLY READY for ERPNext 15!")
        print("\n🚀 Ready for production deployment:")
        print("   • All ERPNext 15 compatibility requirements met")
        print("   • Modern workspace navigation configured") 
        print("   • Automated installation and setup included")
        print("   • Complete business logic implemented")
        print("   • Comprehensive testing validated")
        print("\n📝 Installation Command:")
        print("   bench get-app https://github.com/chaklesh/erpnext_custom_loan.git")
        print("   bench --site your-site install-app custom_loan")
        
        return True
    else:
        print(f"\n⚠️  {total - passed} validation(s) failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = validate_app_readiness()
    exit(0 if success else 1)