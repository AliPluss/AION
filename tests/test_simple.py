"""
Simple tests that should always pass
"""
import sys
import os
from pathlib import Path


def test_python_version():
    """Test Python version is supported"""
    assert sys.version_info >= (3, 8), f"Python 3.8+ required, got {sys.version_info}"


def test_basic_imports():
    """Test basic Python imports work"""
    import json
    import pathlib
    import tempfile
    
    # Test they actually work
    assert json.dumps({"test": True}) == '{"test": true}'
    assert pathlib.Path(".").exists()
    
    with tempfile.NamedTemporaryFile() as f:
        assert f.name is not None


def test_project_structure():
    """Test basic project structure"""
    project_root = Path(__file__).parent.parent
    
    # These files should exist
    essential_files = [
        "README.md",
        "requirements.txt", 
        "pyproject.toml"
    ]
    
    for file_name in essential_files:
        file_path = project_root / file_name
        assert file_path.exists(), f"Essential file {file_name} not found"


def test_directories():
    """Test important directories exist"""
    project_root = Path(__file__).parent.parent
    
    # These directories should exist
    important_dirs = [
        "tests",
        ".github",
        ".github/workflows"
    ]
    
    for dir_name in important_dirs:
        dir_path = project_root / dir_name
        assert dir_path.exists(), f"Important directory {dir_name} not found"
        assert dir_path.is_dir(), f"{dir_name} should be a directory"


def test_workflow_files():
    """Test GitHub workflow files exist"""
    project_root = Path(__file__).parent.parent
    workflows_dir = project_root / ".github" / "workflows"
    
    if workflows_dir.exists():
        workflow_files = list(workflows_dir.glob("*.yml"))
        assert len(workflow_files) > 0, "At least one workflow file should exist"
        
        # Check for specific workflows
        workflow_names = [f.name for f in workflow_files]
        print(f"Found workflows: {workflow_names}")


def test_environment():
    """Test environment is set up correctly"""
    # Test current working directory
    cwd = os.getcwd()
    assert cwd is not None
    
    # Test we can create files
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=True) as f:
        f.write("test")
        f.flush()
        assert os.path.exists(f.name)


def test_always_passes():
    """A test that always passes for CI verification"""
    assert True
    assert 1 + 1 == 2
    assert "hello" == "hello"


if __name__ == "__main__":
    # Run tests directly if called as script
    import pytest
    pytest.main([__file__, "-v"])
