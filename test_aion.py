#!/usr/bin/env python3
"""
🧪 AION Test Suite
Test script to verify AION functionality
"""

import os
import sys
import json
import asyncio
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        # Core modules
        from core.security import SecurityManager
        from core.ai_providers import AIManager
        from core.executor import CodeExecutor
        from core.plugins import PluginManager
        print("✅ Core modules imported successfully")
        
        # Interface modules
        from interfaces.cli import CLIInterface
        from interfaces.tui import TUIInterface
        from interfaces.web import WebInterface
        print("✅ Interface modules imported successfully")
        
        # Utility modules
        from utils.translator import Translator
        from utils.helpers import create_directories, load_config
        print("✅ Utility modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_translator():
    """Test translator functionality"""
    print("\n🌐 Testing translator...")
    
    try:
        from utils.translator import Translator
        
        translator = Translator()
        
        # Test language switching
        translator.set_language("en")
        welcome_en = translator.get("welcome")
        print(f"English: {welcome_en}")
        
        translator.set_language("ar")
        welcome_ar = translator.get("welcome")
        print(f"Arabic: {welcome_ar}")
        
        translator.set_language("es")
        welcome_es = translator.get("welcome")
        print(f"Spanish: {welcome_es}")
        
        print("✅ Translator working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Translator error: {e}")
        return False

def test_security():
    """Test security manager"""
    print("\n🔒 Testing security manager...")
    
    try:
        from core.security import SecurityManager
        
        security = SecurityManager()
        
        # Test token generation
        token = security.generate_session_token()
        print(f"Generated token: {token[:20]}...")
        
        # Test command filtering
        safe_command = "ls -la"
        dangerous_command = "rm -rf /"
        
        is_safe = security.is_command_safe(safe_command)
        is_dangerous = security.is_command_safe(dangerous_command)
        
        print(f"'{safe_command}' is safe: {is_safe}")
        print(f"'{dangerous_command}' is safe: {is_dangerous}")
        
        if is_safe and not is_dangerous:
            print("✅ Security manager working correctly")
            return True
        else:
            print("❌ Security manager not filtering correctly")
            return False
        
    except Exception as e:
        print(f"❌ Security manager error: {e}")
        return False

async def test_ai_providers():
    """Test AI providers (without actual API calls)"""
    print("\n🤖 Testing AI providers...")
    
    try:
        from core.ai_providers import AIManager
        
        ai_manager = AIManager()
        
        # Test provider initialization
        providers = ai_manager.get_available_providers()
        print(f"Available providers: {providers}")
        
        # Test provider switching
        for provider in providers:
            ai_manager.set_provider(provider)
            current = ai_manager.get_current_provider()
            print(f"Switched to: {current}")
        
        print("✅ AI providers manager working correctly")
        return True
        
    except Exception as e:
        print(f"❌ AI providers error: {e}")
        return False

async def test_code_executor():
    """Test code executor"""
    print("\n💻 Testing code executor...")
    
    try:
        from core.executor import CodeExecutor
        
        executor = CodeExecutor()
        
        # Test Python code execution
        python_code = "print('Hello from AION!')"
        result = await executor.execute_code(python_code, "python")
        
        print(f"Python execution result: {result}")

        if hasattr(result, 'success') and result.success and "Hello from AION!" in (result.output or ""):
            print("✅ Code executor working correctly")
            return True
        else:
            print("❌ Code executor not working correctly")
            return False
        
    except Exception as e:
        print(f"❌ Code executor error: {e}")
        return False

async def test_plugins():
    """Test plugin manager"""
    print("\n🧩 Testing plugin manager...")
    
    try:
        from core.plugins import PluginManager
        
        plugin_manager = PluginManager()
        
        # Discover plugins
        await plugin_manager.discover_plugins()
        
        # Get plugin list
        plugins = plugin_manager.get_plugins()
        print(f"Discovered {len(plugins)} plugins")
        
        for plugin in plugins:
            print(f"  - {plugin.name} v{plugin.version}")
        
        print("✅ Plugin manager working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Plugin manager error: {e}")
        return False

def test_config_files():
    """Test configuration files"""
    print("\n📋 Testing configuration files...")
    
    try:
        # Test AI config template
        ai_config_path = Path("config/ai_config_template.json")
        if ai_config_path.exists():
            with open(ai_config_path, 'r') as f:
                ai_config = json.load(f)
            print(f"✅ AI config template loaded: {len(ai_config)} providers")
        else:
            print("❌ AI config template not found")
            return False
        
        # Test security config template
        security_config_path = Path("config/security_config_template.json")
        if security_config_path.exists():
            with open(security_config_path, 'r') as f:
                security_config = json.load(f)
            print(f"✅ Security config template loaded: {len(security_config)} sections")
        else:
            print("❌ Security config template not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Config files error: {e}")
        return False

def test_translation_files():
    """Test translation files"""
    print("\n🌍 Testing translation files...")
    
    try:
        locales_dir = Path("locales")
        if not locales_dir.exists():
            print("❌ Locales directory not found")
            return False
        
        languages = ["ar", "en", "no", "de", "fr", "zh", "es"]
        
        for lang in languages:
            lang_file = locales_dir / f"{lang}.json"
            if lang_file.exists():
                with open(lang_file, 'r', encoding='utf-8') as f:
                    translations = json.load(f)
                print(f"✅ {lang}.json loaded: {len(translations)} translations")
            else:
                print(f"❌ {lang}.json not found")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Translation files error: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        "typer", "rich", "textual", "fastapi", "uvicorn",
        "httpx", "jinja2", "python_multipart"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            # Handle special case for python-multipart
            if package == "python_multipart":
                import python_multipart
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run 'pip install -r requirements.txt' to install missing packages")
        return False
    
    print("✅ All dependencies are installed")
    return True

async def run_all_tests():
    """Run all tests"""
    print("🧪 AION Test Suite")
    print("=" * 50)
    
    tests = [
        ("Dependencies", check_dependencies),
        ("Imports", test_imports),
        ("Config Files", test_config_files),
        ("Translation Files", test_translation_files),
        ("Translator", test_translator),
        ("Security Manager", test_security),
        ("AI Providers", test_ai_providers),
        ("Code Executor", test_code_executor),
        ("Plugin Manager", test_plugins)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {e}")
    
    print(f"\n{'='*50}")
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! AION is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

def main():
    """Main function"""
    try:
        result = asyncio.run(run_all_tests())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n👋 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
