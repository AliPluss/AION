#!/usr/bin/env python3
"""
🚀 AION GitHub Setup Script
Automated script to prepare and publish AION to GitHub
"""

import os
import sys
import json
import subprocess
import webbrowser
from pathlib import Path

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

def print_warning(message):
    """Print warning message"""
    print(f"⚠️  {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ️  {message}")

def run_command(command, check=True):
    """Run a command and return result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        if check and result.returncode != 0:
            print_error(f"Command failed: {command}")
            print_error(f"Error: {result.stderr}")
            return None
        return result
    except Exception as e:
        print_error(f"Failed to run command '{command}': {e}")
        return None

def check_git_installed():
    """Check if Git is installed"""
    result = run_command("git --version", check=False)
    if result and result.returncode == 0:
        print_success(f"Git is installed: {result.stdout.strip()}")
        return True
    else:
        print_warning("Git is not installed or not in PATH")
        return False

def install_git_instructions():
    """Provide Git installation instructions"""
    print_header("Git Installation Required")
    print("🔧 Git is required to publish to GitHub. Please install Git:")
    print("\n📥 Download Git for Windows:")
    print("   https://git-scm.com/download/win")
    print("\n📋 Installation steps:")
    print("   1. Download Git from the link above")
    print("   2. Run the installer with default settings")
    print("   3. Restart your terminal/command prompt")
    print("   4. Run this script again")
    
    # Open Git download page
    try:
        webbrowser.open("https://git-scm.com/download/win")
        print_info("Opening Git download page in your browser...")
    except:
        pass
    
    return False

def setup_git_config():
    """Setup Git configuration"""
    print_header("Git Configuration")
    
    # Check if git config exists
    result = run_command("git config --global user.name", check=False)
    if not result or not result.stdout.strip():
        print("🔧 Setting up Git configuration...")
        name = input("Enter your name for Git commits: ").strip()
        email = input("Enter your email for Git commits: ").strip()
        
        if name and email:
            run_command(f'git config --global user.name "{name}"')
            run_command(f'git config --global user.email "{email}"')
            print_success("Git configuration completed")
        else:
            print_error("Name and email are required")
            return False
    else:
        print_success(f"Git already configured for: {result.stdout.strip()}")
    
    return True

def create_git_repository():
    """Create local Git repository"""
    print_header("Creating Local Git Repository")
    
    # Initialize repository
    result = run_command("git init")
    if not result:
        return False
    print_success("Git repository initialized")
    
    # Add all files
    result = run_command("git add .")
    if not result:
        return False
    print_success("Files added to Git")
    
    # Create initial commit
    commit_message = "🚀 Initial AION v1.0.0 release - Complete AI Operating Node"
    result = run_command(f'git commit -m "{commit_message}"')
    if not result:
        return False
    print_success("Initial commit created")
    
    # Set main branch
    run_command("git branch -M main")
    print_success("Main branch set")
    
    return True

def create_github_repository():
    """Instructions for creating GitHub repository"""
    print_header("Creating GitHub Repository")
    
    print("📋 Please follow these steps to create your GitHub repository:")
    print("\n1. 🌐 Go to GitHub.com and sign in to your account")
    print("2. ➕ Click the '+' button in the top right corner")
    print("3. 📝 Select 'New repository'")
    print("4. 📛 Repository name: 'aion-ai'")
    print("5. 📄 Description: '🤖 AION - AI Operating Node: Multilingual Terminal-based AI Assistant'")
    print("6. 🌍 Make it Public (recommended for open source)")
    print("7. ❌ Do NOT initialize with README, .gitignore, or license (we already have them)")
    print("8. ✅ Click 'Create repository'")
    
    # Open GitHub
    try:
        webbrowser.open("https://github.com/new")
        print_info("Opening GitHub repository creation page...")
    except:
        pass
    
    print("\n⏳ After creating the repository, copy the repository URL")
    print("   Example: https://github.com/yourusername/aion-ai.git")
    
    repo_url = input("\n🔗 Enter your GitHub repository URL: ").strip()
    
    if not repo_url:
        print_error("Repository URL is required")
        return None
    
    return repo_url

def push_to_github(repo_url):
    """Push code to GitHub"""
    print_header("Pushing to GitHub")
    
    # Add remote origin
    result = run_command(f"git remote add origin {repo_url}")
    if not result:
        # Try to set URL if remote already exists
        run_command(f"git remote set-url origin {repo_url}")
    
    print_success("Remote origin set")
    
    # Push to GitHub
    result = run_command("git push -u origin main")
    if not result:
        return False
    
    print_success("Code pushed to GitHub successfully!")
    
    # Extract repository info
    if repo_url.endswith('.git'):
        repo_url = repo_url[:-4]
    
    print(f"\n🎉 Your AION project is now live on GitHub!")
    print(f"🔗 Repository: {repo_url}")
    
    # Open repository
    try:
        webbrowser.open(repo_url)
        print_info("Opening your GitHub repository...")
    except:
        pass
    
    return True

def create_github_release():
    """Instructions for creating GitHub release"""
    print_header("Creating GitHub Release")
    
    # Load release info
    release_info_path = Path("release_info.json")
    if release_info_path.exists():
        with open(release_info_path, 'r', encoding='utf-8') as f:
            release_info = json.load(f)
        
        print("📋 Release information loaded:")
        print(f"   Version: {release_info.get('version', '1.0.0')}")
        print(f"   Title: {release_info.get('title', 'AION v1.0.0')}")
        
        print("\n📝 To create a release on GitHub:")
        print("1. 🏷️  Go to your repository → Releases → Create a new release")
        print(f"2. 🔖 Tag version: v{release_info.get('version', '1.0.0')}")
        print(f"3. 📛 Release title: {release_info.get('title', 'AION v1.0.0')}")
        print("4. 📄 Copy the description from release_info.json")
        print("5. 📎 Upload the files from dist/ folder as assets")
        print("6. ✅ Click 'Publish release'")
        
        print(f"\n📦 Files to upload as release assets:")
        dist_path = Path("dist")
        if dist_path.exists():
            for file in dist_path.glob("*"):
                print(f"   📄 {file.name}")
    
    return True

def main():
    """Main setup function"""
    print("🚀 AION GitHub Setup Script")
    print("=" * 60)
    print("This script will help you publish AION to GitHub")
    
    # Check Git installation
    if not check_git_installed():
        return install_git_instructions()
    
    # Setup Git configuration
    if not setup_git_config():
        return False
    
    # Create local repository
    if not create_git_repository():
        return False
    
    # Create GitHub repository
    repo_url = create_github_repository()
    if not repo_url:
        return False
    
    # Push to GitHub
    if not push_to_github(repo_url):
        return False
    
    # Create release instructions
    create_github_release()
    
    print_header("Setup Complete!")
    print("🎉 AION has been successfully published to GitHub!")
    print("\n🚀 Next steps:")
    print("   1. ⭐ Star your repository")
    print("   2. 📝 Create a release (v1.0.0)")
    print("   3. 📢 Share your project")
    print("   4. 🔄 Enable GitHub Actions for CI/CD")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Setup incomplete. Please resolve the issues and try again.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
