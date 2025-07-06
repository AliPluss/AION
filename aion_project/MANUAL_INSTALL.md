# 🔧 دليل التثبيت اليدوي | Manual Installation Guide

## 📋 الحالة الحالية | Current Status

✅ **Python 3.12.10** - مثبت ويعمل | Installed and working
❌ **Node.js** - غير مثبت | Not installed
❌ **Rust** - غير مثبت | Not installed
❌ **C++** - غير مثبت | Not installed

## 🚀 التثبيت السريع | Quick Installation

**شغل فاحص التثبيت | Run Installation Checker:**
```bash
python install_checker.py
```

**أو استخدم سكريپت PowerShell | Or use PowerShell script:**
```powershell
powershell -ExecutionPolicy Bypass -File install_dependencies.ps1
```

---

## 🎯 التثبيت اليدوي | Manual Installation

### 1. 🟨 تثبيت Node.js | Install Node.js

#### الخطوات | Steps:
1. **اذهب إلى الموقع | Go to website:**
   ```
   https://nodejs.org/en/download
   ```

2. **حمل النسخة LTS | Download LTS version:**
   - اختر "Windows Installer (.msi)" للنظام 64-bit
   - Choose "Windows Installer (.msi)" for 64-bit system

3. **شغل الملف المحمل | Run downloaded file:**
   - انقر نقرة مزدوجة على الملف المحمل
   - Double-click the downloaded file
   - اتبع التعليمات | Follow the installation wizard

4. **التحقق من التثبيت | Verify installation:**
   ```bash
   node --version
   npm --version
   ```

---

### 2. 🦀 تثبيت Rust | Install Rust

#### الخطوات | Steps:
1. **اذهب إلى الموقع | Go to website:**
   ```
   https://rustup.rs/
   ```

2. **حمل rustup-init.exe | Download rustup-init.exe:**
   - انقر على "Download rustup-init.exe (64-bit)"
   - Click "Download rustup-init.exe (64-bit)"

3. **شغل الملف | Run the file:**
   - انقر نقرة مزدوجة على rustup-init.exe
   - Double-click rustup-init.exe
   - اختر "1) Proceed with installation (default)"
   - Choose "1) Proceed with installation (default)"

4. **التحقق من التثبيت | Verify installation:**
   ```bash
   rustc --version
   cargo --version
   ```

---

### 3. ⚡ تثبيت MinGW-w64 (C++) | Install MinGW-w64 (C++)

#### الطريقة الأولى - MSYS2 (موصى به) | Method 1 - MSYS2 (Recommended):

1. **اذهب إلى الموقع | Go to website:**
   ```
   https://www.msys2.org/
   ```

2. **حمل MSYS2 installer | Download MSYS2 installer:**
   - حمل "msys2-x86_64-xxxxxxxx.exe"
   - Download "msys2-x86_64-xxxxxxxx.exe"

3. **ثبت MSYS2 | Install MSYS2:**
   - شغل الملف المحمل واتبع التعليمات
   - Run downloaded file and follow instructions

4. **افتح MSYS2 terminal وشغل | Open MSYS2 terminal and run:**
   ```bash
   pacman -Syu
   pacman -S mingw-w64-x86_64-gcc
   pacman -S mingw-w64-x86_64-gdb
   ```

5. **أضف إلى PATH | Add to PATH:**
   - أضف `C:\msys64\mingw64\bin` إلى متغير PATH
   - Add `C:\msys64\mingw64\bin` to PATH environment variable

#### الطريقة الثانية - TDM-GCC | Method 2 - TDM-GCC:

1. **اذهب إلى الموقع | Go to website:**
   ```
   https://jmeubank.github.io/tdm-gcc/
   ```

2. **حمل TDM-GCC | Download TDM-GCC:**
   - حمل "tdm64-gcc-x.x.x-2.exe"
   - Download "tdm64-gcc-x.x.x-2.exe"

3. **ثبت TDM-GCC | Install TDM-GCC:**
   - شغل الملف واتبع التعليمات
   - Run file and follow instructions

4. **التحقق من التثبيت | Verify installation:**
   ```bash
   g++ --version
   gcc --version
   ```

---

## ✅ التحقق النهائي | Final Verification

بعد تثبيت جميع المتطلبات، افتح terminal جديد وشغل | After installing all requirements, open new terminal and run:

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
Python 3.12.10
v20.x.x (or higher)
rustc 1.70.x (or higher)  
g++ (TDM-GCC or MinGW-W64) x.x.x
```

---

## 🧪 اختبار AION | Test AION

بعد التثبيت الناجح | After successful installation:

```bash
cd aion_project
python main.py start
```

**اختر الخيار 2 (تنفيذ الكود) واختبر جميع اللغات | Choose option 2 (Code Execution) and test all languages**

---

## 🔧 حل المشاكل | Troubleshooting

### مشكلة: "command not found"
**الحل | Solution:**
1. أعد تشغيل terminal | Restart terminal
2. أعد تشغيل الكمبيوتر | Restart computer  
3. تحقق من PATH environment variable

### مشكلة: PATH Environment Variable
**الحل | Solution:**
1. افتح "Environment Variables" من Control Panel
2. أضف المسارات التالية إلى PATH:
   - `C:\Program Files\nodejs\`
   - `C:\Users\[username]\.cargo\bin`
   - `C:\msys64\mingw64\bin` (أو مسار MinGW)

### مشكلة: Rust not found after installation
**الحل | Solution:**
```bash
# أعد تشغيل terminal أو شغل
# Restart terminal or run:
source ~/.cargo/env
```

---

## 📞 الدعم | Support

إذا واجهت مشاكل | If you encounter issues:

1. تأكد من اتصال الإنترنت | Check internet connection
2. تأكد من تحميل النسخ الصحيحة (64-bit) | Ensure correct versions (64-bit)
3. أعد تشغيل الكمبيوتر بعد التثبيت | Restart computer after installation
4. تحقق من إعدادات antivirus | Check antivirus settings

---

## 🎉 بعد التثبيت | After Installation

عند اكتمال التثبيت، ستتمكن من | Once installation is complete, you'll be able to:

- ✅ تشغيل كود Python بسرعة عادية
- ✅ تشغيل كود JavaScript بسرعة عادية  
- ✅ تشغيل كود Rust بأداء عالي جداً 🚀
- ✅ تشغيل كود C++ بأداء عالي جداً ⚡

**استمتع بقوة AION الكاملة! | Enjoy AION's full power!** 🔥
