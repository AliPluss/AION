#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار دعم اللغة العربية في Python
Test Arabic language support in Python
"""

import sys
import os

# تأكد من دعم UTF-8
if sys.platform == "win32":
    # تعيين ترميز UTF-8 لـ Windows
    os.environ["PYTHONIOENCODING"] = "utf-8"
    
    # محاولة تعيين console encoding
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    except:
        pass

def main():
    """الدالة الرئيسية لاختبار النص العربي"""
    
    print("=" * 50)
    print("🤖 اختبار دعم اللغة العربية في AION")
    print("=" * 50)
    
    # اختبار النصوص العربية
    arabic_texts = [
        "مرحباً بك في نظام AION",
        "نظام التشغيل الذكي",
        "مساعد الذكاء الاصطناعي",
        "تم تنفيذ الكود بنجاح ✅",
        "النظام جاهز للاستخدام 🚀"
    ]
    
    print("\n📝 اختبار النصوص العربية:")
    for i, text in enumerate(arabic_texts, 1):
        try:
            print(f"{i}. {text}")
        except UnicodeEncodeError as e:
            print(f"{i}. [خطأ في الترميز: {e}]")
    
    # اختبار العمليات الحسابية
    print("\n🔢 اختبار العمليات الحسابية:")
    print(f"العدد الذهبي: {(1 + 5**0.5) / 2:.6f}")
    print(f"قيمة π: {3.14159265359:.6f}")
    
    # اختبار التاريخ والوقت
    from datetime import datetime
    now = datetime.now()
    print(f"\n⏰ الوقت الحالي: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n✅ انتهى الاختبار بنجاح!")
    print("=" * 50)

if __name__ == "__main__":
    main()
