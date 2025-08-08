#!/usr/bin/env python3
"""
ERPNext 15 Compatibility Test for NAYAG EDGE Custom Loan App
This script validates the app structure and compatibility
"""

import json
import os
import re
from pathlib import Path

def test_app_structure():
    """Test if the app has proper Frappe/ERPNext structure"""
    base_path = Path(".")
    
    print("🔍 Testing App Structure...")
    
    # Check essential files
    essential_files = [
        "setup.py",
        "pyproject.toml", 
        "requirements.txt",
        "custom_loan/__init__.py",
        "custom_loan/hooks.py"
    ]
    
    for file_path in essential_files:
        if (base_path / file_path).exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    return True

def test_doctype_structure():
    """Test DocType JSON structure for ERPNext 15 compatibility"""
    print("\n🔍 Testing DocType Structure...")
    
    doctype_path = Path("custom_loan/doctype")
    doctype_folders = [d for d in doctype_path.iterdir() if d.is_dir() and d.name != "__pycache__"]
    
    for doctype_folder in doctype_folders:
        doctype_name = doctype_folder.name
        json_file = doctype_folder / f"{doctype_name}.json"
        py_file = doctype_folder / f"{doctype_name}.py"
        
        if json_file.exists():
            print(f"✅ {doctype_name}.json exists")
            
            # Test JSON validity
            try:
                with open(json_file, 'r') as f:
                    doctype_data = json.load(f)
                
                # Check essential fields
                required_fields = ["doctype", "fields", "permissions"]
                for field in required_fields:
                    if field in doctype_data:
                        print(f"  ✅ {doctype_name} has {field}")
                    else:
                        print(f"  ❌ {doctype_name} missing {field}")
                        
            except json.JSONDecodeError as e:
                print(f"  ❌ {doctype_name}.json has invalid JSON: {e}")
                return False
        else:
            print(f"❌ {doctype_name}.json missing")
            
        if py_file.exists():
            print(f"✅ {doctype_name}.py exists")
        else:
            print(f"⚠️  {doctype_name}.py missing (optional for simple DocTypes)")
    
    return True

def test_workspace_config():
    """Test workspace configuration for ERPNext 15"""
    print("\n🔍 Testing Workspace Configuration...")
    
    workspace_path = Path("custom_loan/workspace")
    if workspace_path.exists():
        print("✅ Workspace directory exists")
        
        workspace_files = list(workspace_path.glob("*.json"))
        if workspace_files:
            print(f"✅ Found {len(workspace_files)} workspace configuration(s)")
            return True
        else:
            print("❌ No workspace JSON files found")
            return False
    else:
        print("❌ Workspace directory missing")
        return False

def test_hooks_configuration():
    """Test hooks.py for proper configuration"""
    print("\n🔍 Testing Hooks Configuration...")
    
    hooks_path = Path("custom_loan/hooks.py")
    if not hooks_path.exists():
        print("❌ hooks.py missing")
        return False
    
    with open(hooks_path, 'r') as f:
        hooks_content = f.read()
    
    # Check for essential hooks
    essential_configs = [
        "app_name",
        "app_title", 
        "app_publisher",
        "app_version"
    ]
    
    for config in essential_configs:
        if config in hooks_content:
            print(f"✅ {config} configured")
        else:
            print(f"❌ {config} missing in hooks")
            return False
    
    return True

def test_requirements():
    """Test requirements for ERPNext 15 compatibility"""
    print("\n🔍 Testing Requirements...")
    
    req_path = Path("requirements.txt")
    if req_path.exists():
        with open(req_path, 'r') as f:
            requirements = f.read()
        
        if "frappe>=15.0.0" in requirements:
            print("✅ Frappe 15+ requirement specified")
            return True
        elif "frappe" in requirements:
            print("⚠️  Frappe dependency found but version may not be ERPNext 15 compatible")
            return True
        else:
            print("❌ Frappe dependency missing")
            return False
    else:
        print("❌ requirements.txt missing")
        return False

def main():
    """Main test runner"""
    print("=" * 60)
    print("🧪 NAYAG EDGE Custom Loan App - ERPNext 15 Compatibility Test")
    print("=" * 60)
    
    tests = [
        test_app_structure,
        test_doctype_structure,
        test_workspace_config,
        test_hooks_configuration,
        test_requirements
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! App appears to be ERPNext 15 compatible!")
        return 0
    else:
        print(f"⚠️  {total - passed} test(s) failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    exit(main())