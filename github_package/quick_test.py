#!/usr/bin/env python3
"""
🧪 AION Quick Test Script
Quick test to verify AION installation and basic functionality
"""

import sys
import os
import importlib
from pathlib import Path

def test_imports():
    """Test if all modules can be imported"""
    print("📦 Testing imports...")
    
    modules_to_test = [
        "typer",
        "rich", 
        "fastapi",
        "textual",
        "openai",
        "requests",
        "colorama",
        "cryptography",
    ]
    
    failed_imports = []
    
    for module in modules_to_test:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module} - {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_aion_modules():
    """Test AION specific modules"""
    print("\n🤖 Testing AION modules...")
    
    # Add current directory to path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    aion_modules = [
        ("main", "Main application"),
        ("start_aion_en", "English launcher"),
        ("start_aion", "Arabic launcher"),
        ("core.ai_providers", "AI Providers"),
        ("core.security", "Security Manager"),
        ("core.executor", "Code Executor"),
        ("core.plugins", "Plugin Manager"),
        ("interfaces.cli", "CLI Interface"),
        ("interfaces.tui", "TUI Interface"), 
        ("interfaces.web", "Web Interface"),
        ("utils.translator", "Translator"),
        ("utils.helpers", "Helpers"),
        ("utils.arabic_support", "Arabic Support"),
    ]
    
    failed_modules = []
    
    for module_name, description in aion_modules:
        try:
            importlib.import_module(module_name)
            print(f"✅ {description} ({module_name})")
        except ImportError as e:
            print(f"❌ {description} ({module_name}) - {e}")
            failed_modules.append(module_name)
    
    return len(failed_modules) == 0

def test_config_files():
    """Test configuration files"""
    print("\n⚙️  Testing configuration files...")
    
    config_files = [
        "config/ai_config_template.json",
        "locales/en.json",
        "locales/ar.json",
        "locales/fr.json",
        "locales/de.json",
        "locales/es.json",
        "locales/zh.json",
        "locales/no.json",
    ]
    
    missing_files = []
    
    for file_path in config_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (missing)")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_scripts():
    """Test launcher scripts"""
    print("\n📜 Testing launcher scripts...")
    
    scripts = [
        ("aion.sh", "Linux/Mac launcher"),
        ("aion.bat", "Windows launcher"),
        ("run.py", "Setup script"),
    ]
    
    missing_scripts = []
    
    for script_name, description in scripts:
        path = Path(script_name)
        if path.exists():
            print(f"✅ {description} ({script_name})")
        else:
            print(f"❌ {description} ({script_name}) (missing)")
            missing_scripts.append(script_name)
    
    return len(missing_scripts) == 0

def test_basic_functionality():
    """Test basic AION functionality"""
    print("\n🔧 Testing basic functionality...")

    try:
        # Test translator
        from utils.translator import Translator
        translator = Translator()
        result = translator.get("hello", "Hello")
        print(f"✅ Translation test: get('hello') -> '{result}'")

        # Test Arabic support
        from utils.arabic_support import format_arabic_message
        arabic_text = format_arabic_message("مرحبا", "success")
        print(f"✅ Arabic support test: {arabic_text}")

        # Test security manager
        from core.security import SecurityManager
        security = SecurityManager()
        print(f"✅ Security Manager initialized")

        return True

    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 AION Quick Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("AION Modules Test", test_aion_modules),
        ("Config Files Test", test_config_files),
        ("Scripts Test", test_scripts),
        ("Basic Functionality Test", test_basic_functionality),
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                print(f"✅ {test_name} PASSED")
                passed_tests += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "="*50)
    print("🏁 Test Summary")
    print("="*50)
    print(f"✅ Passed: {passed_tests}/{total_tests}")
    print(f"❌ Failed: {total_tests - passed_tests}/{total_tests}")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! AION is ready to use!")
        print("\n🚀 Quick start commands:")
        print("   python start_aion_en.py  # English interface")
        print("   python start_aion.py     # Arabic interface")
        print("   python main.py cli       # Direct CLI")
        return 0
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
