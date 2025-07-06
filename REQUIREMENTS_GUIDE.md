# 📦 AION Requirements Guide

## 🎯 ملفات المتطلبات المختلفة:

### 1. **requirements.txt** (الأساسي)
```bash
pip install -r requirements.txt
```
- **الاستخدام:** التطوير المحلي والإنتاج
- **المحتوى:** جميع المكتبات مع أحدث الإصدارات
- **Python:** 3.9+ (بسبب google-generativeai)

### 2. **requirements-stable.txt** (المستقر)
```bash
pip install -r requirements-stable.txt
```
- **الاستخدام:** البيئات المستقرة
- **المحتوى:** إصدارات مثبتة ومجربة
- **Python:** 3.8+ (متوافق مع إصدارات أقدم)

### 3. **requirements-ci.txt** (CI/CD)
```bash
pip install -r requirements-ci.txt
```
- **الاستخدام:** GitHub Actions والاختبارات الآلية
- **المحتوى:** الحد الأدنى من المكتبات للاختبار
- **Python:** 3.8+ (أقصى توافق)

### 4. **requirements-dev.txt** (التطوير)
```bash
pip install -r requirements-dev.txt
```
- **الاستخدام:** أدوات التطوير الإضافية
- **المحتوى:** أدوات الاختبار والتحليل
- **Python:** 3.8+

## 🚀 التثبيت السريع:

### للاستخدام العادي:
```bash
pip install -r requirements-stable.txt
```

### للتطوير:
```bash
pip install -r requirements-stable.txt
pip install -r requirements-dev.txt
```

### للاختبار فقط:
```bash
pip install -r requirements-ci.txt
```

## 🔧 حل مشاكل التثبيت:

### مشكلة google-generativeai:
```bash
# إذا فشل التثبيت، استخدم:
pip install -r requirements-stable.txt
# أو
pip install -r requirements-ci.txt
```

### مشكلة Python 3.8:
```bash
# استخدم الملف المتوافق:
pip install -r requirements-ci.txt
```

### مشكلة CI/CD:
```bash
# GitHub Actions سيستخدم تلقائياً:
requirements-ci.txt (الأولوية الأولى)
requirements-stable.txt (الأولوية الثانية)
requirements.txt (الأولوية الثالثة)
```

## 📊 مقارنة الملفات:

| الملف | المكتبات | Python | الاستخدام | الاستقرار |
|-------|----------|--------|-----------|-----------|
| **requirements.txt** | كاملة | 3.9+ | إنتاج | ⭐⭐⭐ |
| **requirements-stable.txt** | كاملة | 3.8+ | مستقر | ⭐⭐⭐⭐⭐ |
| **requirements-ci.txt** | أساسية | 3.8+ | اختبار | ⭐⭐⭐⭐⭐ |
| **requirements-dev.txt** | تطوير | 3.8+ | تطوير | ⭐⭐⭐⭐ |

## 🎯 التوصيات:

### 👨‍💻 للمطورين الجدد:
```bash
pip install -r requirements-stable.txt
```

### 🚀 للتطوير النشط:
```bash
pip install -r requirements-stable.txt
pip install -r requirements-dev.txt
```

### 🧪 للاختبار:
```bash
pip install -r requirements-ci.txt
```

### 🏭 للإنتاج:
```bash
pip install -r requirements-stable.txt
```

## 🔍 فحص التثبيت:

### التحقق من المكتبات:
```bash
pip list | grep -E "(rich|typer|textual|fastapi)"
```

### اختبار AION:
```bash
python start_aion_en.py
```

### تشغيل الاختبارات:
```bash
python -m pytest tests/test_simple.py -v
```

## 🛠️ استكشاف الأخطاء:

### خطأ في google-generativeai:
```bash
# الحل: استخدم requirements-ci.txt
pip uninstall google-generativeai
pip install -r requirements-ci.txt
```

### خطأ في Python 3.8:
```bash
# الحل: استخدم requirements-stable.txt
pip install -r requirements-stable.txt
```

### خطأ في CI/CD:
```bash
# الحل: تم إصلاحه تلقائياً في .github/workflows/ci.yml
```

## 📝 ملاحظات مهمة:

1. **google-generativeai** يتطلب Python 3.9+
2. **requirements-ci.txt** لا يحتوي على google-generativeai
3. **CI/CD** يستخدم تلقائياً الملف الأنسب
4. **جميع الملفات** تدعم الوظائف الأساسية لـ AION

## 🎉 الخلاصة:

**استخدم requirements-stable.txt للاستخدام العادي!**

```bash
pip install -r requirements-stable.txt
python start_aion_en.py
```

**🚀 AION سيعمل بدون مشاكل!**
