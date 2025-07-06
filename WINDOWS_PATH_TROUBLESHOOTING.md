# 🔧 Windows PATH Troubleshooting Guide

## المشكلة (Problem)
```
WARNING: The script flake8.exe is installed in 'C:\Users\aba82\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts' which is not on PATH.
```

## الحلول (Solutions)

### 🚀 الحل الأسرع: استخدام python -m
```bash
# بدلاً من:
flake8 .
pytest
black .

# استخدم:
python -m flake8 .
python -m pytest
python -m black .
```

### 🔧 الحل الدائم: إضافة PATH

#### الطريقة الأولى: PowerShell Script
```powershell
# تشغيل fix_python_path.ps1
.\fix_python_path.ps1
```

#### الطريقة الثانية: يدوياً
1. **افتح System Properties:**
   - اضغط `Win + R`
   - اكتب `sysdm.cpl`
   - اضغط Enter

2. **Environment Variables:**
   - اضغط "Environment Variables"
   - في "User variables" اختر "PATH"
   - اضغط "Edit"

3. **أضف المسار:**
   ```
   C:\Users\aba82\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\LocalCache\local-packages\Python312\Scripts
   ```

4. **أعد تشغيل Terminal/IDE**

### 🛠️ الحل البديل: Batch File
```batch
# تشغيل install_dev_tools.bat
install_dev_tools.bat
```

## التحقق من الإصلاح (Verification)

### اختبار الأدوات
```bash
# اختبار flake8
python -m flake8 --version

# اختبار pytest
python -m pytest --version

# اختبار black
python -m black --version

# تشغيل الاختبارات
python -m pytest tests/ -v
```

### اختبار PATH
```bash
# إذا تم إصلاح PATH، هذه الأوامر ستعمل:
flake8 --version
pytest --version
black --version
```

## الأوامر المحدثة (Updated Commands)

### للتطوير المحلي
```bash
# تشغيل الاختبارات
python -m pytest tests/ -v

# فحص الكود
python -m flake8 . --exclude=venv,build,dist

# تنسيق الكود
python -m black . --exclude="/(venv|build|dist)/"

# فحص الأنواع
python -m mypy . --ignore-missing-imports
```

### للـ CI/CD
تم تحديث `.github/workflows/ci.yml` لاستخدام `python -m` في جميع الأوامر.

## نصائح إضافية (Additional Tips)

### 1. استخدام Virtual Environment
```bash
# إنشاء بيئة افتراضية
python -m venv aion_env

# تفعيلها
aion_env\Scripts\activate

# تثبيت الأدوات
pip install -r requirements-dev.txt
```

### 2. تحديث pip
```bash
python -m pip install --upgrade pip
```

### 3. تثبيت بدون تحذيرات
```bash
pip install flake8 --no-warn-script-location
```

## استكشاف الأخطاء (Troubleshooting)

### المشكلة: "command not found"
**الحل:** استخدم `python -m [command]`

### المشكلة: "Permission denied"
**الحل:** تشغيل PowerShell كـ Administrator

### المشكلة: "Path too long"
**الحل:** استخدم مسارات مختصرة أو symbolic links

## الملخص (Summary)

✅ **الحل الأسرع:** استخدم `python -m` مع جميع الأدوات
✅ **الحل الدائم:** أضف Scripts directory إلى PATH
✅ **تم تحديث CI/CD:** لاستخدام `python -m` تلقائياً
✅ **أدوات مساعدة:** Scripts للتثبيت والإصلاح

🎯 **النتيجة:** لن تظهر تحذيرات PATH بعد الآن!
