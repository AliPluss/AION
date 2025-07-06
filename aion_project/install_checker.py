#!/usr/bin/env python3
"""
AION Dependencies Installation Checker
Checks and guides installation of required programming languages
"""

import subprocess
import sys
import os
import webbrowser
from pathlib import Path

def check_command(command):
    """Check if a command is available in the system"""
    try:
        result = subprocess.run([command, '--version'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        return False, ""

def print_status(name, installed, version="", icon=""):
    """Print installation status with colors"""
    status_icon = "✅" if installed else "❌"
    status_text = "Installed" if installed else "Not Installed"
    
    print(f"{status_icon} {icon} {name}: {status_text}")
    if installed and version:
        print(f"    Version: {version.split()[0] if version else 'Unknown'}")

def open_download_pages():
    """Open download pages for missing dependencies"""
    print("\n🌐 Opening download pages...")
    
    urls = [
        "https://nodejs.org/en/download",
        "https://rustup.rs/",
        "https://www.msys2.org/"
    ]
    
    for url in urls:
        try:
            webbrowser.open(url)
            print(f"   Opened: {url}")
        except Exception as e:
            print(f"   Failed to open: {url} - {e}")

def main():
    print("=" * 50)
    print("🤖 AION Dependencies Installation Checker")
    print("=" * 50)
    print()
    
    # Check Python (should be available)
    python_installed, python_version = check_command("python")
    print_status("Python", python_installed, python_version, "🐍")
    
    # Check Node.js
    node_installed, node_version = check_command("node")
    print_status("Node.js", node_installed, node_version, "🟨")
    
    # Check Rust
    rust_installed, rust_version = check_command("rustc")
    print_status("Rust", rust_installed, rust_version, "🦀")
    
    # Check C++
    cpp_installed, cpp_version = check_command("g++")
    print_status("C++", cpp_installed, cpp_version, "⚡")
    
    print()
    print("=" * 50)
    
    # Count missing dependencies
    missing = []
    if not node_installed:
        missing.append("Node.js")
    if not rust_installed:
        missing.append("Rust")
    if not cpp_installed:
        missing.append("C++")
    
    if not missing:
        print("🎉 All dependencies are installed!")
        print("You can now run: python main.py start")
        print("All 4 programming languages will be available in AION!")
    else:
        print(f"⚠️  Missing dependencies: {', '.join(missing)}")
        print()
        print("📋 Installation Instructions:")
        print()
        
        if "Node.js" in missing:
            print("1. 🟨 Node.js (JavaScript support):")
            print("   • Go to: https://nodejs.org/en/download")
            print("   • Download LTS version for Windows")
            print("   • Run installer with default settings")
            print()
        
        if "Rust" in missing:
            print("2. 🦀 Rust (High performance):")
            print("   • Go to: https://rustup.rs/")
            print("   • Download rustup-init.exe")
            print("   • Run and choose default installation")
            print()
        
        if "C++" in missing:
            print("3. ⚡ C++ (High performance):")
            print("   • Go to: https://www.msys2.org/")
            print("   • Download and install MSYS2")
            print("   • Open MSYS2 terminal and run:")
            print("     pacman -Syu")
            print("     pacman -S mingw-w64-x86_64-gcc")
            print("   • Add C:\\msys64\\mingw64\\bin to PATH")
            print()
        
        print("🔄 After installation:")
        print("1. Restart your terminal")
        print("2. Run: python install_checker.py (to verify)")
        print("3. Run: python main.py start")
        print()
        
        # Ask if user wants to open download pages
        try:
            response = input("🌐 Open download pages in browser? (y/n): ").lower().strip()
            if response in ['y', 'yes', 'نعم', '']:
                open_download_pages()
        except KeyboardInterrupt:
            print("\n\nInstallation cancelled.")
    
    print()
    print("=" * 50)
    print("🚀 AION will support all installed languages!")
    print("Current support:")
    print(f"   🐍 Python: {'✅' if python_installed else '❌'}")
    print(f"   🟨 JavaScript: {'✅' if node_installed else '❌'}")
    print(f"   🦀 Rust: {'✅' if rust_installed else '❌'}")
    print(f"   ⚡ C++: {'✅' if cpp_installed else '❌'}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
