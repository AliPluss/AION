#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 AION Final System Test
Comprehensive final testing of all components
"""

import os
import sys
import json
import subprocess
import tempfile
from pathlib import Path

# Setup PATH for testing
def setup_test_environment():
    """Setup test environment with all required paths"""
    current_path = os.environ.get('PATH', '')
    
    paths_to_add = [
        r"C:\Program Files\nodejs",
        os.path.expanduser(r"~\.cargo\bin"),
        r"C:\msys64\mingw64\bin",
        r"C:\MinGW\bin"
    ]
    
    for path in paths_to_add:
        if os.path.exists(path) and path not in current_path:
            current_path = f"{path};{current_path}"
    
    os.environ['PATH'] = current_path
    os.environ['PYTHONIOENCODING'] = 'utf-8'

class FinalSystemTester:
    """Comprehensive system tester"""
    
    def __init__(self):
        self.results = {}
        self.total_tests = 0
        self.passed_tests = 0
        
    def run_test(self, test_name: str, test_func):
        """Run a test and record results"""
        print(f"\n🧪 {test_name}")
        print("-" * 50)
        
        try:
            result = test_func()
            self.results[test_name] = result
            if result:
                self.passed_tests += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            self.results[test_name] = False
            print(f"💥 {test_name}: CRASHED - {e}")
        
        self.total_tests += 1
    
    def test_core_imports(self):
        """Test all core module imports"""
        try:
            # Test main imports
            import main
            from src.utils.code_executor import CodeExecutor
            from src.plugins.plugin_manager import PluginManager
            
            # Test new security modules
            from src.utils.input_validator import validator
            from src.utils.secure_temp import secure_temp
            
            print("✅ All core modules imported successfully")
            return True
            
        except Exception as e:
            print(f"❌ Import failed: {e}")
            return False
    
    def test_configuration_files(self):
        """Test all configuration files"""
        config_files = [
            "config/config.json",
            "config/lang_ar.json", 
            "config/lang_en.json",
            "config/security.json"
        ]
        
        all_valid = True
        for config_file in config_files:
            try:
                if Path(config_file).exists():
                    with open(config_file, "r", encoding="utf-8") as f:
                        json.load(f)
                    print(f"✅ {config_file}: Valid JSON")
                else:
                    print(f"⚠️  {config_file}: Missing")
                    all_valid = False
            except Exception as e:
                print(f"❌ {config_file}: Invalid - {e}")
                all_valid = False
        
        return all_valid
    
    def test_language_detection(self):
        """Test programming language detection"""
        try:
            from src.utils.code_executor import CodeExecutor
            executor = CodeExecutor()
            
            available_languages = executor.get_available_languages()
            print(f"✅ Detected {len(available_languages)} languages:")
            
            for lang in available_languages:
                print(f"  - {lang['display_name']}: {lang['performance_level']} performance")
            
            # Should have at least Python
            return len(available_languages) >= 1
            
        except Exception as e:
            print(f"❌ Language detection failed: {e}")
            return False
    
    def test_security_features(self):
        """Test security features"""
        try:
            from src.utils.input_validator import validator
            from src.utils.secure_temp import secure_temp
            
            # Test input validation
            test_code = "print('Hello World')"
            validated = validator.validate_code_input(test_code)
            print("✅ Input validation working")
            
            # Test secure temp file
            if secure_temp:
                temp_file = secure_temp.create_temp_file(content="test")
                print(f"✅ Secure temp file created: {temp_file}")
                secure_temp.cleanup_file(temp_file)
                print("✅ Secure temp file cleaned up")
            
            return True
            
        except Exception as e:
            print(f"❌ Security features test failed: {e}")
            return False
    
    def test_plugin_system(self):
        """Test plugin system"""
        try:
            from src.plugins.plugin_manager import PluginManager
            
            plugin_manager = PluginManager()
            plugins = plugin_manager.discover_plugins()
            
            print(f"✅ Discovered {len(plugins)} plugins:")
            for plugin in plugins:
                print(f"  - {plugin}")
            
            return len(plugins) > 0
            
        except Exception as e:
            print(f"❌ Plugin system test failed: {e}")
            return False
    
    def test_arabic_support(self):
        """Test Arabic language support"""
        try:
            # Test Arabic text handling
            arabic_text = "مرحباً بك في AION"
            
            # Test encoding/decoding
            encoded = arabic_text.encode('utf-8')
            decoded = encoded.decode('utf-8')
            
            if arabic_text == decoded:
                print("✅ Arabic encoding/decoding working")
            else:
                print("❌ Arabic encoding/decoding failed")
                return False
            
            # Test config file Arabic content
            with open("config/lang_ar.json", "r", encoding="utf-8") as f:
                lang_data = json.load(f)
            
            arabic_entries = sum(1 for v in lang_data.values() 
                               if isinstance(v, str) and any('\u0600' <= c <= '\u06FF' for c in v))
            
            print(f"✅ Found {arabic_entries} Arabic entries in language file")
            
            return arabic_entries > 0
            
        except Exception as e:
            print(f"❌ Arabic support test failed: {e}")
            return False
    
    def test_code_execution_basic(self):
        """Test basic code execution"""
        try:
            # Test Python code execution
            python_code = '''
print("AION Test")
result = 2 + 2
print(f"2 + 2 = {result}")
'''
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(python_code)
                temp_file = f.name
            
            result = subprocess.run([sys.executable, temp_file], 
                                  capture_output=True, text=True, timeout=10)
            
            os.unlink(temp_file)
            
            if result.returncode == 0 and "AION Test" in result.stdout:
                print("✅ Python code execution working")
                return True
            else:
                print(f"❌ Python code execution failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Code execution test failed: {e}")
            return False
    
    def test_file_structure(self):
        """Test complete file structure"""
        required_files = [
            "main.py",
            "requirements.txt",
            "README.md",
            "config/config.json",
            "config/lang_ar.json",
            "src/utils/code_executor.py",
            "src/plugins/plugin_manager.py",
            "src/utils/input_validator.py",
            "src/utils/secure_temp.py"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            print(f"❌ Missing files: {', '.join(missing_files)}")
            return False
        else:
            print(f"✅ All {len(required_files)} required files present")
            return True
    
    def test_dependencies(self):
        """Test Python dependencies"""
        try:
            import rich
            import typer
            print("✅ Core dependencies available")
            
            # Test Rich console
            from rich.console import Console
            console = Console()
            console.print("✅ Rich console working", style="green")
            
            return True
            
        except ImportError as e:
            print(f"❌ Missing dependency: {e}")
            return False
    
    def generate_final_report(self):
        """Generate comprehensive final report"""
        print("\n" + "="*80)
        print("🎯 AION FINAL SYSTEM TEST REPORT")
        print("="*80)
        
        print(f"\n📊 TEST RESULTS:")
        print(f"  Total Tests: {self.total_tests}")
        print(f"  Passed: {self.passed_tests}")
        print(f"  Failed: {self.total_tests - self.passed_tests}")
        print(f"  Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        print(f"\n📋 DETAILED RESULTS:")
        for test_name, result in self.results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {test_name}: {status}")
        
        # Overall assessment
        success_rate = (self.passed_tests / self.total_tests) * 100
        
        if success_rate >= 95:
            print(f"\n🎉 OVERALL STATUS: EXCELLENT ({success_rate:.1f}%)")
            print("✅ AION system is ready for production use!")
            print("🚀 All critical components working perfectly")
        elif success_rate >= 85:
            print(f"\n✅ OVERALL STATUS: GOOD ({success_rate:.1f}%)")
            print("🔧 Minor issues detected, system mostly functional")
        elif success_rate >= 70:
            print(f"\n⚠️  OVERALL STATUS: ACCEPTABLE ({success_rate:.1f}%)")
            print("🔧 Several issues need attention")
        else:
            print(f"\n❌ OVERALL STATUS: NEEDS WORK ({success_rate:.1f}%)")
            print("🔧 Major issues require immediate attention")
        
        print(f"\n🎯 NEXT STEPS:")
        if success_rate >= 95:
            print("  1. ✅ System ready for use")
            print("  2. 🚀 Run: python main.py start")
            print("  3. 🎉 Enjoy AION!")
        else:
            failed_tests = [name for name, result in self.results.items() if not result]
            print("  1. 🔧 Fix failed tests:")
            for test in failed_tests[:3]:  # Show first 3 failed tests
                print(f"     - {test}")
            print("  2. 🔄 Re-run final test")
            print("  3. 🚀 Launch when ready")
        
        return success_rate >= 85

def main():
    """Run comprehensive final system test"""
    print("🎯 AION FINAL SYSTEM TEST")
    print("="*80)
    print("🔧 Setting up test environment...")
    
    setup_test_environment()
    
    tester = FinalSystemTester()
    
    # Run all tests
    test_suite = [
        ("Core Module Imports", tester.test_core_imports),
        ("Configuration Files", tester.test_configuration_files),
        ("File Structure", tester.test_file_structure),
        ("Dependencies", tester.test_dependencies),
        ("Language Detection", tester.test_language_detection),
        ("Security Features", tester.test_security_features),
        ("Plugin System", tester.test_plugin_system),
        ("Arabic Support", tester.test_arabic_support),
        ("Code Execution", tester.test_code_execution_basic)
    ]
    
    for test_name, test_func in test_suite:
        tester.run_test(test_name, test_func)
    
    # Generate final report
    system_ready = tester.generate_final_report()
    
    return system_ready

if __name__ == "__main__":
    main()
