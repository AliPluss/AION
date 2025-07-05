# 🤖 AION - AI Operating Node

[![PyPI version](https://badge.fury.io/py/aion-ai.svg)](https://badge.fury.io/py/aion-ai)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/yourusername/aion-ai/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/yourusername/aion-ai/actions)
[![codecov](https://codecov.io/gh/yourusername/aion-ai/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/aion-ai)

**AION (AI Operating Node)** is an advanced multilingual terminal-based AI assistant that supports multiple programming languages and AI providers with beautiful interfaces and comprehensive features.

## 🌟 Key Features

### 🧠 **Advanced AI Integration**
- Multiple AI providers support (OpenAI, DeepSeek, OpenRouter, Gemini)
- Code generation and optimization
- Code explanation and analysis
- Multi-language translation capabilities

### 💻 **Multi-Language Code Execution**
- **Python** - Direct execution with library support
- **JavaScript** - Node.js and browser execution
- **Rust** - Compile and run Rust projects
- **C++** - Compile and execute C++ programs
- **Shell Scripts** - System command execution

### 🔐 **Dynamic Security System**
- Secure session management
- Sensitive data encryption
- Suspicious activity monitoring
- Advanced file and folder protection

### 🧩 **Flexible Plugin System**
- Custom plugin development
- Ready-to-use plugin library
- Dynamic plugin management
- Comprehensive developer API

### 🌐 **Multiple Interfaces**
- **CLI** - Traditional command-line interface
- **TUI** - Advanced interactive text interface
- **Web** - Web interface for remote access

### 🌍 **Multilingual Support**
- Arabic (with full RTL text support)
- English
- French
- German
- Spanish
- Chinese
- Norwegian

## 🚀 Quick Start

### Installation

#### From PyPI (Recommended)
```bash
pip install aion-ai
```

#### From Source
```bash
git clone https://github.com/yourusername/aion-ai.git
cd aion-ai
pip install -e .
```

#### Using Docker
```bash
docker pull aion-ai:latest
docker run -it aion-ai:latest
```

### Basic Usage

#### Command Line Interface
```bash
# Start AION CLI
aion-cli

# Start with Arabic interface
aion-ar

# Start web interface
aion web --host 0.0.0.0 --port 8000
```

#### Quick Commands
```bash
# Execute Python code
aion> execute python print("Hello, AION!")

# Translate text
aion> translate ar Hello World

# Get help
aion> help

# Change language
aion> change-language
```

## 📦 Installation Methods

### 1. PyPI Installation
```bash
# Install latest stable version
pip install aion-ai

# Install with web interface support
pip install aion-ai[web]

# Install with development tools
pip install aion-ai[dev]

# Install everything
pip install aion-ai[full]
```

### 2. Development Installation
```bash
git clone https://github.com/yourusername/aion-ai.git
cd aion-ai
make setup
```

### 3. Docker Installation
```bash
# Production
docker-compose up -d

# Development
docker-compose --profile dev up -d
```

## 🎯 Usage Examples

### Code Execution
```python
# Python example
aion> execute python
import requests
response = requests.get('https://api.github.com')
print(f"Status: {response.status_code}")
```

### AI-Powered Features
```bash
# Generate code
aion> generate python function to calculate fibonacci

# Explain code
aion> explain def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)

# Translate
aion> translate ar "Hello, how are you?"
```

### Plugin Management
```bash
# List plugins
aion> plugins

# Install plugin
aion> plugin install calculator

# Use plugin
aion> calc 2 + 2 * 3
```

## 🔧 Configuration

### AI Provider Setup
1. Copy the configuration template:
```bash
cp config/ai_config_template.json ~/.aion/config/ai_config.json
```

2. Edit the configuration file:
```json
{
  "openai": {
    "enabled": true,
    "api_key": "your-openai-api-key-here",
    "model": "gpt-3.5-turbo"
  }
}
```

### Language Configuration
```bash
# Set default language
aion config set language ar

# Available languages: en, ar, fr, de, es, zh, no
```

## 🏗️ Architecture

```
AION/
├── core/                   # Core functionality
│   ├── ai_providers.py     # AI provider integrations
│   ├── security.py         # Security management
│   ├── executor.py         # Code execution engine
│   └── plugins.py          # Plugin system
├── interfaces/             # User interfaces
│   ├── cli.py             # Command-line interface
│   ├── tui.py             # Text user interface
│   └── web.py             # Web interface
├── utils/                  # Utilities
│   ├── translator.py       # Translation system
│   ├── helpers.py          # Helper functions
│   └── arabic_support.py   # Arabic language support
├── locales/               # Language files
├── config/                # Configuration templates
├── plugins/               # Built-in plugins
└── templates/             # Web templates
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage
make test-verbose

# Run specific test
pytest tests/test_core.py

# Run integration tests
python test_aion.py
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone repository
git clone https://github.com/yourusername/aion-ai.git
cd aion-ai

# Setup development environment
make setup

# Run in development mode
make run-dev
```

### Code Quality
```bash
# Format code
make format

# Run linting
make lint

# Type checking
make type-check

# Security check
make security
```

## 📚 Documentation

- [User Guide](docs/user-guide.md)
- [API Reference](docs/api-reference.md)
- [Plugin Development](docs/plugin-development.md)
- [Configuration Guide](docs/configuration.md)

## 🔒 Security

AION takes security seriously. Please report security vulnerabilities to [security@aion-ai.com](mailto:security@aion-ai.com).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Powered by [Typer](https://github.com/tiangolo/typer) for CLI framework
- Web interface built with [FastAPI](https://github.com/tiangolo/fastapi)
- TUI powered by [Textual](https://github.com/Textualize/textual)

## 📞 Support

- 📧 Email: [support@aion-ai.com](mailto:support@aion-ai.com)
- 💬 Discord: [Join our community](https://discord.gg/aion-ai)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/aion-ai/issues)
- 📖 Wiki: [GitHub Wiki](https://github.com/yourusername/aion-ai/wiki)

---

<div align="center">
  <strong>Made with ❤️ by the AION Development Team</strong>
</div>
