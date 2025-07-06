# 🚀 AION Installation Guide | دليل تثبيت AION

## 📋 متطلبات النظام | System Requirements

- **Windows 10/11** (recommended)
- **Python 3.10+** ✅ (already installed)
- **PowerShell** (for installation scripts)

## 🎯 المتطلبات المطلوب تثبيتها | Required Components

### 1. 🟨 **Node.js** (JavaScript Runtime)
- **الغرض | Purpose**: تشغيل كود JavaScript
- **الموقع | Website**: https://nodejs.org/
- **الحالة | Status**: ❌ غير مثبت | Not installed

### 2. 🦀 **Rust** (High-Performance Language)
- **الغرض | Purpose**: تشغيل كود Rust عالي الأداء
- **الموقع | Website**: https://rustup.rs/
- **الحالة | Status**: ❌ غير مثبت | Not installed

### 3. ⚡ **MinGW-w64** (C++ Compiler)
- **الغرض | Purpose**: تشغيل كود C++ عالي الأداء
- **الموقع | Website**: https://www.mingw-w64.org/
- **الحالة | Status**: ❌ غير مثبت | Not installed

---

## 🔧 طرق التثبيت | Installation Methods

### الطريقة الأولى: التثبيت التلقائي (موصى به) | Method 1: Automatic Installation (Recommended)

#### باستخدام PowerShell:

1. **افتح PowerShell كمدير | Open PowerShell as Administrator**
   ```powershell
   # Right-click on PowerShell and select "Run as Administrator"
   # انقر بالزر الأيمن على PowerShell واختر "تشغيل كمدير"
   ```

2. **تشغيل سكريبت التثبيت | Run Installation Script**
   ```powershell
   # Navigate to AION directory
   cd "path\to\aion_project"
   
   # Run installation script
   .\install_requirements.ps1
   ```

#### أو باستخدام Winget (Windows 11):
```powershell
.\install_with_winget.ps1
```

---

### الطريقة الثانية: التثبيت اليدوي | Method 2: Manual Installation

#### 1. 🟨 تثبيت Node.js | Install Node.js

**الخطوات | Steps:**
1. اذهب إلى | Go to: https://nodejs.org/
2. حمل النسخة LTS | Download LTS version
3. شغل الملف المحمل | Run the downloaded installer
4. اتبع التعليمات | Follow the installation wizard
5. أعد تشغيل الطرفية | Restart terminal

**التحقق من التثبيت | Verify Installation:**
```bash
node --version
npm --version
```

#### 2. 🦀 تثبيت Rust | Install Rust

**الخطوات | Steps:**
1. اذهب إلى | Go to: https://rustup.rs/
2. حمل `rustup-init.exe` | Download `rustup-init.exe`
3. شغل الملف | Run the file
4. اختر التثبيت الافتراضي | Choose default installation
5. أعد تشغيل الطرفية | Restart terminal

**التحقق من التثبيت | Verify Installation:**
```bash
rustc --version
cargo --version
```

#### 3. ⚡ تثبيت MinGW-w64 | Install MinGW-w64

**الطريقة الأولى - Chocolatey:**
```powershell
# Install Chocolatey first
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install MinGW
choco install mingw -y
```

**الطريقة الثانية - Manual:**
1. اذهب إلى | Go to: https://www.mingw-w64.org/downloads/
2. حمل MSYS2 | Download MSYS2
3. ثبت MSYS2 | Install MSYS2
4. افتح MSYS2 terminal
5. شغل | Run: `pacman -S mingw-w64-x86_64-gcc`

**التحقق من التثبيت | Verify Installation:**
```bash
g++ --version
gcc --version
```

---

## ✅ التحقق من التثبيت | Verification

بعد التثبيت، شغل الأوامر التالية للتحقق | After installation, run these commands to verify:

```bash
# Check Python
python --version

# Check Node.js
node --version

# Check Rust
rustc --version

# Check C++
g++ --version
```

**النتيجة المتوقعة | Expected Output:**
```
Python 3.10.x
v18.x.x (or higher)
rustc 1.70.x (or higher)
g++ (MinGW-W64 x86_64) 12.x.x
```

---

## 🧪 اختبار AION | Test AION

بعد التثبيت، اختبر AION | After installation, test AION:

```bash
cd aion_project
python main.py start
```

**اختر الخيار 2 (تنفيذ الكود) واختبر جميع اللغات | Choose option 2 (Code Execution) and test all languages**

---

## 🔧 حل المشاكل | Troubleshooting

### مشكلة: "command not found"
**الحل | Solution:**
1. أعد تشغيل الطرفية | Restart terminal
2. أعد تشغيل الكمبيوتر | Restart computer
3. تحقق من PATH variables

### مشكلة: PowerShell Execution Policy
**الحل | Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### مشكلة: Permission Denied
**الحل | Solution:**
- شغل PowerShell كمدير | Run PowerShell as Administrator
- تأكد من الصلاحيات | Check permissions

---

## 📞 الدعم | Support

إذا واجهت مشاكل في التثبيت | If you encounter installation issues:

1. تأكد من اتصال الإنترنت | Check internet connection
2. شغل الطرفية كمدير | Run terminal as administrator
3. تحقق من إعدادات الحماية | Check antivirus settings
4. أعد تشغيل الكمبيوتر بعد التثبيت | Restart computer after installation

---

## 🎉 بعد التثبيت | After Installation

عند اكتمال التثبيت، ستتمكن من | Once installation is complete, you'll be able to:

- ✅ تشغيل كود Python
- ✅ تشغيل كود JavaScript  
- ✅ تشغيل كود Rust (أداء عالي)
- ✅ تشغيل كود C++ (أداء عالي)

**استمتع بـ AION! | Enjoy AION!** 🚀
