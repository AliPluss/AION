# 🚀 AION Quick Start Guide

## 📦 Installation

### Option 1: Install from PyPI (Recommended)
```bash
pip install aion-ai
```

### Option 2: Install from GitHub
```bash
git clone https://github.com/AliPluss/AION.git
cd AION
pip install -e .
```

## 🎯 First Run

After installation, start AION with any of these commands:

```bash
aion          # Main command
aion-cli      # CLI alias  
aion-ai       # Full name alias
```

## 🌍 Language Selection

AION supports 7 languages with beautiful animated interface:

- 🇬🇧 **English** - Default interface language
- 🇮🇶 **Arabic (العربية)** - Full RTL support
- 🇫🇷 **French (Français)** - Complete localization
- 🇩🇪 **German (Deutsch)** - Native interface
- 🇪🇸 **Spanish (Español)** - Full translation
- 🇨🇳 **Chinese (中文)** - Simplified Chinese
- 🇳🇴 **Norwegian (Norsk)** - Complete support

**Navigation**: Use ↑↓ arrow keys to select, Enter to confirm

## 🤖 AI Provider Setup

### 1. Choose Your AI Provider

AION supports multiple AI providers:

- **🧠 OpenAI** - GPT-3.5, GPT-4, GPT-4 Turbo
- **🛰️ DeepSeek** - DeepSeek Chat, DeepSeek Coder  
- **🌐 Google Gemini** - Gemini Pro, Gemini Pro Vision
- **🛤️ OpenRouter** - Access to multiple models

### 2. Configure API Keys

Create a `.env` file in your project directory:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# DeepSeek Configuration  
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Google Gemini Configuration
GOOGLE_API_KEY=your_google_api_key_here

# OpenRouter Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 3. Get API Keys

- **OpenAI**: [platform.openai.com](https://platform.openai.com/api-keys)
- **DeepSeek**: [platform.deepseek.com](https://platform.deepseek.com/api_keys)
- **Google**: [makersuite.google.com](https://makersuite.google.com/app/apikey)
- **OpenRouter**: [openrouter.ai](https://openrouter.ai/keys)

## ⌨️ Navigation Controls

AION uses **pure arrow-key navigation** - no typing required!

- **↑↓** - Navigate menu items
- **Enter** - Select/Confirm
- **Esc** - Cancel/Back
- **Tab** - Switch between sections

## 🔒 Security Features

- **🔐 Dynamic Encryption**: HMAC+AES with minute-based rotation
- **🛡️ Sandbox Execution**: Isolated code execution environment
- **📊 Real-time Monitoring**: Continuous security assessment
- **🔑 Secure API Management**: Encrypted credential storage

## 🧩 Plugin System

AION includes a powerful plugin system:

```bash
# List available plugins
aion plugins list

# Load a plugin
aion plugins load example_plugin

# Create custom plugin
aion plugins create my_plugin
```

## 📱 Interface Modes

### 1. TUI Mode (Default)
Beautiful terminal user interface with animations:
```bash
aion
```

### 2. CLI Mode
Command-line interface for scripting:
```bash
aion-cli --prompt "Your question here"
```

### 3. Web Mode
Browser-based interface:
```bash
aion web --port 8000
```

## 🎨 Customization

### Change Language
```bash
aion config language arabic    # Switch to Arabic
aion config language english   # Switch to English
```

### Set Default AI Provider
```bash
aion config provider openai    # Set OpenAI as default
aion config provider deepseek  # Set DeepSeek as default
```

### Configure Security Level
```bash
aion config security high      # Maximum security
aion config security medium    # Balanced security
aion config security low       # Minimal security
```

## 🧪 Testing Installation

Run the test script to verify everything works:

```bash
python test_pypi_package.py
```

## 📚 Common Commands

```bash
# Get help
aion --help

# Check version
aion --version

# Start with specific language
aion --language arabic

# Start with specific provider
aion --provider openai

# Enable debug mode
aion --debug

# Run in quiet mode
aion --quiet
```

## 🆘 Troubleshooting

### Installation Issues
```bash
# Upgrade pip first
pip install --upgrade pip

# Install with verbose output
pip install -v aion-ai

# Install from source if PyPI fails
pip install git+https://github.com/AliPluss/AION.git
```

### API Key Issues
```bash
# Verify .env file location
ls -la .env

# Test API key
aion test-api openai
```

### Import Errors
```bash
# Check installation
pip show aion-ai

# Reinstall if needed
pip uninstall aion-ai
pip install aion-ai
```

## 🔗 Useful Links

- **📖 Documentation**: [GitHub README](https://github.com/AliPluss/AION#readme)
- **🐛 Report Issues**: [GitHub Issues](https://github.com/AliPluss/AION/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/AliPluss/AION/discussions)
- **📦 PyPI Package**: [pypi.org/project/aion-ai](https://pypi.org/project/aion-ai/)

## 🎉 You're Ready!

AION is now installed and ready to use. Start with:

```bash
aion
```

Enjoy your AI-powered terminal experience! 🚀
