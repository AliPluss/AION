#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار منفذ الكود مع النص العربي
Test code executor with Arabic text
"""

import asyncio
import sys
import os

# إضافة المسار الحالي لـ Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.executor import CodeExecutor

async def test_arabic_execution():
    """اختبار تنفيذ الكود العربي"""
    
    print("🧪 اختبار منفذ الكود مع النص العربي")
    print("=" * 50)
    
    executor = CodeExecutor()
    
    # اختبار 1: نص عربي بسيط
    print("\n📝 اختبار 1: طباعة نص عربي بسيط")
    code1 = "print('مرحباً بك في AION!')"
    result1 = await executor.execute_code(code1, "python")
    
    print(f"✅ نجح: {result1.success}")
    if result1.success:
        print(f"📤 المخرجات: {result1.output}")
    else:
        print(f"❌ خطأ: {result1.error}")
    
    # اختبار 2: نص عربي مع رموز تعبيرية
    print("\n📝 اختبار 2: نص عربي مع رموز تعبيرية")
    code2 = "print('🤖 نظام AION جاهز للعمل! ✅')"
    result2 = await executor.execute_code(code2, "python")
    
    print(f"✅ نجح: {result2.success}")
    if result2.success:
        print(f"📤 المخرجات: {result2.output}")
    else:
        print(f"❌ خطأ: {result2.error}")
    
    # اختبار 3: عمليات حسابية مع نص عربي
    print("\n📝 اختبار 3: عمليات حسابية مع نص عربي")
    code3 = """
import math
pi = math.pi
print(f'قيمة π = {pi:.4f}')
print(f'الجذر التربيعي لـ 16 = {math.sqrt(16)}')
print('تم إنجاز العمليات الحسابية بنجاح! 🎯')
"""
    result3 = await executor.execute_code(code3, "python")
    
    print(f"✅ نجح: {result3.success}")
    if result3.success:
        print(f"📤 المخرجات: {result3.output}")
    else:
        print(f"❌ خطأ: {result3.error}")
    
    # اختبار 4: قائمة باللغة العربية
    print("\n📝 اختبار 4: قائمة باللغة العربية")
    code4 = """
languages = ['العربية', 'الإنجليزية', 'الفرنسية', 'الألمانية']
print('اللغات المدعومة في AION:')
for i, lang in enumerate(languages, 1):
    print(f'{i}. {lang}')
print('🌍 دعم متعدد اللغات!')
"""
    result4 = await executor.execute_code(code4, "python")
    
    print(f"✅ نجح: {result4.success}")
    if result4.success:
        print(f"📤 المخرجات: {result4.output}")
    else:
        print(f"❌ خطأ: {result4.error}")
    
    print("\n" + "=" * 50)
    print("🏁 انتهى اختبار منفذ الكود")

if __name__ == "__main__":
    asyncio.run(test_arabic_execution())
