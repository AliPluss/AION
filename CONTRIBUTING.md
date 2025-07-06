# 🤝 Contributing to AION

Thank you for your interest in contributing to AION! We welcome contributions from developers around the world, especially those who can help improve our multilingual support.

## 🌟 Ways to Contribute

- 🐛 **Bug Reports**: Report bugs and issues with detailed information
- 💡 **Feature Requests**: Suggest new features and improvements
- 📝 **Documentation**: Improve documentation and help guides
- 🔧 **Code**: Submit bug fixes and new features
- 🌍 **Translations**: Add or improve language support (Arabic, English, etc.)
- 🧩 **Plugins**: Create new plugins for the community
- 🎨 **UI/UX**: Improve interface design and user experience
- 🧪 **Testing**: Write tests and improve test coverage

## 🚀 Getting Started

### 1. Fork and Clone
```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/AliPluss/AION.git
cd AION
```

### 2. Set Up Development Environment
```bash
# Create virtual environment
python -m venv dev_env
source dev_env/bin/activate  # Windows: dev_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run setup script to create project structure
python setup_aion_fixed.py
```

### 3. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
# or
git checkout -b docs/improve-readme
```

## 📋 Development Guidelines

### Code Style
- Follow PEP 8 style guidelines
- Use type hints where possible
- Write docstrings for functions and classes
- Keep functions small and focused

### Code Formatting
```bash
# Format code
make format

# Check formatting
black --check .
isort --check-only .
```

### Linting
```bash
# Run linting
make lint

# Or manually
flake8 .
mypy . --ignore-missing-imports
```

### Testing
```bash
# Run tests
make test

# Run with coverage
make test-verbose

# Run specific test
pytest tests/test_specific.py
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: OS, Python version, AION version
6. **Logs**: Relevant error messages or logs

### Bug Report Template
```markdown
## Bug Description
Brief description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Environment
- OS: [e.g., Windows 10, Ubuntu 20.04]
- Python: [e.g., 3.9.7]
- AION: [e.g., 1.0.0]

## Additional Context
Any other context about the problem
```

## 💡 Feature Requests

When requesting features:

1. **Use Case**: Describe the use case
2. **Proposed Solution**: Your idea for implementation
3. **Alternatives**: Alternative solutions considered
4. **Additional Context**: Any other relevant information

## 🔧 Code Contributions

### Pull Request Process

1. **Create Issue**: Create an issue first (unless it's a small fix)
2. **Fork & Branch**: Fork the repo and create a feature branch
3. **Develop**: Write your code following our guidelines
4. **Test**: Ensure all tests pass
5. **Document**: Update documentation if needed
6. **Submit**: Create a pull request

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added (if applicable)
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## 🌍 Translation Contributions

### Adding a New Language

1. **Create Language File**: Copy `locales/en.json` to `locales/[lang_code].json`
2. **Translate Strings**: Translate all strings in the file
3. **Update Language List**: Add language to supported languages list
4. **Test**: Test the new language interface
5. **Submit**: Create a pull request

### Translation Guidelines
- Keep translations concise and clear
- Maintain the same tone as the original
- Test translations in the actual interface
- Consider cultural context

## 🧩 Plugin Development

### Creating a Plugin

1. **Plugin Structure**: Follow the plugin template
2. **Base Class**: Inherit from `BasePlugin`
3. **Metadata**: Include proper metadata
4. **Documentation**: Document your plugin
5. **Testing**: Test thoroughly

### Plugin Template
```python
from core.plugins import BasePlugin

class MyPlugin(BasePlugin):
    def __init__(self):
        super().__init__(
            name="My Plugin",
            version="1.0.0",
            description="Description of my plugin",
            author="Your Name"
        )
    
    def execute(self, command: str, args: list) -> str:
        # Plugin logic here
        return "Plugin result"
```

## 📚 Documentation

### Documentation Guidelines
- Use clear, simple language
- Include code examples
- Keep documentation up to date
- Use proper markdown formatting

### Building Documentation
```bash
# Build documentation
make docs

# Serve documentation locally
make docs-serve
```

## 🔒 Security

### Reporting Security Issues
- **DO NOT** create public issues for security vulnerabilities
- Email security issues to: security@aion-ai.com
- Include detailed information about the vulnerability
- Allow time for the issue to be addressed before disclosure

## 📞 Getting Help

- 💬 **Discord**: [Join our community](https://discord.gg/aion-ai)
- 📧 **Email**: dev@aion-ai.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/aion-ai/issues)

## 📄 License

By contributing to AION, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- CHANGELOG.md for significant contributions
- GitHub contributors page

---

Thank you for contributing to AION! 🚀
