#!/usr/bin/env python3
"""
🐍 AION PyPI Deployment Script
Automated deployment script for publishing AION to PyPI
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(message, color=Colors.OKBLUE):
    """Print a colored step message"""
    print(f"{color}{Colors.BOLD}🚀 {message}{Colors.ENDC}")

def print_success(message):
    """Print a success message"""
    print(f"{Colors.OKGREEN}{Colors.BOLD}✅ {message}{Colors.ENDC}")

def print_error(message):
    """Print an error message"""
    print(f"{Colors.FAIL}{Colors.BOLD}❌ {message}{Colors.ENDC}")

def print_warning(message):
    """Print a warning message"""
    print(f"{Colors.WARNING}{Colors.BOLD}⚠️ {message}{Colors.ENDC}")

def run_command(command, check=True):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=check, 
            capture_output=True, 
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {command}")
        print_error(f"Error: {e.stderr}")
        return None

def check_prerequisites():
    """Check if all required tools are installed"""
    print_step("Checking prerequisites...")
    
    required_tools = ['python', 'pip', 'twine']
    missing_tools = []
    
    for tool in required_tools:
        result = run_command(f"which {tool}", check=False)
        if result is None or result.returncode != 0:
            missing_tools.append(tool)
    
    if missing_tools:
        print_error(f"Missing required tools: {', '.join(missing_tools)}")
        print("Please install missing tools:")
        print("pip install --upgrade pip build twine setuptools wheel")
        return False
    
    print_success("All prerequisites are installed")
    return True

def clean_build_directories():
    """Clean previous build directories"""
    print_step("Cleaning previous builds...")
    
    dirs_to_clean = ['build', 'dist', '*.egg-info']
    
    for pattern in dirs_to_clean:
        if '*' in pattern:
            # Handle glob patterns
            import glob
            for path in glob.glob(pattern):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"Removed: {path}")
        else:
            if os.path.exists(pattern):
                shutil.rmtree(pattern)
                print(f"Removed: {pattern}")
    
    print_success("Build directories cleaned")

def verify_package_files():
    """Verify that all required package files exist"""
    print_step("Verifying package files...")
    
    required_files = [
        'setup.py',
        'pyproject.toml',
        'README.md',
        'LICENSE',
        'MANIFEST.in',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print_error(f"Missing required files: {', '.join(missing_files)}")
        return False
    
    print_success("All required package files exist")
    return True

def build_package():
    """Build the package"""
    print_step("Building package...")
    
    result = run_command("python -m build")
    if result is None:
        print_error("Package build failed")
        return False
    
    # Check if dist files were created
    if not os.path.exists('dist'):
        print_error("No dist directory created")
        return False
    
    dist_files = os.listdir('dist')
    if not dist_files:
        print_error("No files in dist directory")
        return False
    
    print_success(f"Package built successfully. Files: {', '.join(dist_files)}")
    return True

def check_package():
    """Check the built package for issues"""
    print_step("Checking package...")
    
    result = run_command("python -m twine check dist/*")
    if result is None:
        print_error("Package check failed")
        return False
    
    print_success("Package check passed")
    return True

def deploy_to_testpypi():
    """Deploy to TestPyPI"""
    print_step("Deploying to TestPyPI...")
    
    result = run_command("python -m twine upload --repository testpypi dist/*")
    if result is None:
        print_error("TestPyPI deployment failed")
        return False
    
    print_success("Successfully deployed to TestPyPI")
    print(f"{Colors.OKCYAN}🔗 Check: https://test.pypi.org/project/aion-ai/{Colors.ENDC}")
    return True

def deploy_to_pypi():
    """Deploy to production PyPI"""
    print_step("Deploying to PyPI...")
    
    result = run_command("python -m twine upload dist/*")
    if result is None:
        print_error("PyPI deployment failed")
        return False
    
    print_success("Successfully deployed to PyPI")
    print(f"{Colors.OKCYAN}🔗 Check: https://pypi.org/project/aion-ai/{Colors.ENDC}")
    return True

def test_installation():
    """Test installation from PyPI"""
    print_step("Testing installation...")
    
    # Create a temporary virtual environment for testing
    test_env = "test_pypi_install"
    
    print("Creating test environment...")
    result = run_command(f"python -m venv {test_env}")
    if result is None:
        print_warning("Could not create test environment")
        return False
    
    # Activate and test installation
    if os.name == 'nt':  # Windows
        activate_cmd = f"{test_env}\\Scripts\\activate"
        pip_cmd = f"{test_env}\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        activate_cmd = f"source {test_env}/bin/activate"
        pip_cmd = f"{test_env}/bin/pip"
    
    print("Installing package in test environment...")
    result = run_command(f"{pip_cmd} install aion-ai")
    if result is None:
        print_warning("Test installation failed")
        shutil.rmtree(test_env, ignore_errors=True)
        return False
    
    print_success("Test installation successful")
    
    # Cleanup
    shutil.rmtree(test_env, ignore_errors=True)
    return True

def main():
    """Main deployment function"""
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("🐍 AION PyPI Deployment Script")
    print("=" * 50)
    print(f"{Colors.ENDC}")
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Verify package files
    if not verify_package_files():
        sys.exit(1)
    
    # Clean build directories
    clean_build_directories()
    
    # Build package
    if not build_package():
        sys.exit(1)
    
    # Check package
    if not check_package():
        sys.exit(1)
    
    # Deploy to TestPyPI first
    print("\n" + "="*50)
    print("🧪 TESTPYPI DEPLOYMENT")
    print("="*50)
    
    if not deploy_to_testpypi():
        sys.exit(1)
    
    # Ask for production deployment
    print("\n" + "="*50)
    print("🚀 PRODUCTION DEPLOYMENT")
    print("="*50)
    
    response = input(f"{Colors.WARNING}Deploy to production PyPI? (y/N): {Colors.ENDC}")
    
    if response.lower() in ['y', 'yes']:
        if not deploy_to_pypi():
            sys.exit(1)
        
        # Test installation
        print("\n" + "="*50)
        print("🧪 INSTALLATION TEST")
        print("="*50)
        
        test_response = input(f"{Colors.WARNING}Test installation from PyPI? (y/N): {Colors.ENDC}")
        if test_response.lower() in ['y', 'yes']:
            test_installation()
    
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}")
    print("🎉 DEPLOYMENT COMPLETE!")
    print("="*50)
    print("Users can now install AION with:")
    print("pip install aion-ai")
    print(f"{Colors.ENDC}")

if __name__ == "__main__":
    main()
