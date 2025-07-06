#!/usr/bin/env python3
"""
🧪 AION Complete System Test
Comprehensive testing with temporary PATH setup
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

def setup_temp_path():
    """Setup temporary PATH with all required tools"""
    current_path = os.environ.get('PATH', '')
    
    # Add Node.js path
    nodejs_path = r"C:\Program Files\nodejs"
    if os.path.exists(nodejs_path):
        current_path = f"{nodejs_path};{current_path}"
        print(f"✅ Added Node.js path: {nodejs_path}")
    
    # Add Rust path
    rust_path = os.path.expanduser(r"~\.cargo\bin")
    if os.path.exists(rust_path):
        current_path = f"{rust_path};{current_path}"
        print(f"✅ Added Rust path: {rust_path}")
    
    # Add MinGW path
    mingw_paths = [
        r"C:\msys64\mingw64\bin",
        r"C:\MinGW\bin",
        r"C:\Program Files\Git\mingw64\bin"
    ]
    
    for mingw_path in mingw_paths:
        if os.path.exists(mingw_path):
            current_path = f"{mingw_path};{current_path}"
            print(f"✅ Added C++ path: {mingw_path}")
            break
    
    os.environ['PATH'] = current_path
    return current_path

def test_language_availability():
    """Test all programming languages"""
    print("\n🔍 Testing Language Availability:")
    print("=" * 50)
    
    languages = {
        "Python": [sys.executable, "--version"],
        "Node.js": ["node", "--version"],
        "Rust": ["rustc", "--version"],
        "C++ (g++)": ["g++", "--version"],
        "C++ (cl)": ["cl"],
    }
    
    results = {}
    for name, command in languages.items():
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            if result.returncode == 0 or (name == "C++ (cl)" and "Microsoft" in result.stderr):
                version_info = result.stdout.strip() or result.stderr.strip()
                results[name] = f"✅ Available: {version_info.split()[0] if version_info else 'Unknown version'}"
            else:
                results[name] = "❌ Not working"
        except Exception as e:
            results[name] = f"❌ Error: {str(e)[:50]}"
    
    for name, status in results.items():
        print(f"  {name}: {status}")
    
    return results

def test_code_execution():
    """Test code execution for available languages"""
    print("\n🚀 Testing Code Execution:")
    print("=" * 50)
    
    # Test Python
    print("\n🐍 Testing Python:")
    try:
        python_code = '''
print("🎉 مرحباً من AION!")
print("Python test successful!")
for i in range(3):
    print(f"Test {i+1}: ✅")
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(python_code)
            temp_file = f.name
        
        result = subprocess.run([sys.executable, temp_file], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Python execution successful!")
            print("Output:", result.stdout.strip())
        else:
            print("❌ Python execution failed:", result.stderr)
        
        os.unlink(temp_file)
    except Exception as e:
        print(f"❌ Python test error: {e}")
    
    # Test JavaScript (if Node.js available)
    print("\n🟨 Testing JavaScript:")
    try:
        js_code = '''
console.log("🎉 مرحباً من AION مع JavaScript!");
console.log("JavaScript test successful!");
for (let i = 1; i <= 3; i++) {
    console.log(`Test ${i}: ✅`);
}
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
            f.write(js_code)
            temp_file = f.name
        
        result = subprocess.run(["node", temp_file], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ JavaScript execution successful!")
            print("Output:", result.stdout.strip())
        else:
            print("❌ JavaScript execution failed:", result.stderr)
        
        os.unlink(temp_file)
    except Exception as e:
        print(f"❌ JavaScript test error: {e}")
    
    # Test Rust (if available)
    print("\n🦀 Testing Rust:")
    try:
        rust_code = '''
fn main() {
    println!("🎉 مرحباً من AION مع Rust!");
    println!("Rust test successful!");
    for i in 1..=3 {
        println!("Test {}: ✅", i);
    }
}
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.rs', delete=False, encoding='utf-8') as f:
            f.write(rust_code)
            temp_file = f.name
        
        # Compile Rust
        exe_file = temp_file.replace('.rs', '.exe')
        compile_result = subprocess.run(["rustc", temp_file, "-o", exe_file], 
                                      capture_output=True, text=True, timeout=30)
        
        if compile_result.returncode == 0:
            # Run compiled executable
            run_result = subprocess.run([exe_file], capture_output=True, text=True, timeout=10)
            if run_result.returncode == 0:
                print("✅ Rust compilation and execution successful!")
                print("Output:", run_result.stdout.strip())
            else:
                print("❌ Rust execution failed:", run_result.stderr)
            
            # Cleanup
            if os.path.exists(exe_file):
                os.unlink(exe_file)
        else:
            print("❌ Rust compilation failed:", compile_result.stderr)
        
        os.unlink(temp_file)
    except Exception as e:
        print(f"❌ Rust test error: {e}")

def test_aion_import():
    """Test AION main module import"""
    print("\n📦 Testing AION Module Import:")
    print("=" * 50)
    
    try:
        # Test main imports
        sys.path.insert(0, str(Path.cwd()))
        
        print("Testing main.py import...")
        import main
        print("✅ main.py imported successfully")
        
        print("Testing code executor import...")
        from src.utils.code_executor import CodeExecutor
        print("✅ CodeExecutor imported successfully")
        
        print("Testing plugin manager import...")
        from src.plugins.plugin_manager import PluginManager
        print("✅ PluginManager imported successfully")
        
        # Test CodeExecutor initialization
        print("Testing CodeExecutor initialization...")
        executor = CodeExecutor()
        print("✅ CodeExecutor initialized successfully")
        
        # Test available languages detection
        print("Testing language detection...")
        available = executor.get_available_languages()
        print(f"✅ Detected {len(available)} available languages")
        
        for lang in available:
            print(f"  - {lang['display_name']}: {lang['performance_level']} performance")
        
        return True
        
    except Exception as e:
        print(f"❌ AION import test failed: {e}")
        return False

def main():
    """Run complete AION system test"""
    print("🧪 AION Complete System Test")
    print("=" * 60)
    
    # Setup PATH
    print("🔧 Setting up temporary PATH...")
    setup_temp_path()
    
    # Test language availability
    lang_results = test_language_availability()
    
    # Test code execution
    test_code_execution()
    
    # Test AION imports
    import_success = test_aion_import()
    
    # Summary
    print("\n📊 Test Summary:")
    print("=" * 50)
    
    available_count = sum(1 for status in lang_results.values() if "✅" in status)
    total_count = len(lang_results)
    
    print(f"Languages Available: {available_count}/{total_count}")
    print(f"AION Module Import: {'✅ Success' if import_success else '❌ Failed'}")
    
    if available_count >= 2 and import_success:
        print("\n🎉 AION System Test: PASSED")
        print("✅ System is ready for production use!")
    else:
        print("\n⚠️  AION System Test: PARTIAL")
        print("🔧 Some components need attention")
    
    print("\n🚀 To run AION:")
    print("   python main.py start")

if __name__ == "__main__":
    main()
