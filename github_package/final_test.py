#!/usr/bin/env python3
"""
🧪 AION Final Test Suite
Complete functionality test for AION package
"""

import sys
import os
import subprocess
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🧪 {title}")
    print("="*60)

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_warning(message):
    """Print warning message"""
    print(f"⚠️  {message}")

def test_imports():
    """Test all AION imports"""
    print_header("Import Tests")
    
    imports_to_test = [
        ("main", "Main application"),
        ("start_aion", "Arabic launcher"),
        ("start_aion_en", "English launcher"),
        ("core.ai_providers", "AI Providers"),
        ("core.security", "Security Manager"),
        ("core.plugins", "Plugin Manager"),
        ("utils.translator", "Translator"),
        ("utils.helpers", "Helpers"),
        ("utils.arabic_support", "Arabic Support"),
        ("interfaces.cli", "CLI Interface"),
        ("interfaces.tui", "TUI Interface"),
        ("interfaces.web", "Web Interface"),
    ]
    
    success_count = 0
    for module_name, description in imports_to_test:
        try:
            __import__(module_name)
            print_success(f"{description} ({module_name})")
            success_count += 1
        except ImportError as e:
            print_error(f"{description} ({module_name}): {e}")
        except Exception as e:
            print_warning(f"{description} ({module_name}): {e}")
    
    print(f"\n📊 Import Results: {success_count}/{len(imports_to_test)} successful")
    return success_count == len(imports_to_test)

def test_basic_functionality():
    """Test basic AION functionality"""
    print_header("Basic Functionality Tests")
    
    try:
        # Test translator
        from utils.translator import Translator
        translator = Translator()
        result = translator.get("hello", "Hello")
        print_success(f"Translator: get('hello') -> '{result}'")
        
        # Test Arabic support
        from utils.arabic_support import format_arabic_message
        arabic_text = format_arabic_message("مرحبا", "success")
        print_success(f"Arabic support: {arabic_text}")
        
        # Test security manager
        from core.security import SecurityManager
        security = SecurityManager()
        print_success("Security Manager initialized")
        
        # Test AI providers
        from core.ai_providers import AIManager
        ai_manager = AIManager()
        print_success("AI Manager initialized")
        
        # Test plugin manager
        from core.plugins import PluginManager
        plugin_manager = PluginManager()
        print_success("Plugin Manager initialized")
        
        return True
        
    except Exception as e:
        print_error(f"Basic functionality test failed: {e}")
        return False

def test_launchers():
    """Test launcher scripts"""
    print_header("Launcher Tests")
    
    launchers = [
        ("start_aion_en.py", "English launcher"),
        ("start_aion.py", "Arabic launcher"),
        ("main.py", "Main application")
    ]
    
    success_count = 0
    for launcher, description in launchers:
        if Path(launcher).exists():
            print_success(f"{description} ({launcher}) - File exists")
            success_count += 1
        else:
            print_error(f"{description} ({launcher}) - File missing")
    
    print(f"\n📊 Launcher Results: {success_count}/{len(launchers)} found")
    return success_count == len(launchers)

def test_configuration():
    """Test configuration files"""
    print_header("Configuration Tests")
    
    config_files = [
        ("config/ai_config_template.json", "AI Config Template"),
        ("locales/en.json", "English Locale"),
        ("locales/ar.json", "Arabic Locale"),
        ("locales/fr.json", "French Locale"),
        ("locales/de.json", "German Locale"),
        ("locales/es.json", "Spanish Locale"),
        ("locales/zh.json", "Chinese Locale"),
        ("locales/no.json", "Norwegian Locale"),
    ]
    
    success_count = 0
    for config_file, description in config_files:
        if Path(config_file).exists():
            print_success(f"{description} ({config_file})")
            success_count += 1
        else:
            print_error(f"{description} ({config_file}) - Missing")
    
    print(f"\n📊 Configuration Results: {success_count}/{len(config_files)} found")
    return success_count == len(config_files)

def test_package_structure():
    """Test package structure"""
    print_header("Package Structure Tests")
    
    required_files = [
        ("setup.py", "Setup script"),
        ("pyproject.toml", "Project configuration"),
        ("requirements.txt", "Requirements"),
        ("README.md", "README file"),
        ("LICENSE", "License file"),
        ("__init__.py", "Package init"),
        ("__main__.py", "Main module"),
        (".gitignore", "Git ignore"),
        ("Dockerfile", "Docker configuration"),
        ("docker-compose.yml", "Docker Compose"),
        ("Makefile", "Build automation"),
    ]
    
    success_count = 0
    for file_path, description in required_files:
        if Path(file_path).exists():
            print_success(f"{description} ({file_path})")
            success_count += 1
        else:
            print_error(f"{description} ({file_path}) - Missing")
    
    print(f"\n📊 Package Structure Results: {success_count}/{len(required_files)} found")
    return success_count >= len(required_files) * 0.8  # 80% threshold

def main():
    """Run all tests"""
    print("🚀 AION Final Test Suite")
    print("=" * 60)
    
    # Run all tests
    tests = [
        ("Package Structure", test_package_structure),
        ("Configuration", test_configuration),
        ("Imports", test_imports),
        ("Launchers", test_launchers),
        ("Basic Functionality", test_basic_functionality),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"{test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print_header("Final Results")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name} Test PASSED")
        else:
            print_error(f"{test_name} Test FAILED")
    
    print(f"\n📊 Overall Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! AION is ready for GitHub publication!")
        print("\n🚀 Next steps:")
        print("   1. git init && git add . && git commit -m 'Initial AION release'")
        print("   2. Create GitHub repository")
        print("   3. git remote add origin <your-repo-url>")
        print("   4. git push -u origin main")
        print("   5. Create release v1.0.0 on GitHub")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please fix issues before publication.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
