#!/usr/bin/env python3
"""
🚀 AION GitHub Publisher
Simplified GitHub publishing without Git command line
"""

import os
import sys
import json
import shutil
import webbrowser
from pathlib import Path
import zipfile

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"🚀 {title}")
    print("="*60)

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ️  {message}")

def create_github_package():
    """Create a GitHub-ready package"""
    print_header("Creating GitHub Package")
    
    # Create GitHub package directory
    github_dir = Path("github_package")
    if github_dir.exists():
        shutil.rmtree(github_dir)
    github_dir.mkdir()
    
    print_info("Preparing files for GitHub...")
    
    # Files to include in GitHub package
    files_to_copy = [
        # Core files
        "main.py", "start_aion.py", "start_aion_en.py", "__init__.py", "__main__.py",
        
        # Package files
        "setup.py", "pyproject.toml", "requirements.txt", "requirements-dev.txt",
        "MANIFEST.in", "LICENSE", "CHANGELOG.md",
        
        # Documentation
        "README_GITHUB.md", "CONTRIBUTING.md", 
        
        # Build files
        "build_release.py", "install.py", "final_test.py", "quick_test.py",
        "build.bat", "Dockerfile", "docker-compose.yml",
        
        # Git files
        ".gitignore",
    ]
    
    # Directories to copy
    dirs_to_copy = [
        "core", "interfaces", "utils", "config", "locales", "templates",
        ".github", "dist"
    ]
    
    # Copy files
    copied_files = 0
    for file_name in files_to_copy:
        src = Path(file_name)
        if src.exists():
            dst = github_dir / file_name
            shutil.copy2(src, dst)
            copied_files += 1
    
    # Copy directories
    copied_dirs = 0
    for dir_name in dirs_to_copy:
        src = Path(dir_name)
        if src.exists():
            dst = github_dir / dir_name
            shutil.copytree(src, dst)
            copied_dirs += 1
    
    print_success(f"Copied {copied_files} files and {copied_dirs} directories")
    
    # Rename README for GitHub
    readme_src = github_dir / "README_GITHUB.md"
    readme_dst = github_dir / "README.md"
    if readme_src.exists():
        readme_src.rename(readme_dst)
        print_success("README prepared for GitHub")
    
    return github_dir

def create_zip_package(github_dir):
    """Create ZIP package for easy upload"""
    print_header("Creating ZIP Package")
    
    zip_path = Path("AION-GitHub-Package.zip")
    if zip_path.exists():
        zip_path.unlink()
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in github_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(github_dir)
                zipf.write(file_path, arcname)
    
    print_success(f"ZIP package created: {zip_path}")
    print_info(f"Package size: {zip_path.stat().st_size / 1024 / 1024:.1f} MB")
    
    return zip_path

def create_release_notes():
    """Create release notes"""
    print_header("Creating Release Notes")
    
    release_notes = """# 🚀 AION v1.0.0 - AI Operating Node

## 🎉 First Release

Welcome to AION (AI Operating Node) - a comprehensive multilingual terminal-based AI assistant!

### ✨ Features

- 🌍 **Multilingual Support**: Arabic, English, Norwegian, German, French, Chinese, Spanish
- 🤖 **Multiple AI Providers**: OpenAI, DeepSeek, OpenRouter, Gemini
- 💻 **Code Execution**: Python, JavaScript, Rust, C++
- 🔒 **Advanced Security**: Session management and token handling
- 🧩 **Plugin System**: Extensible architecture
- 🌐 **Multiple Interfaces**: CLI, TUI, Web
- 🐳 **Docker Support**: Complete containerization
- 🔄 **CI/CD Ready**: GitHub Actions pipeline

### 📦 Installation

```bash
# From PyPI (coming soon)
pip install aion-ai

# From source
git clone https://github.com/yourusername/aion-ai.git
cd aion-ai
python install.py
```

### 🚀 Quick Start

```bash
# English interface
aion-cli

# Arabic interface  
aion-ar

# Web interface
python -m aion web
```

### 📋 Requirements

- Python 3.8+
- Windows, macOS, or Linux

### 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

### 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

**Built with ❤️ by the AION Development Team**
"""
    
    release_file = Path("RELEASE_NOTES.md")
    with open(release_file, 'w', encoding='utf-8') as f:
        f.write(release_notes)
    
    print_success("Release notes created: RELEASE_NOTES.md")
    return release_file

