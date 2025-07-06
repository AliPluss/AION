# 🔒 AION Security Guide

## GitHub Secrets Management

### 🔑 Required Secrets for AION

#### For PyPI Publishing (Optional)
```
PYPI_API_TOKEN - PyPI API token for package publishing
```

#### For AI Providers (Development)
```
OPENAI_API_KEY - OpenAI API key
ANTHROPIC_API_KEY - Claude API key  
GOOGLE_API_KEY - Gemini API key
DEEPSEEK_API_KEY - DeepSeek API key
```

### 🛡️ How to Add Secrets to GitHub

1. **Go to Repository Settings**
   - Navigate to your GitHub repository
   - Click on "Settings" tab
   - Go to "Secrets and variables" → "Actions"

2. **Add New Repository Secret**
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Your PyPI API token
   - Click "Add secret"

3. **Environment Protection (Recommended)**
   - Go to "Environments" in repository settings
   - Create "production" environment
   - Add protection rules:
     - Required reviewers
     - Wait timer
     - Deployment branches

### 🚫 What NOT to Do

#### ❌ Never commit these files:
```
.env
.env.local
.env.production
api_keys.txt
secrets.txt
credentials.json
*_token
*_key
*_secret
```

#### ❌ Never hardcode secrets in code:
```python
# DON'T DO THIS
api_key = "sk-1234567890abcdef"
token = "pypi-AgEIcHlwaS5vcmc..."

# DO THIS INSTEAD
import os
api_key = os.getenv("OPENAI_API_KEY")
token = os.getenv("PYPI_API_TOKEN")
```

## 🔐 Local Development Security

### Environment Variables
```bash
# Create .env file (already in .gitignore)
echo "OPENAI_API_KEY=your_key_here" > .env
echo "ANTHROPIC_API_KEY=your_key_here" >> .env
```

### Using python-dotenv
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment")
```

## 🛠️ CI/CD Security Best Practices

### 1. Separate Workflows
- ✅ **CI/CD Testing**: No secrets needed
- ✅ **Publishing**: Separate workflow with environment protection

### 2. Environment Protection
```yaml
# .github/workflows/publish.yml
jobs:
  publish:
    environment: production  # Requires approval
    steps:
      - name: Publish to PyPI
        env:
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
```

### 3. Conditional Execution
```yaml
# Only run on releases
on:
  release:
    types: [published]
```

### 4. Secret Scanning
```yaml
# Enable secret scanning in repository settings
# GitHub will automatically detect exposed secrets
```

## 🔍 Security Scanning

### Automated Security Checks
```yaml
# Already included in CI/CD
- name: Security scan with bandit
  run: python -m bandit -r . -f json -o bandit-report.json

- name: Check for vulnerabilities
  run: python -m safety check --json
```

### Manual Security Audit
```bash
# Check for hardcoded secrets
grep -r "api_key\|token\|secret\|password" --include="*.py" .

# Check for exposed files
find . -name "*.env*" -o -name "*_key*" -o -name "*_token*"

# Audit dependencies
pip-audit
```

## 🚨 Security Incident Response

### If API Key is Exposed:

1. **Immediate Actions:**
   - Revoke the exposed key immediately
   - Generate new API key
   - Update GitHub secrets

2. **Investigation:**
   - Check git history: `git log --all --grep="api_key"`
   - Check GitHub commits for exposed secrets
   - Review access logs if available

3. **Prevention:**
   - Update .gitignore
   - Add pre-commit hooks
   - Enable secret scanning

### Pre-commit Hook for Security
```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
EOF

# Install hooks
pre-commit install
```

## 📋 Security Checklist

### Before Committing:
- [ ] No API keys in code
- [ ] .env files in .gitignore
- [ ] Secrets use environment variables
- [ ] No hardcoded credentials

### Before Deploying:
- [ ] All secrets in GitHub Secrets
- [ ] Environment protection enabled
- [ ] Security scanning passed
- [ ] Dependencies audited

### Regular Maintenance:
- [ ] Rotate API keys quarterly
- [ ] Review access permissions
- [ ] Update security dependencies
- [ ] Monitor for exposed secrets

## 🎯 AION Specific Security

### AI Provider Keys
```python
# config/ai_providers.py
import os

PROVIDERS = {
    "openai": {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "base_url": "https://api.openai.com/v1"
    },
    "anthropic": {
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
        "base_url": "https://api.anthropic.com"
    }
}
```

### User Data Protection
```python
# Encrypt sensitive user data
from cryptography.fernet import Fernet

def encrypt_user_data(data: str) -> bytes:
    key = os.getenv("ENCRYPTION_KEY")
    f = Fernet(key)
    return f.encrypt(data.encode())
```

### Secure Configuration
```python
# Use pydantic for validation
from pydantic import BaseSettings, SecretStr

class Settings(BaseSettings):
    openai_api_key: SecretStr
    anthropic_api_key: SecretStr
    
    class Config:
        env_file = ".env"
```

## 🔗 Additional Resources

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [OWASP Security Guidelines](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.org/dev/security/)
- [PyPI Security](https://pypi.org/help/#apitoken)

---

**🛡️ Remember: Security is not optional - it's essential for protecting users and maintaining trust!**
