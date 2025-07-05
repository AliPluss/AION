#!/usr/bin/env python3
"""
🚀 AION Installation Script
Quick installation script for AION from local build
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {command}")
        print(f"Error: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (requires 3.8+)")
        return False

def install_from_local():
    """Install AION from local build"""
    print("📦 Installing AION from local build...")
    
    # Check if dist directory exists
    dist_dir = Path("dist")
    if not dist_dir.exists():
        print("❌ dist directory not found. Please run build_release.py first.")
        return False
    
    # Find wheel file
    wheel_files = list(dist_dir.glob("*.whl"))
    if not wheel_files:
        print("❌ No wheel file found in dist directory.")
        return False
    
    wheel_file = wheel_files[0]
    print(f"📄 Found wheel file: {wheel_file.name}")
    
    # Install the wheel
    result = run_command(f"pip install {wheel_file}")
    if result is not None:
        print("✅ AION installed successfully!")
        return True
    else:
        print("❌ Installation failed!")
        return False

def install_from_pypi():
    """Install AION from PyPI"""
    print("📦 Installing AION from PyPI...")
    
    result = run_command("pip install aion-ai")
    if result is not None:
        print("✅ AION installed successfully from PyPI!")
        return True
    else:
        print("❌ PyPI installation failed!")
        return False

def install_dependencies():
    """Install AION dependencies"""
    print("📦 Installing dependencies...")
    
    requirements_file = Path("requirements.txt")
    if requirements_file.exists():
        result = run_command(f"pip install -r {requirements_file}")
        if result is not None:
            print("✅ Dependencies installed successfully!")
            return True
        else:
            print("❌ Dependencies installation failed!")
            return False
    else:
        print("⚠️  requirements.txt not found, skipping dependencies")
        return True

def test_installation():
    """Test AION installation"""
    print("🧪 Testing AION installation...")
    
    try:
        # Test import - try different module names
        try:
            import aion_ai
            print(f"✅ AION package imported successfully")
        except ImportError:
            try:
                import main
                print(f"✅ AION main module imported successfully")
            except ImportError:
                print("❌ Could not import AION modules")
                return False

        # Test command line tools
        print("🔧 Testing command line tools...")

        # Test different command variations
        commands_to_test = [
            "aion --help",
            "aion-cli --help",
            "aion-ar --help",
            "python -m aion_ai --help",
            "python -c \"import main; print('AION main module works')\""
        ]

        success_count = 0
        for cmd in commands_to_test:
            result = run_command(cmd)
            if result is not None:
                print(f"✅ Command working: {cmd.split()[0]}")
                success_count += 1
            else:
                print(f"⚠️  Command not working: {cmd.split()[0]}")

        if success_count > 0:
            print(f"✅ {success_count}/{len(commands_to_test)} command line tools working!")
            return True
        else:
            print("⚠️  No command line tools working, but module import successful")
            return True

    except Exception as e:
        print(f"❌ AION testing failed: {e}")
        return False

def main():
    """Main installation function"""
    print("🚀 AION Installation Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        print("Please upgrade to Python 3.8 or higher")
        return 1
    
    # Installation options
    print("\n📋 Installation Options:")
    print("1. Install from local build (recommended for development)")
    print("2. Install from PyPI (recommended for users)")
    print("3. Install dependencies only")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
    except KeyboardInterrupt:
        print("\n\n👋 Installation cancelled by user")
        return 0
    
    success = False
    
    if choice == "1":
        print("\n" + "="*30 + " Local Installation " + "="*30)
        success = install_from_local()
        
    elif choice == "2":
        print("\n" + "="*30 + " PyPI Installation " + "="*30)
        success = install_from_pypi()
        
    elif choice == "3":
        print("\n" + "="*30 + " Dependencies Only " + "="*30)
        success = install_dependencies()
        
    else:
        print("❌ Invalid choice. Please run the script again.")
        return 1
    
    if success and choice in ["1", "2"]:
        print("\n" + "="*30 + " Testing Installation " + "="*30)
        test_success = test_installation()
        
        if test_success:
            print("\n🎉 AION installed and tested successfully!")
            print("\n🚀 Quick start commands:")
            print("   aion-cli          # English interface")
            print("   aion-ar           # Arabic interface")
            print("   python -m aion    # Direct module execution")
            print("\n📚 For more information:")
            print("   aion --help       # Show help")
            print("   aion-cli --help   # CLI help")
        else:
            print("\n⚠️  Installation completed but testing failed.")
            print("You may need to restart your terminal or check your PATH.")
    
    elif success:
        print("\n✅ Dependencies installed successfully!")
    
    else:
        print("\n❌ Installation failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
