# 🎯 AION - AI Operating Node | Intelligent Operating Node

<div align="center">

![AION Logo](https://img.shields.io/badge/AION-AI%20Operating%20Node-blue?style=for-the-badge&logo=terminal)
![Version](https://img.shields.io/badge/version-2.2.0-green?style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/aion-ai?style=for-the-badge&logo=pypi)
![License](https://img.shields.io/badge/license-MIT-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.10+-blue?style=for-the-badge&logo=python)

[![CI/CD Pipeline](https://github.com/AliPluss/AION/actions/workflows/ci.yml/badge.svg)](https://github.com/AliPluss/AION/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)

**Next-Generation AI-Powered Terminal Assistant

[English](#english) | [العربية](#arabic)

</div>

---

## English

**AION** is a revolutionary AI-powered terminal assistant that transforms your command line experience with intelligent automation, beautiful animated interfaces, and comprehensive multilingual support. Built with Python, enhanced with Rust performance, and featuring next-generation terminal UI.

## 🌟 Overview

AION combines the power of multiple AI providers with advanced security, professional-grade features, and an innovative animated terminal interface. Designed for developers, researchers, and enterprises requiring sophisticated AI assistance with cultural sensitivity and multilingual support.

## ✨ Core Features

### 🧠 AI & Intelligence
- **Multi-Provider Support**: OpenAI, DeepSeek, OpenRouter, Google Gemini with automatic failover
- **Dynamic Model Selection**: Choose and switch between different AI models seamlessly
- **Conversation Management**: Persistent conversation history with context awareness
- **Response Caching**: Intelligent caching system for improved performance and cost optimization
- **Usage Analytics**: Comprehensive tracking of tokens, costs, and performance metrics

### 🌍 Multilingual Excellence
- **7 Languages Supported**: Arabic (العربية), English, French (Français), German (Deutsch), Spanish (Español), Chinese (中文), Norwegian (Norsk)
- **RTL Support**: Full right-to-left text support for Arabic interface
- **Dynamic Language Switching**: Change interface language on-the-fly
- **Localized Content**: All UI elements, messages, and documentation available in multiple languages

### 🔒 Advanced Security
- **Dynamic Security Protocols**: HMAC+AES encryption with minute-based parameter rotation
- **Real-time Threat Monitoring**: Continuous system monitoring and threat assessment
- **Secure API Key Management**: Encrypted storage and handling of sensitive credentials
- **Audit Logging**: Comprehensive security event logging and monitoring
- **Sandbox Execution**: Isolated code execution environment with Docker integration

### 🚀 System Integration
- **Email System**: Full SMTP/IMAP integration with OTP authentication
- **External Platforms**: GitHub, Slack, Notion, Google Drive integrations
- **Voice Control**: Speech-to-text and text-to-speech with multi-language support
- **File Management**: Advanced file operations with encryption and monitoring
- **Task Management**: Professional task scheduling and execution system
- **Code Editor**: Integrated code editor with syntax highlighting for 23+ languages

### 🔧 Professional Tools
- **Advanced Export System**: 13+ export formats including PDF, Excel, Word, PowerPoint
- **Automation Recipes**: Create and execute complex automation workflows
- **Plugin Architecture**: Extensible system with custom plugin support
- **Performance Monitoring**: Real-time system performance and resource tracking
- **Comprehensive Testing**: 100+ automated tests with CI/CD pipeline integration

### 🎮 Pure Arrow-Key Navigation System
- **Zero Manual Input**: No typing language codes, numbers, or commands for navigation
- **Full Arrow Key Support**: ↑↓←→ navigation throughout all interfaces
- **Animated Visual Feedback**: Real-time animations show selection states
- **Inline Icon Integration**: Icons and text perfectly aligned in single lines
- **Professional UX**: Consistent interaction patterns across all menus

#### Navigation Controls:
- **↑↓ Arrow Keys**: Navigate through menu items
- **←→ Arrow Keys**: Navigate between sections
- **Enter Key**: Select highlighted item
- **Escape Key**: Cancel/go back
- **Q Key**: Quit application

#### Animation System:
- **Pulse**: 🧠 OpenAI, English language
- **Orbit**: 🛰️ DeepSeek provider
- **Bounce**: 🇮🇶 Arabic language (RTL)
- **Wiggle**: 🧩 Plugin manager
- **Glow**: ⚡ JavaScript, security warnings
- **Ripple**: 🌐 Google provider

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (Required)
- **Git** for cloning the repository
- **Docker** (Optional, for containerized deployment)
- **Virtual Environment** (Recommended)

### Installation

#### Method 1: PyPI Installation (Recommended) 🐍

```bash
# Install AION from PyPI
pip install aion-ai

# Start AION
aion

# Or use alternative commands
aion-cli
aion-ai
```

#### Method 2: Standard Installation

```bash
# Clone the repository
git clone https://github.com/AliPluss/AION.git
cd AION

# Create and activate virtual environment
python -m venv aion_env
source aion_env/bin/activate  # On Windows: aion_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-integrations.txt  # For full features

# Start AION
python main.py start
```

#### Method 3: Docker Deployment

```bash
# Clone and build
git clone https://github.com/AliPluss/AION.git
cd AION

# Build and run with Docker
docker-compose up --build

# Or use Docker directly
docker build -t aion .
docker run -it --name aion-container aion
```

#### Method 4: Development Setup

```bash
# Clone repository
git clone https://github.com/AliPluss/AION.git
cd AION

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/ -v

# Start with development features
python main.py start --dev-mode

# Quick test
python start_aion_en.py
```

### Testing & Verification

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/test_basic.py -v      # Basic functionality
python -m pytest tests/test_imports.py -v   # Import validation

# Quick health check
python start_aion_en.py
```

## 🎯 Usage Examples

### Basic AI Interaction

```bash
# Start AION
python main.py start

# Select language (Arabic/English/etc.)
# Choose AI Assistant mode
# Enter your questions or requests
```

### Advanced Features

```bash
# Execute code with syntax highlighting
python main.py execute --language python --file script.py

# Manage tasks and scheduling
python main.py task create --name "backup" --schedule "daily"

# Export conversation to PDF
python main.py export --format pdf --output conversation.pdf

# Voice control (if enabled)
python main.py voice --enable --language ar
```

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.10 or higher
- **Operating System**: Windows 10+, macOS 10.15+, Linux (Ubuntu 18.04+)
- **Memory**: 1GB RAM minimum (2GB recommended)
- **Storage**: 500MB free space
- **Network**: Internet connection for AI providers

### Recommended Requirements
- **Python**: 3.11+ for optimal performance
- **Memory**: 4GB RAM for full features
- **Storage**: 2GB for plugins and cache
- **Docker**: For containerized deployment

## 🔧 Configuration

### AI Provider Setup

1. **OpenAI Configuration**:
   ```bash
   # Set your OpenAI API key
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. **DeepSeek Configuration**:
   ```bash
   # Set your DeepSeek API key
   export DEEPSEEK_API_KEY="your-api-key-here"
   ```

3. **Google Gemini Configuration**:
   ```bash
   # Set your Gemini API key
   export GEMINI_API_KEY="your-api-key-here"
   ```

### Language Configuration

```bash
# Set default language
python main.py config set --language ar  # Arabic
python main.py config set --language en  # English
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/AliPluss/AION.git
cd AION

# Create virtual environment
python -m venv aion_dev
source aion_dev/bin/activate  # On Windows: aion_dev\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-integrations.txt

# Install pre-commit hooks
pre-commit install

# Run tests
python -m pytest tests/ -v --cov=core --cov=interfaces --cov=utils

# Run linting and formatting
python -m flake8 .
python -m black .
python -m isort .
```

### Project Architecture

```
AION/
├── 📁 core/                    # Core system modules
│   ├── ai_providers.py         # AI provider integrations
│   ├── security.py             # Security and encryption
│   ├── task_manager.py         # Task scheduling and execution
│   ├── automation_recipes.py   # Automation workflows
│   ├── export_system.py        # Export functionality
│   └── ...
├── 📁 interfaces/              # User interfaces
│   ├── cli.py                  # Command line interface
│   ├── tui.py                  # Terminal user interface
│   └── web.py                  # Web interface
├── 📁 integrations/            # External integrations
│   ├── email_system.py         # Email integration
│   ├── github_integration.py   # GitHub integration
│   ├── slack_integration.py    # Slack integration
│   └── ...
├── 📁 utils/                   # Utility modules
│   ├── translator.py           # Multilingual support
│   ├── helpers.py              # Common utilities
│   └── arabic_support.py       # Arabic language support
├── 📁 locales/                 # Translation files
│   ├── ar.json                 # Arabic translations
│   ├── en.json                 # English translations
│   └── ...
├── 📁 config/                  # Configuration files
├── 📁 templates/               # Web templates
├── 📁 tests/                   # Test suite
├── 📁 plugins/                 # Plugin system
├── 📁 monitoring/              # Performance monitoring
├── 📁 file_system/             # File operations
├── 📁 shell/                   # Shell integration
└── 📁 editor/                  # Code editor
```

## 🌍 Language Support

AION supports 7 languages with native interface translation:

- 🇺🇸 English (Default)
- 🇮🇶 Arabic (العربية)
- 🇫🇷 French (Français)
- 🇩🇪 German (Deutsch)
- 🇪🇸 Spanish (Español)
- 🇨🇳 Chinese (中文)
- 🇳🇴 Norwegian (Norsk)

## 🤖 AI Providers

- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Anthropic**: Claude 3 (Opus, Sonnet, Haiku)
- **Google**: Gemini Pro, Gemini Pro Vision
- **DeepSeek**: DeepSeek Chat, DeepSeek Coder
- **OpenRouter**: Access to multiple models

## 🚀 Advanced Features

### 🔐 Security Features
- **Dynamic Encryption**: HMAC+AES encryption with minute-based rotation
- **Threat Monitoring**: Real-time security assessment and protection
- **Secure Storage**: Encrypted API key and sensitive data management
- **Audit Logging**: Comprehensive security event tracking
- **Sandbox Execution**: Isolated code execution environment
- **Rate Limiting**: Intelligent request throttling and protection
- **Input Validation**: Comprehensive input sanitization and validation

### 🌐 Integration Capabilities
- **Email System**: Full SMTP/IMAP with OTP authentication
- **GitHub Integration**: Repository management and collaboration
- **Slack Integration**: Team communication and notifications
- **Google Drive**: File storage and sharing
- **Notion Integration**: Documentation and knowledge management

### 🎯 Automation & Productivity
- **Task Scheduling**: Cron-like task scheduling with dependencies
- **Automation Recipes**: Complex workflow automation
- **Voice Control**: Speech-to-text and text-to-speech
- **Code Editor**: Integrated editor with 23+ language support
- **Export System**: 13+ export formats including PDF, Excel, Word

## 🔧 Troubleshooting

### Common Issues

**Installation Issues**:
```bash
# If pip install fails
python -m pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

# For Windows users with path issues
set PATH=%PATH%;C:\Python310\Scripts
```

**API Key Issues**:
```bash
# Verify API keys are set correctly
python main.py config check

# Reset configuration
python main.py config reset
```

**Language Issues**:
```bash
# Fix Arabic display issues
pip install python-bidi arabic-reshaper

# Reset language settings
python main.py language reset
```

### Performance Optimization

```bash
# Enable performance mode
python main.py config set --performance-mode high

# Clear cache
python main.py cache clear

# Optimize database
python main.py optimize
```

## 📊 Monitoring & Analytics

AION includes comprehensive monitoring capabilities:

- **Performance Metrics**: CPU, memory, and response time tracking
- **Usage Analytics**: Token usage, cost tracking, and provider statistics
- **Error Monitoring**: Comprehensive error logging and reporting
- **Health Checks**: Automated system health monitoring

## 🔌 Plugin Development

### Creating Custom Plugins

```python
# Example plugin structure
from core.plugins import BasePlugin

class MyPlugin(BasePlugin):
    def __init__(self):
        super().__init__("my_plugin", "1.0.0")

    def execute(self, command: str, args: dict):
        # Plugin logic here
        return {"status": "success", "result": "Plugin executed"}
```

### Plugin Installation

```bash
# Install plugin
python main.py plugin install --path /path/to/plugin

# List plugins
python main.py plugin list

# Enable/disable plugins
python main.py plugin enable my_plugin
python main.py plugin disable my_plugin
```

## 📚 Documentation

- [Installation Guide](INSTALLATION.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [Security Guide](SECURITY.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python 3.8+
- Uses Rich for beautiful terminal output
- Powered by FastAPI for web interface
- Textual for TUI components

## 📞 Support

- 🐛 [Report Issues](https://github.com/AliPluss/aion-ai/issues)
- 💬 [Discussions](https://github.com/AliPluss/aion-ai/discussions)
- 📧 Email: project.django.rst@gmail.com
- 🌐 Repository: https://github.com/AliPluss/AION

---

**Made with ❤️ by the AION Team**
