# 🤖 AION - AI Operating Node

**Modern Interactive TUI - Complete AI Terminal Assistant**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0--final-green.svg)](https://github.com/AliPluss/AION)
[![TUI](https://img.shields.io/badge/interface-modern--TUI-brightgreen.svg)](https://github.com/AliPluss/AION)
[![Interactive](https://img.shields.io/badge/mode-fully--interactive-blue.svg)](https://github.com/AliPluss/AION)

---

## 🌟 Overview

AION (AI Operating Node) is a **modern, fully interactive Terminal User Interface (TUI)** that provides a complete AI-powered terminal assistant experience. Built with **Textual** and **Rich**, it delivers persistent sessions, arrow-key navigation, and real-time AI interactions.

### ✨ Key Features

- 🔁 **Persistent Interactive Sessions**: Never exits after actions - continuous operation
- ⌨️ **Full Arrow-Key Navigation**: Professional keyboard-controlled interface
- 🤖 **5 AI Providers**: OpenAI, DeepSeek, Google Gemini, Anthropic Claude, OpenRouter
- 🌐 **7 Languages**: Real-time switching without restart
- 💬 **Live AI Chat**: Interactive conversations within the TUI
- 🔍 **Smart Search**: Multi-platform developer resource search
- 📘 **Command Explanation**: AI-powered command analysis
- 🔐 **Secure API Management**: Encrypted .env storage with real-time validation
- 🎨 **Modern UI**: Rich formatting with consistent styling and themes
- 📊 **System Status**: Real-time monitoring and configuration display

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/AliPluss/AION.git
cd AION

# Install dependencies
pip install textual rich

# Launch AION (recommended)
python aion.py

# Or launch TUI directly
python aion_tui.py

# Or use main CLI entry point
python aion_cli.py
```

---

## 🎮 Interactive Interface

### Main Menu
```
🤖 AION - AI Operating Node
Interactive Terminal Assistant

🌐 Language: EN | 🤖 AI: OPENAI | 🎨 Theme: Dark

┌─ Menu Options ─────────────────────────────┐
│ 🌐 Language Settings (L)                   │
│ 🤖 AI Provider Setup (A)                   │
│ 🎨 Theme Selection (T)                      │
│ 💬 AI Chat (C)                             │
│ 🔍 Smart Search (S)                        │
│ 📘 Command Explain (E)                     │
│ 📊 System Status (I)                       │
│ ❓ Help Guide (H)                          │
│ 🚪 Exit AION (Q)                           │
└────────────────────────────────────────────┘

Use keyboard shortcuts or click buttons
```

### Keyboard Shortcuts
| Key | Action | Description |
|-----|--------|-------------|
| `L` | Language | Change interface language |
| `A` | AI Setup | Configure AI provider & API key |
| `T` | Theme | Select visual theme |
| `C` | Chat | Open AI chat interface |
| `S` | Search | Smart developer search |
| `E` | Explain | AI command explanation |
| `I` | Status | System status display |
| `H` | Help | Interactive help guide |
| `Q` | Quit | Exit AION |

---

## 🔧 Features

### ✅ **Persistent Interactive Experience**
- **Continuous Operation**: Session never exits after actions
- **Main Menu Return**: All features return to control center
- **Error Recovery**: Graceful handling with session continuation
- **Keyboard Navigation**: Professional arrow-key controlled interface

### ✅ **Real-Time Language Switching**
- **7 Languages**: English, Arabic (RTL), Norwegian, German, French, Chinese, Spanish
- **Instant Updates**: UI changes immediately without restart
- **Status Persistence**: Language choice saved automatically
- **Cultural Adaptation**: Proper text rendering and formatting

### ✅ **Professional AI Integration**
- **API Key Setup**: Secure prompting and .env storage
- **Provider Validation**: Real-time configuration verification
- **Live Chat Mode**: Interactive conversations within TUI
- **Smart Responses**: Context-aware AI assistance

### ✅ **Advanced Search & Explanation**
- **Multi-Source Search**: StackOverflow, GitHub, Python Docs
- **Command Analysis**: AI-powered command explanation
- **Formatted Results**: Professional table output with URLs
- **Resource Links**: Direct access to documentation

---

## 🌍 Language Support

Complete interface translation with real-time switching:

- 🇬🇧 **English** (Default)
- 🇮🇶 **العربية** (Arabic) - Full RTL support
- 🇳🇴 **Norsk** (Norwegian)
- 🇩🇪 **Deutsch** (German)
- 🇫🇷 **Français** (French)
- 🇨🇳 **中文** (Chinese)
- 🇪🇸 **Español** (Spanish)

**Language switching is instant** - no restart required!

---

## 🤖 AI Provider Setup

### Supported Providers
- **🧠 OpenAI**: GPT-4, GPT-3.5 (`AION_OPENAI_API_KEY`)
- **🛰️ DeepSeek**: Advanced reasoning models (`AION_DEEPSEEK_API_KEY`)
- **🌐 Google**: Gemini Pro (`AION_GOOGLE_API_KEY`)
- **🤖 Anthropic**: Claude (`AION_ANTHROPIC_API_KEY`)
- **🛤️ OpenRouter**: Multiple models (`AION_OPENROUTER_API_KEY`)

### Setup Process
1. Launch AION: `python aion_tui.py`
2. Press `A` for AI setup
3. Use ↑↓ arrows to select provider
4. Enter API key (securely stored in .env)
5. Confirmation: "✅ API Key saved and activated"

---

## 📊 System Status

AION provides comprehensive system monitoring:

```
📊 AION System Status

🌐 Language: EN
🤖 AI Provider: OPENAI
🎨 Theme: Dark
🔐 API Keys: 1 configured
💾 Session: Active and persistent
🔧 Config: Loaded successfully

📍 Working Directory: /path/to/aion
🐍 Python Version: 3.12.0
⚡ AION Version: v1.0.0-final
```

---

## 🛠️ Development

### Requirements
- **Python 3.10+**
- **Textual**: Modern TUI framework
- **Rich**: Terminal formatting and styling
- **JSON**: Configuration management
- **Pathlib**: File system operations

### Project Structure
```
AION/
├── aion_tui.py             # 🎯 Modern TUI application
├── aion_cli.py             # 🚀 Main CLI entry point
├── aion/                   # 📦 Core package modules
│   ├── ai_engine/         # 🤖 AI integration
│   ├── interfaces/        # 🎮 Interface components
│   ├── utils/            # 🔧 Utility functions
│   └── main.py           # 📍 Package entry
├── locales/              # 🌍 Language files
├── requirements.txt      # 📋 Dependencies
└── .env                 # 🔐 API keys (auto-generated)
```

---

## 🧪 Testing

AION TUI has been comprehensively validated:

### ✅ **Validated Features**
- **Language Selection**: All 7 languages with real-time switching ✅
- **AI Provider Setup**: API key storage and validation ✅
- **Chat Functionality**: Live AI conversations ✅
- **Search Integration**: Multi-platform developer search ✅
- **Command Explanation**: AI-powered analysis ✅
- **Session Persistence**: No unexpected exits ✅
- **Error Handling**: Graceful recovery and continuation ✅
- **Arrow Navigation**: Responsive keyboard control ✅
- **Status Monitoring**: Real-time system information ✅

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
# Clone and setup
git clone https://github.com/AliPluss/AION.git
cd AION

# Install dependencies
pip install textual rich

# Test the TUI
python aion_tui.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Textual**: Modern TUI framework by Textualize
- **Rich Library**: Beautiful terminal formatting
- **Python Community**: Excellent ecosystem support
- **AI Providers**: OpenAI, DeepSeek, Google, Anthropic, OpenRouter

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/AliPluss/AION/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AliPluss/AION/discussions)
- **Documentation**: [Project Wiki](https://github.com/AliPluss/AION/wiki)

---

## 🎯 Production Status

**AION v1.0.0-final** is production-ready with:
- ✅ Complete modern interactive TUI experience
- ✅ Persistent sessions with no exits after actions
- ✅ Full arrow-key navigation throughout
- ✅ Real-time language switching (7 languages)
- ✅ Secure API key management with validation
- ✅ Live AI chat and search functionality
- ✅ Professional error handling and recovery
- ✅ Cross-platform compatibility confirmed

**Ready for immediate deployment and professional use!**

---

**Made with ❤️ by the AION Team | Modern TUI Release v1.0.0-final**
