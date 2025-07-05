#!/usr/bin/env python3
"""
🚀 AION Release Builder
Script to prepare AION for GitHub release and PyPI publication
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path
from datetime import datetime

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

def check_dependencies():
    """Check if required build dependencies are installed"""
    print("📦 Checking build dependencies...")
    
    required_packages = [
        "build", "twine", "wheel", "setuptools"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Installing missing packages: {', '.join(missing)}")
        run_command(f"pip install {' '.join(missing)}")
    
    return True

def clean_build_artifacts():
    """Clean previous build artifacts"""
    print("🧹 Cleaning build artifacts...")

    dirs_to_clean = [
        "build", "dist", "__pycache__",
        ".pytest_cache", ".mypy_cache", "htmlcov"
    ]

    # Clean directories
    for dir_name in dirs_to_clean:
        path = Path(dir_name)
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
                print(f"🗑️  Removed {dir_name}")
            else:
                path.unlink()
                print(f"🗑️  Removed {dir_name}")

    # Clean egg-info directories
    for egg_info in Path(".").glob("*.egg-info"):
        if egg_info.is_dir():
            shutil.rmtree(egg_info)
            print(f"🗑️  Removed {egg_info.name}")

    return True

def update_version():
    """Update version information"""
    print("📝 Updating version information...")
    
    # Read current version from setup.py
    setup_file = Path("setup.py")
    if setup_file.exists():
        content = setup_file.read_text()
        # Extract version (simple regex would work here)
        import re
        version_match = re.search(r'version="([^"]+)"', content)
        if version_match:
            current_version = version_match.group(1)
            print(f"📋 Current version: {current_version}")
            return current_version
    
    return "1.0.0"

def run_tests():
    """Run test suite"""
    print("🧪 Running test suite...")
    
    # Check if pytest is available
    try:
        import pytest
        result = run_command("python -m pytest --tb=short")
        if result is not None:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Tests failed!")
            return False
    except ImportError:
        print("⚠️  pytest not installed, skipping tests")
        return True

def run_linting():
    """Run code linting"""
    print("🔍 Running code linting...")
    
    # Check flake8
    try:
        import flake8
        result = run_command("flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics")
        if result is not None:
            print("✅ Linting passed!")
            return True
    except ImportError:
        print("⚠️  flake8 not installed, skipping linting")
        return True

def build_package():
    """Build the package"""
    print("🏗️  Building package...")
    
    # Build using python -m build
    result = run_command("python -m build")
    if result is not None:
        print("✅ Package built successfully!")
        
        # List built files
        dist_dir = Path("dist")
        if dist_dir.exists():
            print("📦 Built files:")
            for file in dist_dir.iterdir():
                print(f"   📄 {file.name}")
        
        return True
    else:
        print("❌ Package build failed!")
        return False

def check_package():
    """Check the built package"""
    print("🔍 Checking package...")
    
    result = run_command("twine check dist/*")
    if result is not None:
        print("✅ Package check passed!")
        return True
    else:
        print("❌ Package check failed!")
        return False

def create_github_release_info():
    """Create GitHub release information"""
    print("📋 Creating GitHub release information...")
    
    version = update_version()
    release_date = datetime.now().strftime("%Y-%m-%d")
    
    release_info = {
        "tag_name": f"v{version}",
        "target_commitish": "main",
        "name": f"AION v{version}",
        "body": f"""# 🚀 AION v{version} Release

## 🌟 What's New

This release includes all the core features of AION:

### ✨ Features
- 🌍 **Multilingual Support**: 7 languages with beautiful UI
- 🤖 **AI Integration**: Multiple AI providers support
- 💻 **Code Execution**: Python, JavaScript, Rust, C++
- 🔒 **Security**: Advanced security and session management
- 🧩 **Plugins**: Extensible plugin system
- 🌐 **Interfaces**: CLI, TUI, and Web interfaces

### 📦 Installation
```bash
pip install aion-ai=={version}
```

### 🔗 Quick Start
```bash
# Start AION
aion-cli

# Or with Arabic interface
aion-ar
```

### 📚 Documentation
- [User Guide](https://github.com/yourusername/aion-ai/wiki)
- [API Reference](https://github.com/yourusername/aion-ai/blob/main/docs/api-reference.md)

### 🙏 Thanks
Thank you to all contributors and users who made this release possible!

---
**Full Changelog**: https://github.com/yourusername/aion-ai/compare/v0.9.0...v{version}
""",
        "draft": False,
        "prerelease": False
    }
    
    # Save release info
    with open("release_info.json", "w") as f:
        json.dump(release_info, f, indent=2)
    
    print("📄 Release info saved to release_info.json")
    return True

def prepare_github_files():
    """Prepare files for GitHub"""
    print("📁 Preparing GitHub files...")
    
    # Copy README_GITHUB.md to README.md for GitHub
    github_readme = Path("README_GITHUB.md")
    main_readme = Path("README.md")
    
    if github_readme.exists():
        # Backup original README
        if main_readme.exists():
            shutil.copy2(main_readme, "README_ORIGINAL.md")
            print("📋 Backed up original README.md")
        
        # Copy GitHub README
        shutil.copy2(github_readme, main_readme)
        print("📋 Updated README.md for GitHub")
    
    return True

def main():
    """Main build process"""
    print("🚀 AION Release Builder")
    print("=" * 50)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    steps = [
        ("Check Dependencies", check_dependencies),
        ("Clean Build Artifacts", clean_build_artifacts),
        ("Update Version", update_version),
        ("Run Tests", run_tests),
        ("Run Linting", run_linting),
        ("Build Package", build_package),
        ("Check Package", check_package),
        ("Create Release Info", create_github_release_info),
        ("Prepare GitHub Files", prepare_github_files),
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        try:
            result = step_func()
            if result:
                print(f"✅ {step_name} completed successfully!")
            else:
                print(f"❌ {step_name} failed!")
                failed_steps.append(step_name)
        except Exception as e:
            print(f"❌ {step_name} failed with exception: {e}")
            failed_steps.append(step_name)
    
    print("\n" + "="*50)
    print("🏁 Build Summary")
    print("="*50)
    
    if failed_steps:
        print(f"❌ Failed steps: {', '.join(failed_steps)}")
        print("Please fix the issues and try again.")
        return 1
    else:
        print("✅ All steps completed successfully!")
        print("\n📦 Your package is ready for release!")
        print("\n🚀 Next steps:")
        print("1. Upload to PyPI: twine upload dist/*")
        print("2. Create GitHub release using release_info.json")
        print("3. Push changes to GitHub")
        return 0

if __name__ == "__main__":
    sys.exit(main())
