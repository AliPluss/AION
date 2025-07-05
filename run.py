#!/usr/bin/env python3
"""
🚀 AION Quick Start Script
Quick launcher for AION with automatic setup
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        Path.home() / ".aion",
        Path.home() / ".aion" / "logs",
        Path.home() / ".aion" / "plugins",
        Path.home() / ".aion" / "config"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def setup_config():
    """Setup configuration files"""
    config_dir = Path.home() / ".aion" / "config"
    template_file = Path(__file__).parent / "config" / "ai_config_template.json"
    config_file = config_dir / "ai_config.json"
    
    if not config_file.exists() and template_file.exists():
        shutil.copy2(template_file, config_file)
        print(f"📋 Created AI config: {config_file}")
        print("⚠️  Please edit the config file to add your API keys")

def install_dependencies():
    """Install required dependencies"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if requirements_file.exists():
        print("📦 Installing dependencies...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False
    else:
        print("⚠️  requirements.txt not found")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        "typer", "rich", "textual", "fastapi", "uvicorn", "httpx"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        return False
    
    print("✅ All required packages are installed")
    return True

def run_aion():
    """Run AION main application"""
    main_file = Path(__file__).parent / "main.py"
    
    if main_file.exists():
        print("🚀 Starting AION...")
        try:
            subprocess.run([sys.executable, str(main_file)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to start AION: {e}")
        except KeyboardInterrupt:
            print("\n👋 AION stopped by user")
    else:
        print("❌ main.py not found")

def show_help():
    """Show help information"""
    help_text = """
🤖 AION - AI Operating Node

Usage: python run.py [command]

Commands:
  setup     - Setup AION (create directories, install dependencies)
  install   - Install dependencies only
  config    - Setup configuration files
  run       - Run AION (default)
  help      - Show this help

Examples:
  python run.py setup    # First time setup
  python run.py          # Run AION
  python run.py config   # Setup config files
"""
    print(help_text)

def main():
    """Main function"""
    if not check_python_version():
        sys.exit(1)
    
    # Parse command line arguments
    command = sys.argv[1] if len(sys.argv) > 1 else "run"
    
    if command == "help":
        show_help()
        return
    
    elif command == "setup":
        print("🔧 Setting up AION...")
        create_directories()
        setup_config()
        if install_dependencies():
            print("✅ AION setup completed successfully!")
            print("📝 Don't forget to configure your AI API keys in ~/.aion/config/ai_config.json")
        else:
            print("❌ Setup failed")
            sys.exit(1)
    
    elif command == "install":
        print("📦 Installing dependencies...")
        if not install_dependencies():
            sys.exit(1)
    
    elif command == "config":
        print("📋 Setting up configuration...")
        create_directories()
        setup_config()
    
    elif command == "run":
        # Check if dependencies are installed
        if not check_dependencies():
            print("💡 Run 'python run.py setup' to install dependencies")
            sys.exit(1)
        
        # Create directories if they don't exist
        create_directories()
        
        # Run AION
        run_aion()
    
    else:
        print(f"❌ Unknown command: {command}")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
