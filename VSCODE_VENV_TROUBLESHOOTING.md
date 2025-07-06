# 🔧 VS Code Virtual Environment Troubleshooting

## المشكلة (Problem)
```
VenvError: CREATE_VENV.PIP_FAILED_INSTALL_REQUIREMENTS
Error while running venv creation script: CREATE_VENV.PIP_FAILED_INSTALL_REQUIREMENTS
```

## الأسباب المحتملة (Possible Causes)

### 1. 📦 مشاكل في requirements.txt
- حزم غير متوافقة
- إصدارات متضاربة
- حزم تتطلب مكتبات نظام إضافية

### 2. 🌐 مشاكل الشبكة
- انقطاع الاتصال أثناء التحميل
- مشاكل في PyPI
- Firewall أو Proxy issues

### 3. 🔒 مشاكل الصلاحيات
- عدم وجود صلاحيات كتابة
- مجلدات محمية
- Antivirus blocking

### 4. 🐍 مشاكل Python
- إصدار Python غير متوافق
- pip قديم أو تالف
- مسارات Python خاطئة

## الحلول (Solutions)

### 🚀 الحل السريع: تشغيل fix_vscode_venv.bat
```batch
# تشغيل الإصلاح التلقائي
fix_vscode_venv.bat
```

### 🔧 الحل اليدوي: خطوة بخطوة

#### الخطوة 1: تنظيف البيئات القديمة
```bash
# حذف البيئات الافتراضية القديمة
rmdir /s /q .venv
rmdir /s /q venv
rmdir /s /q aion_env
```

#### الخطوة 2: إنشاء بيئة جديدة
```bash
# إنشاء بيئة افتراضية جديدة
python -m venv .venv

# تفعيل البيئة
.venv\Scripts\activate.bat

# ترقية pip
python -m pip install --upgrade pip
```

#### الخطوة 3: تثبيت المتطلبات تدريجياً
```bash
# تثبيت الأساسيات أولاً
python -m pip install wheel setuptools

# تثبيت المتطلبات الأساسية
python -m pip install -r requirements-minimal.txt

# تثبيت باقي المتطلبات (اختياري)
python -m pip install -r requirements.txt
```

#### الخطوة 4: تكوين VS Code
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./.venv/Scripts/python.exe",
  "python.terminal.activateEnvironment": true,
  "python.testing.pytestEnabled": true
}
```

### 🛠️ حلول بديلة

#### الحل البديل 1: استخدام conda
```bash
# إنشاء بيئة conda
conda create -n aion python=3.12
conda activate aion
pip install -r requirements-minimal.txt
```

#### الحل البديل 2: تثبيت عالمي (غير مستحسن)
```bash
# تثبيت الحزم عالمياً (للاختبار فقط)
pip install --user typer rich fastapi uvicorn
```

#### الحل البديل 3: استخدام pipenv
```bash
# استخدام pipenv
pip install pipenv
pipenv install --dev
pipenv shell
```

## التحقق من الإصلاح (Verification)

### اختبار البيئة الافتراضية
```bash
# تفعيل البيئة
.venv\Scripts\activate.bat

# اختبار Python
python --version

# اختبار الحزم الأساسية
python -c "import typer; print('✅ Typer works')"
python -c "import rich; print('✅ Rich works')"
python -c "import fastapi; print('✅ FastAPI works')"
```

### اختبار VS Code
1. **إعادة تشغيل VS Code**
2. **اختيار المفسر:** `Ctrl+Shift+P` → `Python: Select Interpreter`
3. **اختيار .venv:** اختر المفسر من مجلد `.venv`
4. **اختبار Terminal:** افتح terminal جديد وتأكد من تفعيل البيئة

## نصائح الوقاية (Prevention Tips)

### 1. 📋 استخدام requirements محدودة
- ابدأ بـ `requirements-minimal.txt`
- أضف الحزم تدريجياً
- اختبر كل إضافة

### 2. 🔄 تحديث الأدوات بانتظام
```bash
python -m pip install --upgrade pip setuptools wheel
```

### 3. 🧹 تنظيف دوري
```bash
# تنظيف cache pip
pip cache purge

# حذف البيئات القديمة
rmdir /s /q .venv
```

### 4. 📝 توثيق البيئة
```bash
# حفظ البيئة الحالية
pip freeze > requirements-working.txt
```

## الأخطاء الشائعة (Common Errors)

### خطأ: "Microsoft Visual C++ 14.0 is required"
**الحل:** تثبيت Visual Studio Build Tools

### خطأ: "Failed building wheel"
**الحل:** 
```bash
pip install --upgrade setuptools wheel
pip install --no-cache-dir package_name
```

### خطأ: "Permission denied"
**الحل:** تشغيل Command Prompt كـ Administrator

### خطأ: "No module named 'pip'"
**الحل:**
```bash
python -m ensurepip --upgrade
```

## الملخص (Summary)

✅ **الحل الأسرع:** تشغيل `fix_vscode_venv.bat`
✅ **الحل المضمون:** تثبيت تدريجي بـ `requirements-minimal.txt`
✅ **الحل الدائم:** تكوين VS Code settings صحيح
✅ **الوقاية:** تنظيف دوري وتحديث الأدوات

🎯 **النتيجة:** VS Code سيعمل مع البيئة الافتراضية بدون مشاكل!
