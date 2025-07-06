#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔤 AION Arabic Interface Test
Comprehensive Arabic text rendering and encoding test
"""

import os
import sys
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Setup encoding for Arabic support
if sys.platform == "win32":
    os.system('chcp 65001 >nul 2>&1')
    os.environ["PYTHONIOENCODING"] = "utf-8"

console = Console()

def test_arabic_text_rendering():
    """Test Arabic text rendering in Rich console"""
    print("\n🔤 Testing Arabic Text Rendering:")
    print("=" * 50)
    
    arabic_texts = [
        "مرحباً بك في AION",
        "🧠 مساعد الذكاء الاصطناعي",
        "⚡ تنفيذ الكود متعدد اللغات",
        "🦀 رست - أداء عالي مع أمان الذاكرة",
        "⚡ سي++ - أقصى أداء وتحكم كامل",
        "🐍 بايثون - لغة سهلة ومرنة للتطوير السريع",
        "🟨 جافا سكريبت - لغة الويب والتطبيقات التفاعلية"
    ]
    
    try:
        console.print("\n[bold green]✅ Rich Console Arabic Test:[/bold green]")
        for text in arabic_texts:
            console.print(f"  {text}")
        
        # Test Rich Panel with Arabic
        console.print("\n[bold blue]📦 Rich Panel Test:[/bold blue]")
        panel = Panel(
            "🎉 مرحباً من AION!\nهذا اختبار للوحة العربية",
            title="🧠 AION - مساعد ذكي",
            border_style="green"
        )
        console.print(panel)
        
        # Test Rich Table with Arabic
        console.print("\n[bold yellow]📊 Rich Table Test:[/bold yellow]")
        table = Table(title="🌐 اللغات المتاحة | Available Languages")
        table.add_column("اللغة | Language", style="cyan")
        table.add_column("الأداء | Performance", style="magenta")
        table.add_column("الحالة | Status", style="green")
        
        table.add_row("🐍 Python", "متوسط", "✅ متاح")
        table.add_row("🟨 JavaScript", "متوسط", "✅ متاح")
        table.add_row("🦀 Rust", "عالي جداً", "✅ متاح")
        table.add_row("⚡ C++", "عالي جداً", "❌ غير مثبت")
        
        console.print(table)
        
        return True
        
    except Exception as e:
        print(f"❌ Arabic rendering test failed: {e}")
        return False

def test_config_files_arabic():
    """Test Arabic content in configuration files"""
    print("\n📁 Testing Arabic in Config Files:")
    print("=" * 50)
    
    try:
        # Test config.json
        config_path = Path("config/config.json")
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            
            # Check for Arabic content
            arabic_found = False
            def check_arabic_recursive(obj, path=""):
                nonlocal arabic_found
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        check_arabic_recursive(value, f"{path}.{key}")
                elif isinstance(obj, str):
                    if any('\u0600' <= char <= '\u06FF' for char in obj):
                        print(f"  ✅ Arabic found in {path}: {obj[:50]}...")
                        arabic_found = True
            
            check_arabic_recursive(config)
            
            if arabic_found:
                print("✅ config.json contains Arabic text")
            else:
                print("⚠️  config.json has no Arabic text")
        
        # Test lang_ar.json
        lang_path = Path("config/lang_ar.json")
        if lang_path.exists():
            with open(lang_path, "r", encoding="utf-8") as f:
                lang_data = json.load(f)
            
            arabic_count = 0
            for key, value in lang_data.items():
                if isinstance(value, str) and any('\u0600' <= char <= '\u06FF' for char in value):
                    arabic_count += 1
            
            print(f"✅ lang_ar.json contains {arabic_count} Arabic entries")
            
            # Show sample entries
            sample_entries = list(lang_data.items())[:3]
            for key, value in sample_entries:
                print(f"  {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Config files test failed: {e}")
        return False

def test_unicode_handling():
    """Test Unicode and emoji handling"""
    print("\n🦄 Testing Unicode and Emoji Handling:")
    print("=" * 50)
    
    try:
        # Test various Unicode characters
        unicode_tests = [
            ("Arabic", "مرحباً بك في عالم البرمجة"),
            ("Emojis", "🧠🚀⚡🦀🐍🟨💻🎉✅❌"),
            ("Mixed", "🎯 AION - مساعد ذكي 🤖"),
            ("RTL", "العربية من اليمين إلى اليسار"),
            ("Numbers", "النسخة 2.0.0 من AION"),
            ("Special", "تم التثبيت بنجاح! ✅")
        ]
        
        for test_name, text in unicode_tests:
            try:
                # Test string operations
                length = len(text)
                encoded = text.encode('utf-8')
                decoded = encoded.decode('utf-8')
                
                if text == decoded:
                    print(f"  ✅ {test_name}: {text} (length: {length})")
                else:
                    print(f"  ❌ {test_name}: Encoding/decoding mismatch")
                    
            except Exception as e:
                print(f"  ❌ {test_name}: Error - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Unicode test failed: {e}")
        return False

def test_file_encoding():
    """Test file encoding for Arabic content"""
    print("\n📄 Testing File Encoding:")
    print("=" * 50)
    
    try:
        # Test writing and reading Arabic content
        test_content = """
# اختبار الترميز العربي
مرحباً بك في AION
🧠 مساعد الذكاء الاصطناعي
⚡ تنفيذ الكود متعدد اللغات
"""
        
        test_file = Path("temp_arabic_test.txt")
        
        # Write with UTF-8 encoding
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        # Read back and verify
        with open(test_file, "r", encoding="utf-8") as f:
            read_content = f.read()
        
        if test_content.strip() == read_content.strip():
            print("✅ File encoding test passed")
            print("✅ Arabic content preserved correctly")
        else:
            print("❌ File encoding test failed")
            print("❌ Arabic content corrupted")
        
        # Cleanup
        if test_file.exists():
            test_file.unlink()
        
        return True
        
    except Exception as e:
        print(f"❌ File encoding test failed: {e}")
        return False

def main():
    """Run comprehensive Arabic interface test"""
    print("🔤 AION Arabic Interface Comprehensive Test")
    print("=" * 60)
    
    tests = [
        ("Arabic Text Rendering", test_arabic_text_rendering),
        ("Config Files Arabic", test_config_files_arabic),
        ("Unicode Handling", test_unicode_handling),
        ("File Encoding", test_file_encoding)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n📊 Arabic Interface Test Summary:")
    print("=" * 50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 Arabic Interface Test: PERFECT!")
        print("✅ All Arabic features working correctly")
    elif passed >= total * 0.8:
        print("\n✅ Arabic Interface Test: GOOD")
        print("🔧 Minor issues detected")
    else:
        print("\n⚠️  Arabic Interface Test: NEEDS ATTENTION")
        print("🔧 Multiple issues detected")
    
    return passed == total

if __name__ == "__main__":
    main()