def show_github_instructions():
    """Show GitHub publishing instructions"""
    print_header("GitHub Publishing Instructions")
    
    print("📋 Follow these steps to publish AION on GitHub:")
    print()
    print("🌐 **Method 1: Using GitHub Web Interface (Recommended)**")
    print("1. Go to https://github.com/new")
    print("2. Repository name: 'aion-ai'")
    print("3. Description: '🤖 AION - AI Operating Node: Multilingual Terminal-based AI Assistant'")
    print("4. Make it Public")
    print("5. Don't initialize with README/license (we have them)")
    print("6. Click 'Create repository'")
    print("7. Click 'uploading an existing file'")
    print("8. Drag and drop the AION-GitHub-Package.zip file")
    print("9. Commit the files")
    print()
    print("🖥️ **Method 2: Using GitHub Desktop**")
    print("1. Download GitHub Desktop from https://desktop.github.com/")
    print("2. Install and sign in to your GitHub account")
    print("3. Click 'Add an Existing Repository from your Hard Drive'")
    print("4. Select the 'github_package' folder")
    print("5. Publish to GitHub")
    print()
    print("📦 **Method 3: Extract and Upload**")
    print("1. Extract AION-GitHub-Package.zip to a new folder")
    print("2. Create new repository on GitHub")
    print("3. Upload all extracted files via web interface")
    print()
    
    # Open GitHub
    try:
        webbrowser.open("https://github.com/new")
        print_info("Opening GitHub repository creation page...")
    except:
        pass

def show_release_instructions():
    """Show release creation instructions"""
    print_header("Creating GitHub Release")
    
    print("🏷️ After uploading your code, create a release:")
    print()
    print("1. Go to your repository on GitHub")
    print("2. Click 'Releases' → 'Create a new release'")
    print("3. Tag version: 'v1.0.0'")
    print("4. Release title: '🚀 AION v1.0.0 - AI Operating Node'")
    print("5. Copy description from RELEASE_NOTES.md")
    print("6. Upload these files as assets:")
    
    # List distribution files
    dist_dir = Path("dist")
    if dist_dir.exists():
        for file in dist_dir.glob("*"):
            print(f"   📄 {file.name}")
    
    print("7. Click 'Publish release'")
    print()
    print("🎉 Your AION project will be live on GitHub!")

def main():
    """Main publishing function"""
    print("🚀 AION GitHub Publisher")
    print("=" * 60)
    print("This will prepare AION for GitHub publishing")
    print()
    
    try:
        # Create GitHub package
        github_dir = create_github_package()
        
        # Create ZIP package
        zip_path = create_zip_package(github_dir)
        
        # Create release notes
        release_file = create_release_notes()
        
        # Show instructions
        show_github_instructions()
        show_release_instructions()
        
        print_header("Package Ready!")
        print("📦 Your AION package is ready for GitHub!")
        print()
        print("📁 Files created:")
        print(f"   📂 {github_dir}/ - GitHub package directory")
        print(f"   📄 {zip_path} - ZIP package for upload")
        print(f"   📄 {release_file} - Release notes")
        print()
        print("🚀 Next steps:")
        print("1. Go to https://github.com/new (already opened)")
        print("2. Create repository 'aion-ai'")
        print("3. Upload the ZIP file or use GitHub Desktop")
        print("4. Create release v1.0.0")
        print("5. Share your project!")
        
        return True
        
    except Exception as e:
        print_error(f"Error creating package: {e}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Publishing cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
