# 🌍 AION - Multilingual AI Operating Node

## Overview / نظرة عامة

AION is a powerful multilingual AI assistant that works from the terminal and supports multiple programming languages, AI providers, and interface languages.

AION هو مساعد ذكي متعدد اللغات قوي يعمل من الطرفية ويدعم لغات البرمجة المتعددة ومقدمي الذكاء الاصطناعي ولغات الواجهة.

## 🚀 Quick Start / البدء السريع

### English Interface (Default)
```bash
python start_aion_en.py
```

### Arabic Interface (Original)
```bash
python start_aion.py
```

## 🌐 Language Selection / اختيار اللغة

When you start AION with `start_aion_en.py`, you'll see a language selection menu:

عند بدء تشغيل AION باستخدام `start_aion_en.py`، ستظهر قائمة اختيار اللغة:

```
🌍 Language Selection / اختيار اللغة
========================================
1. English (Default)
2. العربية (Arabic)
3. Français (French)
4. Deutsch (German)
5. Español (Spanish)
6. 中文 (Chinese)
7. Norsk (Norwegian)

Select language / اختر اللغة (1-7, default=1):
```

## 🔧 Terminal Arabic Support / دعم العربية في Terminal

### ✅ Recommended Terminals / الـ Terminals المُوصى بها:
- **Windows Terminal** (Best choice / الخيار الأفضل)
- **PowerShell 7+**
- **VS Code Integrated Terminal**
- **Git Bash** (with proper configuration)

### ⚠️ Limited Support / دعم محدود:
- **Command Prompt (cmd.exe)** - Basic support only
- **PowerShell 5.1** - May have display issues

### 🛠️ Configuration Tips / نصائح التكوين:

#### For Windows Terminal:
1. Install Windows Terminal from Microsoft Store
2. Set UTF-8 encoding in settings
3. Use a font that supports Arabic (like Cascadia Code)

#### For PowerShell:
```powershell
# Set UTF-8 encoding
chcp 65001
$env:PYTHONIOENCODING="utf-8"
$env:PYTHONUTF8="1"
```

## 📋 Available Commands / الأوامر المتاحة

### Core Commands / الأوامر الأساسية:

| English | Arabic | Description |
|---------|--------|-------------|
| `help` | `مساعدة` | Show help information |
| `execute python print('Hello')` | `execute python print('مرحبا')` | Execute code |
| `translate ar Hello` | `translate en مرحبا` | Translate text |
| `plugins` | `إضافات` | Show available plugins |
| `security` | `أمان` | Show security status |
| `change-language` | `تغيير-اللغة` | Change interface language |
| `exit` | `خروج` | Exit AION |

### Example Usage / أمثلة الاستخدام:

#### English Interface:
```
AION> execute python print('Hello AION! 🚀')
✅ Code executed successfully:
Hello AION! 🚀

AION> plugins
📦 Available plugins and modules:
• Calculator Plugin v1.0.0 - Advanced calculator
• Weather Plugin (in development) - Weather information
```

#### Arabic Interface:
```
AION> execute python print('مرحباً بك في AION! 🚀')
✅ تم تنفيذ الكود بنجاح:
‮مرحباً بك في AION! 🚀‬

AION> plugins
📦 الإضافات والوحدات المتاحة في النظام:
• Calculator Plugin v1.0.0 - آلة حاسبة متقدمة
• Weather Plugin (قيد التطوير) - معلومات الطقس
```

## 🔧 Technical Features / الميزات التقنية

### ✅ Fixed Issues / المشاكل المحلولة:
- **Arabic Text Direction**: Arabic text now displays correctly (RTL) / اتجاه النص العربي: النص العربي يظهر الآن بشكل صحيح
- **UTF-8 Encoding**: Full Unicode support / ترميز UTF-8: دعم كامل لـ Unicode
- **Terminal Compatibility**: Better support across different terminals / توافق Terminal: دعم أفضل عبر terminals مختلفة
- **Language Selection**: Choose interface language at startup / اختيار اللغة: اختر لغة الواجهة عند البدء

### 🚀 Enhanced Features / الميزات المحسنة:
- **Multilingual Commands**: Commands work in multiple languages / أوامر متعددة اللغات
- **Dynamic Language Switching**: Change language during runtime / تبديل اللغة الديناميكي
- **Smart Text Detection**: Automatic Arabic text direction fixing / كشف النص الذكي
- **Cross-Platform Support**: Works on Windows, Linux, macOS / دعم متعدد المنصات

## 🐛 Troubleshooting / استكشاف الأخطاء

### Arabic Text Issues / مشاكل النص العربي:

**Problem**: Arabic text appears reversed or garbled
**Solution**: 
1. Use Windows Terminal or VS Code terminal
2. Ensure UTF-8 encoding is enabled
3. Use `start_aion_en.py` and select Arabic (option 2)

**المشكلة**: النص العربي يظهر معكوساً أو مشوهاً
**الحل**:
1. استخدم Windows Terminal أو VS Code terminal
2. تأكد من تفعيل ترميز UTF-8
3. استخدم `start_aion_en.py` واختر العربية (خيار 2)

### Installation Issues / مشاكل التثبيت:

```bash
# Install required packages
pip install -r requirements.txt

# If Rich library is missing
pip install rich typer

# For development
pip install -e .
```

## 📁 File Structure / هيكل الملفات

```
AION/
├── start_aion.py          # Arabic interface (original)
├── start_aion_en.py       # English interface with language selection
├── utils/
│   ├── arabic_support.py  # Arabic text support utilities
│   └── translator.py      # Translation utilities
├── core/
│   ├── executor.py        # Code execution with Arabic support
│   └── security.py        # Security management
└── interfaces/
    └── cli.py             # Command line interface
```

## 🤝 Contributing / المساهمة

We welcome contributions in all supported languages!
نرحب بالمساهمات بجميع اللغات المدعومة!

## 📄 License / الترخيص

This project is licensed under the MIT License.
هذا المشروع مرخص تحت رخصة MIT.

---

**Happy Coding! / برمجة سعيدة! 🚀**
