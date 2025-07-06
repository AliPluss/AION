#!/usr/bin/env python3
"""
Advanced Installation Checker for AION
Checks common installation paths and provides detailed guidance
"""

import os
import subprocess
import sys
from pathlib import Path

def check_path_command(command):
    """Check if command is in PATH"""
    try:
        result = subprocess.run([command, '--version'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stdout.strip()
    except:
        return False, ""

def check_file_exists(path):
    """Check if file exists at given path"""
    return Path(path).exists()

def find_installations():
    """Find installations in common paths"""
    print("🔍 البحث في المسارات الشائعة | Searching common paths...")
    print("=" * 60)
    
    # Node.js common paths
    node_paths = [
        r"C:\Program Files\nodejs\node.exe",
        r"C:\Program Files (x86)\nodejs\node.exe",
        os.path.expanduser(r"~\AppData\Roaming\npm\node.exe"),
        r"C:\nodejs\node.exe"
    ]
    
    print("🟨 Node.js:")
    node_found = False
    for path in node_paths:
        if check_file_exists(path):
            print(f"   ✅ Found: {path}")
            node_found = True
            # Try to get version
            try:
                result = subprocess.run([path, '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"      Version: {result.stdout.strip()}")
            except:
                pass
    
    if not node_found:
        print("   ❌ Not found in common paths")
    
    print()
    
    # Rust common paths
    rust_paths = [
        os.path.expanduser(r"~\.cargo\bin\rustc.exe"),
        r"C:\Users\%USERNAME%\.cargo\bin\rustc.exe",
        r"C:\rust\bin\rustc.exe"
    ]
    
    print("🦀 Rust:")
    rust_found = False
    for path in rust_paths:
        expanded_path = os.path.expandvars(path)
        if check_file_exists(expanded_path):
            print(f"   ✅ Found: {expanded_path}")
            rust_found = True
            # Try to get version
            try:
                result = subprocess.run([expanded_path, '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"      Version: {result.stdout.strip()}")
            except:
                pass
    
    if not rust_found:
        print("   ❌ Not found in common paths")
    
    print()
    
    # C++ common paths
    cpp_paths = [
        r"C:\msys64\mingw64\bin\g++.exe",
        r"C:\MinGW\bin\g++.exe",
        r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\*\bin\Hostx64\x64\cl.exe",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Tools\MSVC\*\bin\Hostx64\x64\cl.exe"
    ]
    
    print("⚡ C++:")
    cpp_found = False
    for path in cpp_paths:
        if '*' in path:
            # Handle wildcard paths
            import glob
            matches = glob.glob(path)
            if matches:
                for match in matches:
                    if check_file_exists(match):
                        print(f"   ✅ Found: {match}")
                        cpp_found = True
                        break
        else:
            if check_file_exists(path):
                print(f"   ✅ Found: {path}")
                cpp_found = True
                # Try to get version
                try:
                    if 'g++' in path:
                        result = subprocess.run([path, '--version'], capture_output=True, text=True, timeout=5)
                    else:  # cl.exe
                        result = subprocess.run([path], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0 or result.stderr:
                        version_info = result.stdout.strip() or result.stderr.strip()
                        print(f"      Version: {version_info.split()[0] if version_info else 'Unknown'}")
                except:
                    pass
    
    if not cpp_found:
        print("   ❌ Not found in common paths")
    
    return node_found, rust_found, cpp_found

def check_environment_variables():
    """Check PATH environment variable"""
    print("\n🔧 فحص متغيرات البيئة | Checking Environment Variables")
    print("=" * 60)
    
    path_var = os.environ.get('PATH', '')
    paths = path_var.split(os.pathsep)
    
    relevant_paths = []
    for path in paths:
        path_lower = path.lower()
        if any(keyword in path_lower for keyword in ['node', 'rust', 'cargo', 'mingw', 'msys', 'gcc', 'visual studio']):
            relevant_paths.append(path)
    
    if relevant_paths:
        print("📁 مسارات ذات صلة في PATH | Relevant paths in PATH:")
        for path in relevant_paths:
            print(f"   • {path}")
    else:
        print("⚠️  لم يتم العثور على مسارات ذات صلة في PATH")
        print("   This might be why the commands are not recognized")

def provide_solutions():
    """Provide solutions for common issues"""
    print("\n💡 الحلول المقترحة | Suggested Solutions")
    print("=" * 60)
    
    print("1. 🔄 إعادة تشغيل Terminal | Restart Terminal:")
    print("   • Close this terminal completely")
    print("   • Open a new terminal/command prompt")
    print("   • Run: python check_installations.py")
    print()
    
    print("2. 🔧 إضافة إلى PATH يدوياً | Add to PATH manually:")
    print("   • Press Win + R, type 'sysdm.cpl'")
    print("   • Go to Advanced → Environment Variables")
    print("   • Edit PATH and add these if they exist:")
    print("     - C:\\Program Files\\nodejs")
    print("     - %USERPROFILE%\\.cargo\\bin")
    print("     - C:\\msys64\\mingw64\\bin")
    print()
    
    print("3. 🔍 التحقق من التثبيت | Verify Installation:")
    print("   • Node.js: Check if installed in Programs & Features")
    print("   • Rust: Look for .cargo folder in your user directory")
    print("   • C++: Check if MSYS2 or Visual Studio is installed")

def main():
    print("🔍 فاحص التثبيتات المتقدم | Advanced Installation Checker")
    print("=" * 60)
    print()
    
    # Check PATH first
    print("1️⃣ فحص PATH | Checking PATH commands:")
    node_in_path, node_version = check_path_command("node")
    rust_in_path, rust_version = check_path_command("rustc")
    cpp_in_path, cpp_version = check_path_command("g++")
    
    print(f"   🟨 Node.js: {'✅' if node_in_path else '❌'} {node_version if node_in_path else 'Not in PATH'}")
    print(f"   🦀 Rust: {'✅' if rust_in_path else '❌'} {rust_version if rust_in_path else 'Not in PATH'}")
    print(f"   ⚡ C++: {'✅' if cpp_in_path else '❌'} {cpp_version if cpp_in_path else 'Not in PATH'}")
    print()
    
    # If not in PATH, search for installations
    if not all([node_in_path, rust_in_path, cpp_in_path]):
        print("2️⃣ البحث في المسارات | Searching file system:")
        node_found, rust_found, cpp_found = find_installations()
        
        check_environment_variables()
        provide_solutions()
        
        print(f"\n📊 ملخص النتائج | Results Summary:")
        print(f"   🟨 Node.js: {'✅ Installed' if node_found or node_in_path else '❌ Not Found'}")
        print(f"   🦀 Rust: {'✅ Installed' if rust_found or rust_in_path else '❌ Not Found'}")
        print(f"   ⚡ C++: {'✅ Installed' if cpp_found or cpp_in_path else '❌ Not Found'}")
        
        if any([node_found, rust_found, cpp_found]) and not all([node_in_path, rust_in_path, cpp_in_path]):
            print("\n⚠️  بعض البرامج مثبتة لكن غير مضافة إلى PATH")
            print("   Some programs are installed but not in PATH")
            print("   Please restart your terminal or add them to PATH manually")
    else:
        print("🎉 جميع البرامج مثبتة وتعمل بشكل صحيح!")
        print("   All programs are installed and working correctly!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nتم الإلغاء | Cancelled")
    except Exception as e:
        print(f"\nخطأ | Error: {e}")
