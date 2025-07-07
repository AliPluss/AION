#!/usr/bin/env python3
"""
🧪 AION PyPI Package Test Script
Test script to verify AION package functionality after PyPI installation
"""

import sys
import subprocess
import importlib
import os
from pathlib import Path

def test_import():
    """Test if AION can be imported successfully"""
    print("🧪 Testing AION import...")
    
    try:
        import aion
        print("✅ Successfully imported 'aion' package")
        
        # Test main module
        from aion import main
        print("✅ Successfully imported 'aion.main'")
        
        # Test core modules
        from aion.core import ai_providers
        print("✅ Successfully imported 'aion.core.ai_providers'")
        
        from aion.interfaces import arrow_navigation
        print("✅ Successfully imported 'aion.interfaces.arrow_navigation'")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_entry_points():
    """Test if entry points are working"""
    print("\n🧪 Testing entry points...")
    
    commands = ['aion', 'aion-cli', 'aion-ai']
    
    for cmd in commands:
        try:
            # Test if command exists
            result = subprocess.run(
                [cmd, '--help'], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"✅ Command '{cmd}' is working")
            else:
                print(f"❌ Command '{cmd}' failed with return code {result.returncode}")
                print(f"   Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"⚠️ Command '{cmd}' timed out")
        except FileNotFoundError:
            print(f"❌ Command '{cmd}' not found")
        except Exception as e:
            print(f"❌ Error testing '{cmd}': {e}")

def test_dependencies():
    """Test if all required dependencies are available"""
    print("\n🧪 Testing dependencies...")
    
    required_deps = [
        'typer',
        'rich', 
        'textual',
        'fastapi',
        'uvicorn',
        'pydantic',
        'cryptography',
        'psutil',
        'aiofiles',
        'httpx',
        'python-dotenv',
        'openai',
        'google-generativeai',
        'requests',
        'pyyaml',
        'click'
    ]
    
    missing_deps = []
    
    for dep in required_deps:
        try:
            # Handle special cases
            if dep == 'python-dotenv':
                importlib.import_module('dotenv')
            elif dep == 'google-generativeai':
                importlib.import_module('google.generativeai')
            else:
                importlib.import_module(dep)
            
            print(f"✅ Dependency '{dep}' is available")
            
        except ImportError:
            print(f"❌ Dependency '{dep}' is missing")
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"\n⚠️ Missing dependencies: {', '.join(missing_deps)}")
        return False
    else:
        print("\n✅ All dependencies are available")
        return True

def test_package_structure():
    """Test if package structure is correct"""
    print("\n🧪 Testing package structure...")
    
    try:
        import aion
        package_path = Path(aion.__file__).parent
        
        expected_modules = [
            'main.py',
            'core',
            'interfaces', 
            'utils'
        ]
        
        for module in expected_modules:
            module_path = package_path / module
            if module_path.exists():
                print(f"✅ Found '{module}'")
            else:
                print(f"❌ Missing '{module}'")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking package structure: {e}")
        return False

def test_version():
    """Test if version information is available"""
    print("\n🧪 Testing version information...")
    
    try:
        import aion
        
        # Try to get version from different sources
        version = None
        
        # Method 1: __version__ attribute
        if hasattr(aion, '__version__'):
            version = aion.__version__
            print(f"✅ Version from __version__: {version}")
        
        # Method 2: importlib.metadata
        try:
            from importlib.metadata import version as get_version
            version = get_version('aion-ai')
            print(f"✅ Version from metadata: {version}")
        except Exception:
            pass
        
        if version:
            return True
        else:
            print("⚠️ Version information not found")
            return False
            
    except Exception as e:
        print(f"❌ Error getting version: {e}")
        return False

def test_basic_functionality():
    """Test basic AION functionality"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        from aion.interfaces.arrow_navigation import ArrowNavigator
        
        # Test ArrowNavigator creation
        test_items = [
            ("en", "English", "🇬🇧"),
            ("ar", "Arabic", "🇮🇶"),
        ]
        
        navigator = ArrowNavigator(test_items, "Test Navigation")
        print("✅ ArrowNavigator created successfully")
        
        # Test menu rendering
        panel = navigator.render()
        print("✅ Menu rendering works")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and return overall result"""
    print("🚀 AION PyPI Package Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_import),
        ("Entry Points Test", test_entry_points),
        ("Dependencies Test", test_dependencies),
        ("Package Structure Test", test_package_structure),
        ("Version Test", test_version),
        ("Basic Functionality Test", test_basic_functionality),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "="*50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! AION package is working correctly.")
        return True
    else:
        print(f"⚠️ {total - passed} tests failed. Please check the issues above.")
        return False

def main():
    """Main test function"""
    success = run_all_tests()
    
    if success:
        print("\n🎯 AION is ready to use!")
        print("Try running: aion --help")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the installation.")
        sys.exit(1)

if __name__ == "__main__":
    main()
