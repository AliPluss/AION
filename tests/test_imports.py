"""
Test AION module imports
"""
import pytest
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_basic_imports():
    """Test basic Python imports work"""
    import json
    import os
    import sys
    import pathlib
    
    assert json.dumps({"test": True}) == '{"test": true}'
    assert os.path.exists(".")
    assert sys.version_info >= (3, 8)
    assert pathlib.Path(".").exists()


def test_aion_structure():
    """Test AION package structure"""
    aion_path = project_root / "aion"
    assert aion_path.exists(), "AION package directory should exist"
    assert aion_path.is_dir(), "AION should be a directory"
    
    # Check main files
    main_files = [
        "aion/__init__.py",
        "aion/main.py"
    ]
    
    for file_path in main_files:
        full_path = project_root / file_path
        assert full_path.exists(), f"File {file_path} should exist"


def test_aion_submodules():
    """Test AION submodule structure"""
    submodules = [
        "aion/core",
        "aion/interfaces", 
        "aion/utils"
    ]
    
    for submodule in submodules:
        submodule_path = project_root / submodule
        if submodule_path.exists():
            assert submodule_path.is_dir(), f"{submodule} should be a directory"
            init_file = submodule_path / "__init__.py"
            assert init_file.exists(), f"{submodule}/__init__.py should exist"


def test_requirements_file():
    """Test requirements file exists and is readable"""
    req_file = project_root / "requirements.txt"
    assert req_file.exists(), "requirements.txt should exist"
    
    # Try to read it
    content = req_file.read_text()
    assert len(content) > 0, "requirements.txt should not be empty"


def test_config_files():
    """Test configuration files exist"""
    config_files = [
        "pyproject.toml",
        "README.md"
    ]
    
    for config_file in config_files:
        file_path = project_root / config_file
        assert file_path.exists(), f"Config file {config_file} should exist"


@pytest.mark.unit
def test_python_version_compatibility():
    """Test Python version compatibility"""
    assert sys.version_info >= (3, 8), "Python 3.8+ is required for AION"
    assert sys.version_info < (4, 0), "Python 4.x is not yet supported"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
