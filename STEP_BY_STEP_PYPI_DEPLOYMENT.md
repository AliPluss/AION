# 🚀 دليل النشر على PyPI خطوة بخطوة

## 📋 الخطوات المطلوبة

### 1. 🔐 إعداد API Tokens

#### للـ TestPyPI (للاختبار):
1. اذهب إلى: https://test.pypi.org/account/login/
2. سجل دخولك
3. اذهب إلى: https://test.pypi.org/manage/account/token/
4. اضغط "Add API token"
5. اختر "Entire account" للنطاق
6. انسخ الـ token (يبدأ بـ `pypi-`)

#### للـ PyPI الإنتاجي:
1. اذهب إلى: https://pypi.org/account/login/
2. سجل دخولك
3. اذهب إلى: https://pypi.org/manage/account/token/
4. اضغط "Add API token"
5. اختر "Entire account" للنطاق
6. انسخ الـ token (يبدأ بـ `pypi-`)

### 2. 🧪 النشر على TestPyPI (للاختبار)

```bash
# استخدم الـ token الخاص بـ TestPyPI
python -m twine upload --repository testpypi dist/* --username __token__ --password pypi-YOUR_TESTPYPI_TOKEN_HERE
```

### 3. ✅ اختبار التثبيت من TestPyPI

```bash
# إنشاء بيئة اختبار جديدة
python -m venv test_env
test_env\Scripts\activate

# تثبيت من TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ aion-ai

# اختبار التشغيل
aion --help
python -c "import aion; print('✅ AION imported successfully!')"
```

### 4. 🚀 النشر على PyPI الإنتاجي

```bash
# استخدم الـ token الخاص بـ PyPI الإنتاجي
python -m twine upload dist/* --username __token__ --password pypi-YOUR_PYPI_TOKEN_HERE
```

### 5. 🎉 اختبار التثبيت النهائي

```bash
# إنشاء بيئة جديدة
python -m venv final_test
final_test\Scripts\activate

# تثبيت من PyPI
pip install aion-ai

# اختبار التشغيل
aion
aion-cli --help
aion-ai --version
```

## 🔧 الأوامر الجاهزة للتنفيذ

### أمر النشر على TestPyPI:
```bash
python -m twine upload --repository testpypi dist/* --username __token__ --password [YOUR_TESTPYPI_TOKEN]
```

### أمر النشر على PyPI:
```bash
python -m twine upload dist/* --username __token__ --password [YOUR_PYPI_TOKEN]
```

## 📊 التحقق من النشر

### TestPyPI:
- الرابط: https://test.pypi.org/project/aion-ai/
- التثبيت: `pip install --index-url https://test.pypi.org/simple/ aion-ai`

### PyPI الإنتاجي:
- الرابط: https://pypi.org/project/aion-ai/
- التثبيت: `pip install aion-ai`

## 🚨 ملاحظات مهمة

1. **احتفظ بالـ tokens آمنة** - لا تشاركها مع أحد
2. **اختبر على TestPyPI أولاً** قبل النشر الإنتاجي
3. **تأكد من عمل جميع الأوامر** بعد التثبيت
4. **لا يمكن حذف إصدار** بعد النشر على PyPI

## 🎯 الخطوة التالية

**أرسل لي API token من TestPyPI وسأقوم بالنشر فوراً!**

Token format: `pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
