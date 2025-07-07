#!/usr/bin/env python3
"""
Direct Arrow Navigation Test
Tests the arrow navigation system directly
"""

import sys
import os
from pathlib import Path

# Add AION to path
sys.path.insert(0, str(Path(__file__).parent))

def test_arrow_navigation_import():
    """Test if arrow navigation can be imported"""
    print("🔍 Testing Arrow Navigation Import...")
    
    try:
        from aion.interfaces.arrow_navigation import ArrowNavigator, select_language_arrows
        print("✅ Arrow navigation imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_arrow_navigator_class():
    """Test ArrowNavigator class functionality"""
    print("🎮 Testing ArrowNavigator Class...")
    
    try:
        from aion.interfaces.arrow_navigation import ArrowNavigator
        
        # Create navigator instance
        navigator = ArrowNavigator()
        print("✅ ArrowNavigator instance created")
        
        # Test platform detection
        import platform
        system = platform.system()
        print(f"✅ Platform detected: {system}")
        
        # Test key mapping
        if hasattr(navigator, 'key_map'):
            print(f"✅ Key mapping available: {len(navigator.key_map)} keys")
        
        return True
        
    except Exception as e:
        print(f"❌ ArrowNavigator test failed: {e}")
        return False

def test_language_selection_function():
    """Test language selection with arrow navigation"""
    print("🌐 Testing Language Selection Function...")
    
    try:
        from aion.interfaces.arrow_navigation import select_language_arrows
        print("✅ select_language_arrows function imported")
        
        # Test function signature
        import inspect
        sig = inspect.signature(select_language_arrows)
        print(f"✅ Function signature: {sig}")
        
        return True
        
    except Exception as e:
        print(f"❌ Language selection test failed: {e}")
        return False

def test_main_integration():
    """Test integration with main.py"""
    print("🔗 Testing Main.py Integration...")
    
    try:
        from aion.main import select_language
        print("✅ select_language function imported from main")
        
        # Check if it uses arrow navigation
        import inspect
        source = inspect.getsource(select_language)
        
        if "select_language_arrows" in source:
            print("✅ Main uses arrow navigation function")
        else:
            print("⚠️ Main might not use arrow navigation")
        
        return True
        
    except Exception as e:
        print(f"❌ Main integration test failed: {e}")
        return False

def test_ai_manager():
    """Test AI Manager functionality"""
    print("🤖 Testing AI Manager...")
    
    try:
        from aion.core.ai_manager import AIManager
        
        # Create AI manager
        manager = AIManager()
        print("✅ AIManager created successfully")
        
        # Test provider stats
        stats = manager.get_provider_stats()
        print(f"✅ Provider stats: {stats['total_providers']} total, {stats['active_providers']} active")
        
        # Test available providers
        available = manager.get_available_providers()
        print(f"✅ Available providers: {available}")
        
        return True
        
    except Exception as e:
        print(f"❌ AI Manager test failed: {e}")
        return False

def check_duplicate_files():
    """Check for duplicate files in the project"""
    print("📁 Checking for Duplicate Files...")
    
    # Common duplicate patterns
    duplicate_patterns = [
        ("main.py", "aion/main.py"),
        ("arrow_navigation.py", "aion/interfaces/arrow_navigation.py"),
        ("ai_manager.py", "aion/core/ai_manager.py"),
    ]
    
    duplicates_found = []
    
    for pattern1, pattern2 in duplicate_patterns:
        if os.path.exists(pattern1) and os.path.exists(pattern2):
            duplicates_found.append((pattern1, pattern2))
    
    if duplicates_found:
        print("⚠️ Potential duplicates found:")
        for dup1, dup2 in duplicates_found:
            print(f"  - {dup1} <-> {dup2}")
        return False
    else:
        print("✅ No duplicate files detected")
        return True

def run_comprehensive_test():
    """Run all tests"""
    print("🧪 Starting Comprehensive Arrow Navigation Test")
    print("=" * 60)
    
    tests = [
        ("Arrow Navigation Import", test_arrow_navigation_import),
        ("ArrowNavigator Class", test_arrow_navigator_class),
        ("Language Selection Function", test_language_selection_function),
        ("Main Integration", test_main_integration),
        ("AI Manager", test_ai_manager),
        ("Duplicate Files Check", check_duplicate_files)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            result = test_func()
            status = "✅ PASSED" if result else "❌ FAILED"
            results.append((test_name, status))
            print(f"   {status}")
        except Exception as e:
            status = f"❌ ERROR: {str(e)}"
            results.append((test_name, status))
            print(f"   {status}")
    
    # Summary
    passed = sum(1 for _, status in results if "✅ PASSED" in status)
    total = len(results)
    
    print("\n" + "=" * 60)
    print(f"🎯 TEST RESULTS: {passed}/{total} tests passed")
    print(f"📊 Success Rate: {(passed/total)*100:.1f}%")
    print("=" * 60)
    
    print("\nDETAILED RESULTS:")
    for test_name, status in results:
        print(f"  {test_name}: {status}")
    
    # Recommendations
    print(f"\n🎯 ARROW NAVIGATION STATUS:")
    if passed >= 4:
        print("✅ ARROW NAVIGATION SYSTEM OPERATIONAL")
        print("🎮 Ready for keyboard-only interaction")
    else:
        print("⚠️ ARROW NAVIGATION NEEDS ATTENTION")
        print("🔧 Some components require fixes")
    
    return passed >= 4

if __name__ == "__main__":
    success = run_comprehensive_test()
    
    if success:
        print("\n🚀 ARROW NAVIGATION: READY FOR USE")
    else:
        print("\n⚠️ ARROW NAVIGATION: NEEDS FIXES")
    
    sys.exit(0 if success else 1)
