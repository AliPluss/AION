# 🐍 AION PyPI Deployment Guide

## 📋 Overview
This guide provides step-by-step instructions for deploying AION to PyPI (Python Package Index) so users can install it using `pip install aion-ai`.

## 🔧 Prerequisites

### 1. Install Build Tools
```bash
pip install --upgrade pip
pip install build twine setuptools wheel
```

### 2. Create PyPI Account
- Register at [PyPI.org](https://pypi.org/account/register/)
- Register at [TestPyPI.org](https://test.pypi.org/account/register/) (for testing)

### 3. Configure API Tokens
Create API tokens for secure authentication:
- Go to PyPI Account Settings → API tokens
- Create token with scope: "Entire account"
- Save the token securely

## 📦 Package Preparation

### 1. Verify Package Structure
```
AION/
├── aion/                    # Main package
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   ├── interfaces/
│   └── utils/
├── setup.py                 # Package setup
├── pyproject.toml          # Modern Python packaging
├── MANIFEST.in             # Package inclusion rules
├── README.md               # Package description
├── LICENSE                 # MIT License
├── CHANGELOG.md            # Version history
└── requirements.txt        # Dependencies
```

### 2. Update Version Numbers
Update version in both files:
- `setup.py`: `version="2.2.0"`
- `pyproject.toml`: `version = "2.2.0"`

### 3. Verify Dependencies
Ensure all dependencies are properly listed in:
- `setup.py` → `install_requires`
- `pyproject.toml` → `dependencies`

## 🧪 Testing Before Deployment

### 1. Build Package Locally
```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build the package
python -m build
```

### 2. Verify Package Contents
```bash
# Check generated files
ls -la dist/

# Verify package contents
tar -tzf dist/aion-ai-2.2.0.tar.gz
```

### 3. Test Installation Locally
```bash
# Install in development mode
pip install -e .

# Test commands
aion --help
aion-cli --help
aion-ai --help
```

## 🚀 Deployment Steps

### 1. Deploy to TestPyPI (Recommended First)
```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ aion-ai
```

### 2. Deploy to Production PyPI
```bash
# Upload to PyPI
python -m twine upload dist/*
```

### 3. Verify Deployment
```bash
# Install from PyPI
pip install aion-ai

# Test functionality
aion --version
```

## 🔐 Authentication Methods

### Method 1: API Token (Recommended)
```bash
# Set token as environment variable
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-api-token-here

# Upload
python -m twine upload dist/*
```

### Method 2: Interactive Login
```bash
# Twine will prompt for credentials
python -m twine upload dist/*
```

### Method 3: .pypirc Configuration
Create `~/.pypirc`:
```ini
[distutils]
index-servers = pypi testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-token-here
```

## 📋 Complete Deployment Script

Create `deploy_to_pypi.sh`:
```bash
#!/bin/bash
set -e

echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

echo "📦 Building package..."
python -m build

echo "🧪 Testing package..."
python -m twine check dist/*

echo "🚀 Uploading to TestPyPI..."
python -m twine upload --repository testpypi dist/*

echo "✅ TestPyPI deployment complete!"
echo "🔗 Check: https://test.pypi.org/project/aion-ai/"

read -p "Deploy to production PyPI? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Uploading to PyPI..."
    python -m twine upload dist/*
    echo "✅ PyPI deployment complete!"
    echo "🔗 Check: https://pypi.org/project/aion-ai/"
fi
```

## 📊 Post-Deployment Verification

### 1. Installation Test
```bash
# Create fresh virtual environment
python -m venv test_env
source test_env/bin/activate  # Linux/Mac
# test_env\Scripts\activate   # Windows

# Install from PyPI
pip install aion-ai

# Test functionality
aion --help
python -c "import aion; print('Import successful!')"
```

### 2. Monitor Package Stats
- Visit [PyPI Project Page](https://pypi.org/project/aion-ai/)
- Check download statistics
- Monitor user feedback and issues

## 🔄 Version Updates

For future releases:

1. **Update Version Numbers**:
   - `setup.py`
   - `pyproject.toml`
   - `CHANGELOG.md`

2. **Build and Test**:
   ```bash
   rm -rf build/ dist/ *.egg-info/
   python -m build
   python -m twine check dist/*
   ```

3. **Deploy**:
   ```bash
   python -m twine upload dist/*
   ```

## 🎯 User Installation Instructions

After successful deployment, users can install AION using:

```bash
# Install latest version
pip install aion-ai

# Install specific version
pip install aion-ai==2.2.0

# Install with development dependencies
pip install aion-ai[dev]

# Install with full features
pip install aion-ai[full]
```

## 🆘 Troubleshooting

### Common Issues:

1. **Version Already Exists**:
   - Increment version number
   - Cannot overwrite existing PyPI versions

2. **Authentication Failed**:
   - Verify API token
   - Check .pypirc configuration

3. **Package Build Errors**:
   - Check setup.py syntax
   - Verify MANIFEST.in includes

4. **Import Errors After Installation**:
   - Check entry points in setup.py
   - Verify package structure

## 📞 Support

- **PyPI Issues**: [PyPI Help](https://pypi.org/help/)
- **Packaging Guide**: [Python Packaging User Guide](https://packaging.python.org/)
- **AION Issues**: [GitHub Issues](https://github.com/AliPluss/AION/issues)

---

**🎉 Ready to deploy AION to PyPI!**

Users will be able to install with: `pip install aion-ai`
