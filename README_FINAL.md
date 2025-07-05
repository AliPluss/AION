# 🤖 AION - AI Operating Node

[![PyPI version](https://badge.fury.io/py/aion-ai.svg)](https://badge.fury.io/py/aion-ai)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AION (AI Operating Node)** is an advanced multilingual terminal-based AI assistant that supports multiple programming languages and AI providers with beautiful interfaces and comprehensive features.

## 🌟 Key Features

- 🌍 **Multilingual Support**: 7 languages with beautiful UI (Arabic, English, French, German, Spanish, Chinese, Norwegian)
- 🤖 **AI Integration**: Multiple AI providers (OpenAI, DeepSeek, OpenRouter, Gemini)
- 💻 **Code Execution**: Python, JavaScript, Rust, C++
- 🔒 **Security**: Advanced security and session management
- 🧩 **Plugin System**: Extensible plugin architecture
- 🌐 **Multiple Interfaces**: CLI, TUI, and Web interfaces
- 🎨 **Beautiful UI**: Rich terminal interface with colors and emojis

## 🚀 Quick Installation

### Method 1: From PyPI (Recommended)
```bash
pip install aion-ai
```

### Method 2: From Source
```bash
git clone https://github.com/yourusername/aion-ai.git
cd aion-ai
python install.py
```

### Method 3: Using Installation Script
```bash
# Download and run
python install.py
```

## 🎯 Quick Start

### Start AION
```bash
# English interface
aion-cli

# Arabic interface  
aion-ar

# Direct CLI
aion cli

# Web interface
aion web --host 0.0.0.0 --port 8000

# TUI interface
aion tui
```

### Basic Commands
```bash
# Execute code
aion> execute python print("Hello, AION!")

# Translate text
aion> translate ar "Hello World"

# Get help
aion> help

# Change language
aion> change-language

# Show system info
aion> system-info
```

## 📦 Installation Options

### Full Installation
```bash
pip install aion-ai[full]
```

### Web Interface Only
```bash
pip install aion-ai[web]
```

### Development Installation
```bash
pip install aion-ai[dev]
```

## 🔧 Configuration

### AI Provider Setup
1. Create configuration directory:
```bash
mkdir -p ~/.aion/config
```

2. Copy and edit configuration:
```bash
cp config/ai_config_template.json ~/.aion/config/ai_config.json
```

3. Add your API keys:
```json
{
  "openai": {
    "enabled": true,
    "api_key": "your-api-key-here",
    "model": "gpt-3.5-turbo"
  }
}
```

## 🌍 Supported Languages

| Language | Code | Status |
|----------|------|--------|
| العربية | ar | ✅ Full RTL support |
| English | en | ✅ Default |
| Français | fr | ✅ Complete |
| Deutsch | de | ✅ Complete |
| Español | es | ✅ Complete |
| 中文 | zh | ✅ Simplified |
| Norsk | no | ✅ Complete |

## 🧪 Testing

### Quick Test
```bash
python quick_test.py
```

### Full Test Suite
```bash
python test_aion.py
```

### Manual Testing
```bash
# Test English interface
python start_aion_en.py

# Test Arabic interface
python start_aion.py

# Test direct execution
python main.py cli
```

## 🏗️ Building from Source

### Prerequisites
- Python 3.8+
- pip
- git

### Build Steps
```bash
# Clone repository
git clone https://github.com/yourusername/aion-ai.git
cd aion-ai

# Install build dependencies
pip install build twine wheel

# Build package
python build_release.py

# Install locally
pip install dist/aion_ai-1.0.0-py3-none-any.whl
```

## 🐳 Docker Support

### Run with Docker
```bash
# Build image
docker build -t aion-ai .

# Run container
docker run -it aion-ai

# Web interface
docker run -p 8000:8000 aion-ai python main.py web
```

### Docker Compose
```bash
# Production
docker-compose up -d

# Development
docker-compose --profile dev up -d
```

## 📚 Documentation

- [User Guide](docs/user-guide.md)
- [API Reference](docs/api-reference.md)
- [Plugin Development](docs/plugin-development.md)
- [Configuration Guide](docs/configuration.md)

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/yourusername/aion-ai.git
cd aion-ai
make setup
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Powered by [Typer](https://github.com/tiangolo/typer) for CLI framework
- Web interface built with [FastAPI](https://github.com/tiangolo/fastapi)
- TUI powered by [Textual](https://github.com/Textualize/textual)

## 📞 Support

- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/aion-ai/issues)
- 📧 Email: support@aion-ai.com
- 📖 Wiki: [GitHub Wiki](https://github.com/yourusername/aion-ai/wiki)

---

<div align="center">
  <strong>Made with ❤️ by the AION Development Team</strong>
</div>
