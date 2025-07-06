# 🧠 AION - AI Operating Node

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/AliPluss/AION)
[![Version](https://img.shields.io/badge/Version-2.0.0-brightgreen.svg)](https://github.com/AliPluss/AION/releases)
[![Arabic Support](https://img.shields.io/badge/Arabic-Supported-orange.svg)](https://github.com/AliPluss/AION)

**AION (AI Operating Node)** is an advanced terminal-based AI assistant system that supports multiple programming languages, AI providers, and offers dynamic security features with an interactive CLI/TUI/Web interface. Built with full Arabic language support and multilingual capabilities.

## 🌟 Key Features

### 🤖 Advanced AI Integration
- **Multiple AI Providers**: OpenAI GPT-4/3.5, DeepSeek, OpenRouter, Google Gemini
- **Smart Context Management**: Maintains conversation history and context
- **Dynamic Model Selection**: Switch between different AI models seamlessly
- **Streaming Responses**: Real-time AI responses with progress indicators
- **Custom System Prompts**: Personalized AI behavior

### 💻 Multi-Language Code Execution
- **Supported Languages**: Python, Rust, C++, JavaScript, TypeScript, Go, Java, C#
- **Secure Sandboxing**: Safe code execution environment with resource limits
- **Real-time Output**: Live execution feedback with syntax highlighting
- **Error Handling**: Comprehensive error reporting and debugging assistance
- **Package Management**: Automatic dependency installation

### 🌍 Comprehensive Multilingual Support
- **7 Languages**: Arabic (العربية), English, Norwegian (Norsk), German (Deutsch), French (Français), Chinese (中文), Spanish (Español)
- **RTL Support**: Full right-to-left text support for Arabic with proper formatting
- **Dynamic Language Switching**: Change interface language without restart
- **Localized UI**: Fully translated interface elements and messages
- **Cultural Adaptation**: Region-specific formatting and conventions

### 🔒 Enterprise-Grade Security
- **Dynamic Security Levels**: Adjustable security policies (Low, Medium, High, Custom)
- **Code Sandboxing**: Isolated execution environment with containerization
- **Permission Management**: Granular access control for system resources
- **Audit Logging**: Complete activity tracking and compliance reporting
- **Encryption**: End-to-end encryption for sensitive data

### 🔌 Extensible Plugin System
- **Hot-loading Plugins**: Load and unload plugins without system restart
- **Plugin Manager**: Built-in plugin management with dependency resolution
- **API Integration**: Connect to external services and APIs
- **Custom Commands**: Create custom commands and workflows
- **Plugin Marketplace**: Community-driven plugin ecosystem

### 🎨 Multiple Interface Options
- **CLI**: Rich command-line interface with auto-completion
- **TUI**: Beautiful terminal user interface with Textual framework
- **Web Interface**: Modern FastAPI-based web dashboard
- **Voice Control**: Speech recognition and text-to-speech synthesis
- **API Endpoints**: RESTful API for integration

## 🚀 Quick Installation & Setup

### Prerequisites
- **Python**: 3.10 or higher
- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 2GB free space

### Automated Installation

1. **Clone the repository**:
```bash
git clone https://github.com/AliPluss/AION.git
cd AION
```

2. **Run the automated setup**:
```bash
python setup_aion_fixed.py
```

3. **Navigate to the project and start**:
```bash
cd aion_project
python main.py start
```

### Manual Installation

1. **Create virtual environment**:
```bash
python -m venv aion_env
source aion_env/bin/activate  # On Windows: aion_env\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure settings**:
```bash
cp config/config_template.json config/config.json
# Edit config.json with your API keys and preferences
```

## 📦 Complete Dependencies List

### Core Dependencies (Auto-installed)
```txt
# Terminal & UI Framework
rich>=13.0.0              # Beautiful terminal formatting and colors
typer>=0.9.0              # Modern CLI framework with type hints
textual>=0.40.0           # Advanced TUI framework
click>=8.0.0              # Command line interface creation toolkit

# Web Framework
fastapi>=0.100.0          # Modern web framework for APIs
uvicorn>=0.23.0           # Lightning-fast ASGI server
jinja2>=3.1.0             # Template engine for web interface
python-multipart>=0.0.6   # Form data parsing

# AI & HTTP
openai>=1.0.0             # OpenAI API client
anthropic>=0.7.0          # Claude AI API client
google-generativeai>=0.3.0 # Google Gemini API client
requests>=2.31.0          # HTTP library for API calls
aiohttp>=3.8.0            # Async HTTP client/server

# Data & Configuration
pydantic>=2.0.0           # Data validation using Python type hints
python-dotenv>=1.0.0      # Load environment variables from .env
pyyaml>=6.0               # YAML parser and emitter
toml>=0.10.2              # TOML parser

# File & System Operations
aiofiles>=23.0.0          # Async file operations
watchdog>=3.0.0           # File system event monitoring
psutil>=5.9.0             # System and process utilities
pathlib2>=2.3.7           # Object-oriented filesystem paths

# Security & Encryption
cryptography>=41.0.0      # Cryptographic recipes and primitives
bcrypt>=4.0.0             # Password hashing
jwt>=1.3.1                # JSON Web Token implementation

# Async & Concurrency
asyncio>=3.4.3            # Asynchronous I/O
concurrent-futures>=3.1.1  # High-level interface for asynchronously executing callables
```

### Optional Dependencies
```txt
# Voice Features
speech-recognition>=3.10.0 # Speech recognition library
pyttsx3>=2.90             # Text-to-speech conversion
pyaudio>=0.2.11           # Audio I/O library

# Advanced AI Providers
deepseek-api>=1.0.0       # DeepSeek AI API client
cohere>=4.0.0             # Cohere AI API client
together>=0.2.0           # Together AI API client

# Development & Testing
pytest>=7.0.0             # Testing framework
pytest-asyncio>=0.21.0    # Async testing support
black>=23.0.0             # Code formatter
flake8>=6.0.0             # Code linter
mypy>=1.0.0               # Static type checker

# Database (Optional)
sqlalchemy>=2.0.0         # SQL toolkit and ORM
sqlite3                   # Built-in SQLite support
redis>=4.0.0              # Redis client (for caching)

# Monitoring & Logging
loguru>=0.7.0             # Advanced logging
prometheus-client>=0.17.0  # Metrics collection
```

## 🎯 Usage Examples

### Interactive Terminal Mode
```bash
# Start the main interactive interface
python main.py start

# Quick AI chat
python main.py ai

# Show version and system info
python main.py version

# Display help
python main.py --help
```

### Web Interface
```bash
# Start web server on default port (8000)
python main.py web

# Start on custom port with specific host
python main.py web --host 0.0.0.0 --port 3000

# Enable debug mode
python main.py web --debug
```

### Voice Control
```bash
# Start voice recognition mode
python main.py voice

# Voice with specific language
python main.py voice --lang ar  # Arabic voice commands
```

### Code Execution
```bash
# Execute Python code
python main.py exec --lang python --code "print('Hello AION!')"

# Execute from file
python main.py exec --file script.py

# Interactive code session
python main.py repl --lang python
```

### Plugin Management
```bash
# List available plugins
python main.py plugins list

# Install plugin
python main.py plugins install plugin_name

# Enable/disable plugin
python main.py plugins enable plugin_name
python main.py plugins disable plugin_name
```

## ⚙️ Configuration Guide

### Basic Configuration (`config/config.json`)
```json
{
  "app": {
    "name": "AION",
    "version": "2.0.0",
    "language": "ar",           // Default: Arabic
    "theme": "dark",            // dark, light, auto
    "auto_save": true,
    "session_timeout": 3600
  },
  "ai": {
    "default_provider": "openai",
    "providers": {
      "openai": {
        "api_key": "your-openai-api-key",
        "model": "gpt-4",
        "max_tokens": 2000,
        "temperature": 0.7
      },
      "deepseek": {
        "api_key": "your-deepseek-api-key",
        "model": "deepseek-chat",
        "max_tokens": 1500
      },
      "gemini": {
        "api_key": "your-gemini-api-key",
        "model": "gemini-pro"
      }
    }
  },
  "security": {
    "level": "medium",          // low, medium, high, custom
    "sandbox_enabled": true,
    "max_execution_time": 30,
    "allowed_imports": ["os", "sys", "json"],
    "blocked_functions": ["exec", "eval"]
  },
  "features": {
    "voice_enabled": true,
    "web_interface": true,
    "plugins_enabled": true,
    "export_enabled": true,
    "auto_completion": true
  },
  "interface": {
    "cli": {
      "prompt_style": "rich",
      "auto_suggest": true,
      "history_size": 1000
    },
    "web": {
      "host": "127.0.0.1",
      "port": 8000,
      "cors_enabled": true
    }
  }
}
```

### Environment Variables (`.env`)
```env
# AI Provider API Keys
OPENAI_API_KEY=your-openai-key
DEEPSEEK_API_KEY=your-deepseek-key
GEMINI_API_KEY=your-gemini-key
ANTHROPIC_API_KEY=your-claude-key

# Application Settings
AION_DEBUG=false
AION_LOG_LEVEL=INFO
AION_DATA_DIR=./data
AION_CACHE_DIR=./cache

# Security Settings
AION_SECRET_KEY=your-secret-key
AION_ENCRYPTION_KEY=your-encryption-key

# Database (Optional)
DATABASE_URL=sqlite:///aion.db
REDIS_URL=redis://localhost:6379
```

### Language Configuration
Each language has its own JSON file in `locales/`:

```json
// locales/ar.json (Arabic)
{
  "welcome": "مرحباً بك في AION",
  "ai_assistant": "مساعد الذكاء الاصطناعي",
  "code_execution": "تنفيذ الكود",
  "voice_mode": "الوضع الصوتي",
  "settings": "الإعدادات",
  "help": "المساعدة",
  "exit": "خروج",
  "error_occurred": "حدث خطأ: {error}",
  "processing": "جاري المعالجة...",
  "completed": "تم بنجاح"
}
```

## 🏗️ Architecture & Development

### Project Structure
```
AION/
├── 📁 core/                    # Core system components
│   ├── 🐍 ai_providers.py      # AI provider implementations
│   ├── 🐍 executor.py          # Code execution engine
│   ├── 🐍 security.py          # Security and sandboxing
│   ├── 🐍 plugins.py           # Plugin system management
│   └── 🐍 __init__.py
├── 📁 interfaces/              # User interface implementations
│   ├── 🐍 cli.py               # Command-line interface
│   ├── 🐍 tui.py               # Terminal user interface
│   ├── 🐍 web.py               # Web interface (FastAPI)
│   └── 🐍 __init__.py
├── 📁 locales/                 # Internationalization files
│   ├── 🌐 ar.json              # Arabic translations
│   ├── 🌐 en.json              # English translations
│   ├── 🌐 de.json              # German translations
│   ├── 🌐 fr.json              # French translations
│   ├── 🌐 no.json              # Norwegian translations
│   ├── 🌐 zh.json              # Chinese translations
│   └── 🌐 es.json              # Spanish translations
├── 📁 plugins/                 # Plugin directory
│   ├── 🔌 example_plugin.py    # Example plugin implementation
│   └── 📁 __pycache__/
├── 📁 utils/                   # Utility functions
│   ├── 🐍 arabic_support.py    # Arabic text processing
│   ├── 🐍 translator.py        # Translation utilities
│   ├── 🐍 helpers.py           # General helper functions
│   └── 🐍 __init__.py
├── 📁 config/                  # Configuration files
│   ├── ⚙️ config.json          # Main configuration
│   ├── ⚙️ ai_config.json       # AI provider settings
│   └── ⚙️ security_config.json # Security policies
├── 📁 templates/               # Web interface templates
│   ├── 🌐 index.html           # Main web page
│   ├── 🌐 chat.html            # Chat interface
│   └── 📁 static/              # CSS, JS, images
├── 📁 data/                    # Application data
├── 📁 logs/                    # Log files
├── 📁 exports/                 # Exported sessions
├── 🐍 main.py                  # Main application entry point
├── 🐍 setup_aion_fixed.py      # Automated setup script
├── 📄 requirements.txt         # Python dependencies
├── 📄 requirements-dev.txt     # Development dependencies
├── 📄 README.md               # This file
├── 📄 LICENSE                 # MIT License
└── 📄 CHANGELOG.md            # Version history
```

### Adding New AI Providers
```python
# core/ai_providers.py
class CustomAIProvider:
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    async def get_completion(self, prompt: str, **kwargs) -> str:
        # Implement your AI provider logic here
        pass

    def validate_config(self) -> bool:
        # Validate configuration
        return bool(self.api_key)
```

### Creating Custom Plugins
```python
# plugins/my_custom_plugin.py
from core.plugins import BasePlugin

class MyCustomPlugin(BasePlugin):
    name = "My Custom Plugin"
    version = "1.0.0"
    description = "A custom plugin for AION"

    def __init__(self):
        super().__init__()
        self.commands = {
            "hello": self.say_hello,
            "calculate": self.calculate
        }

    def say_hello(self, args: list) -> str:
        name = args[0] if args else "World"
        return f"Hello, {name}!"

    def calculate(self, args: list) -> str:
        try:
            expression = " ".join(args)
            result = eval(expression)  # Note: Use safely in production
            return f"Result: {result}"
        except Exception as e:
            return f"Error: {e}"

    def on_load(self):
        print(f"Plugin {self.name} loaded successfully!")

    def on_unload(self):
        print(f"Plugin {self.name} unloaded!")
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=core --cov=interfaces --cov=utils

# Run specific test file
python -m pytest tests/test_ai_providers.py

# Run with verbose output
python -m pytest -v
```

### Test Arabic Support
```bash
python test_arabic.py
```

### Quick System Test
```bash
python quick_test.py
```

## 🤝 Contributing

We welcome contributions from the community! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/AliPluss/AION.git
cd AION

# Create virtual environment
python -m venv dev_env
source dev_env/bin/activate  # Windows: dev_env\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
python -m pytest
```

### Code Style
- **Formatter**: Black
- **Linter**: Flake8
- **Type Checker**: MyPy
- **Import Sorting**: isort

```bash
# Format code
black .

# Check linting
flake8 .

# Type checking
mypy .
```

## 📊 Performance & Benchmarks

### System Requirements
- **Minimum**: 4GB RAM, 2GB storage, Python 3.10+
- **Recommended**: 8GB RAM, 5GB storage, Python 3.11+
- **Optimal**: 16GB RAM, 10GB storage, Python 3.12+

### Performance Metrics
- **Startup Time**: < 2 seconds
- **AI Response Time**: 1-5 seconds (depending on provider)
- **Code Execution**: < 1 second for simple scripts
- **Memory Usage**: 50-200MB (depending on features enabled)
- **Concurrent Users**: Up to 100 (web interface)

## 🔧 Troubleshooting

### Common Issues

1. **Arabic text not displaying correctly**:
   ```bash
   # Windows: Set console to UTF-8
   chcp 65001

   # Linux/Mac: Check locale
   export LANG=en_US.UTF-8
   ```

2. **AI provider API errors**:
   - Verify API keys in `config/config.json`
   - Check internet connection
   - Verify API quotas and limits

3. **Plugin loading errors**:
   - Check plugin syntax
   - Verify plugin dependencies
   - Review plugin logs in `logs/plugins.log`

4. **Web interface not accessible**:
   - Check if port is already in use
   - Verify firewall settings
   - Try different port: `python main.py web --port 8080`

### Debug Mode
```bash
# Enable debug logging
export AION_DEBUG=true
python main.py start

# Or use debug flag
python main.py start --debug
```

### Log Files
- **Application**: `logs/aion.log`
- **AI Providers**: `logs/ai_providers.log`
- **Security**: `logs/security.log`
- **Plugins**: `logs/plugins.log`
- **Web Interface**: `logs/web.log`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

### Core Technologies
- **[Rich](https://github.com/Textualize/rich)** - Beautiful terminal formatting
- **[Textual](https://github.com/Textualize/textual)** - Modern TUI framework
- **[FastAPI](https://fastapi.tiangolo.com/)** - High-performance web framework
- **[Typer](https://typer.tiangolo.com/)** - Modern CLI framework
- **[OpenAI](https://openai.com/)** - AI language models

### Community
- Thanks to all contributors and beta testers
- Special thanks to the Arabic-speaking developer community
- Inspired by modern terminal applications and AI assistants

## 📞 Support & Community

### Get Help
- 📧 **Email**: [support@aion-ai.com](mailto:support@aion-ai.com)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/AliPluss/AION/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/AliPluss/AION/discussions)
- 📖 **Documentation**: [Wiki](https://github.com/AliPluss/AION/wiki)

### Community Links
- 🌟 **Star us on GitHub**: [AION Repository](https://github.com/AliPluss/AION)
- 🐦 **Follow on Twitter**: [@AION_AI](https://twitter.com/AION_AI)
- 💼 **LinkedIn**: [AION Project](https://linkedin.com/company/aion-ai)
- 📺 **YouTube**: [AION Tutorials](https://youtube.com/@AION_AI)

### Contributing
- 🤝 **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- 🌍 **Translate**: Help us add more languages
- 🔌 **Plugins**: Create and share plugins
- 📝 **Documentation**: Improve our docs

---

<div align="center">
  <h3>🧠 AION - Where AI Meets Terminal Excellence</h3>
  <p><strong>Built with ❤️ for developers, by developers</strong></p>
  <p>
    <a href="https://github.com/AliPluss/AION/stargazers">⭐ Star</a> •
    <a href="https://github.com/AliPluss/AION/fork">🍴 Fork</a> •
    <a href="https://github.com/AliPluss/AION/issues">🐛 Report Bug</a> •
    <a href="https://github.com/AliPluss/AION/discussions">💬 Discuss</a>
  </p>
</div>
