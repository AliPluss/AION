# AION Tests

This directory contains the test suite for the AION (AI Operating Node) project.

## Test Structure

```
tests/
├── __init__.py          # Test package initialization
├── conftest.py          # Pytest configuration and fixtures
├── test_basic.py        # Basic functionality tests
├── test_core.py         # Core module tests
├── test_integration.py  # Integration tests
└── README.md           # This file
```

## Running Tests

### Prerequisites

Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

### Basic Test Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_basic.py

# Run with coverage
pytest --cov=. --cov-report=html

# Run only basic tests
make test-basic

# Run only integration tests
make test-integration

# Health check
make health-check
```

### Test Categories

#### Basic Tests (`test_basic.py`)
- Python version compatibility
- Core module imports
- File structure validation
- Configuration file existence

#### Core Tests (`test_core.py`)
- Core module functionality
- Configuration handling
- Mock-based testing

#### Integration Tests (`test_integration.py`)
- System component integration
- End-to-end workflows
- AION project specific tests

## Test Configuration

### Pytest Configuration
Configuration is defined in `pyproject.toml`:
- Test paths: `tests/` and root directory
- Test file patterns: `test_*.py`, `*_test.py`
- Markers for categorizing tests

### Fixtures
Common fixtures are defined in `conftest.py`:
- `mock_config`: Mock configuration data
- `mock_ai_provider`: Mock AI provider
- `sample_code`: Sample code for testing
- `temp_config_file`: Temporary config file

### Markers
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.slow`: Slow-running tests
- `@pytest.mark.unit`: Unit tests

## CI/CD Integration

Tests are automatically run in GitHub Actions:
- Multiple Python versions (3.8-3.12)
- Multiple operating systems (Ubuntu, Windows)
- Code quality checks (flake8, black, mypy)
- Security checks (bandit, safety)

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure project root is in Python path
2. **Missing Dependencies**: Install with `pip install -r requirements-dev.txt`
3. **Path Issues**: Tests assume they're run from project root

### Debug Mode
Run tests with more verbose output:
```bash
pytest -v --tb=long --capture=no
```

### Skip Slow Tests
```bash
pytest -m "not slow"
```

## Contributing

When adding new tests:
1. Follow the existing naming convention
2. Add appropriate markers
3. Use fixtures for common setup
4. Keep tests focused and independent
5. Add docstrings explaining test purpose

## Test Coverage

Aim for high test coverage while focusing on:
- Critical functionality
- Error handling
- Integration points
- Configuration management
