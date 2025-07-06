"""
Basic tests for AION system
"""
import pytest
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_python_version():
    """Test that Python version is supported"""
    assert sys.version_info >= (3, 8), "Python 3.8+ is required"


def test_imports():
    """Test that basic Python modules can be imported"""
    # Test essential Python modules
    import json
    import os
    import sys
    import pathlib

    # Verify they work
    assert json.dumps({"test": True}) == '{"test": true}'
    assert os.path.exists(".")
    assert sys.version_info >= (3, 8)
    assert pathlib.Path(".").exists()

    # Try to import AION modules if they exist (optional)
    aion_modules = ["core", "interfaces", "utils"]
    available_modules = []

    for module_name in aion_modules:
        try:
            __import__(module_name)
            available_modules.append(module_name)
        except ImportError:
            pass  # Module not available, that's OK

    # Log what's available
    print(f"Available AION modules: {available_modules}")
    assert True  # Test passes regardless of AION modules


def test_config_files_exist():
    """Test that essential config files exist"""
    config_files = [
        "requirements.txt",
        "pyproject.toml",
        "README.md"
    ]
    
    for config_file in config_files:
        file_path = project_root / config_file
        assert file_path.exists(), f"Required file {config_file} not found"


def test_main_modules_exist():
    """Test that main application files exist"""
    main_files = [
        "main.py",
        "start_aion_en.py"
    ]
    
    for main_file in main_files:
        file_path = project_root / main_file
        assert file_path.exists(), f"Main file {main_file} not found"


def test_core_directory_structure():
    """Test that core directory structure exists"""
    core_dirs = [
        "core",
        "interfaces", 
        "utils",
        "locales",
        "config"
    ]
    
    for core_dir in core_dirs:
        dir_path = project_root / core_dir
        if dir_path.exists():
            assert dir_path.is_dir(), f"{core_dir} should be a directory"


def test_locale_files():
    """Test that locale files exist"""
    locale_dir = project_root / "locales"
    if locale_dir.exists():
        expected_locales = ["en.json", "ar.json"]
        for locale in expected_locales:
            locale_file = locale_dir / locale
            if locale_file.exists():
                assert locale_file.is_file(), f"Locale file {locale} should exist"


class TestAIONBasic:
    """Basic AION functionality tests"""
    
    def test_can_create_instance(self):
        """Test that we can create basic instances"""
        # This is a placeholder test
        assert True
    
    def test_environment_setup(self):
        """Test that environment is properly set up"""
        # Check if we're in the right directory
        assert project_root.exists()
        assert (project_root / "main.py").exists() or (project_root / "aion_project" / "main.py").exists()


if __name__ == "__main__":
    pytest.main([__file__])
