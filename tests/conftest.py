"""
Pytest configuration and fixtures for AION tests
"""
import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture(scope="session")
def project_root_path():
    """Fixture providing the project root path"""
    return project_root


@pytest.fixture
def mock_config():
    """Mock configuration for testing"""
    return {
        "app": {
            "language": "en",
            "theme": "default",
            "debug": False
        },
        "ai": {
            "default_provider": "openai",
            "current_model": "gpt-4",
            "max_tokens": 4000
        },
        "providers": {
            "openai": {
                "api_key": "test-key",
                "models": ["gpt-4", "gpt-3.5-turbo"]
            },
            "deepseek": {
                "api_key": "test-key",
                "models": ["deepseek-chat", "deepseek-coder"]
            }
        }
    }


@pytest.fixture
def mock_ai_provider():
    """Mock AI provider for testing"""
    provider = Mock()
    provider.name = "test-provider"
    provider.models = ["test-model"]
    provider.generate_response.return_value = "Test response"
    return provider


@pytest.fixture
def sample_code():
    """Sample code for testing code execution"""
    return {
        "python": 'print("Hello, World!")',
        "javascript": 'console.log("Hello, World!");',
        "rust": 'fn main() { println!("Hello, World!"); }',
        "cpp": '#include <iostream>\nint main() { std::cout << "Hello, World!" << std::endl; return 0; }'
    }


@pytest.fixture
def temp_config_file(tmp_path, mock_config):
    """Create a temporary config file for testing"""
    import json
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(mock_config, indent=2))
    return config_file


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment before each test"""
    # Ensure we're in the right directory
    os.chdir(project_root)
    yield
    # Cleanup after test if needed


def pytest_configure(config):
    """Configure pytest"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    # Add markers to tests based on their location
    for item in items:
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Mark slow tests
        if "slow" in item.name or "integration" in str(item.fspath):
            item.add_marker(pytest.mark.slow)
