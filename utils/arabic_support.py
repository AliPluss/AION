#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
دعم اللغة العربية في AION
Arabic language support utilities for AION
"""

import sys
import os
import re

def setup_arabic_console():
    """إعداد وحدة التحكم لدعم النص العربي"""
    if sys.platform == "win32":
        try:
            # تعيين ترميز UTF-8 للوحة التحكم
            os.system('chcp 65001 >nul 2>&1')
            
            # تعيين متغيرات البيئة
            os.environ["PYTHONIOENCODING"] = "utf-8"
            os.environ["PYTHONUTF8"] = "1"
            
            # إعادة تكوين stdout و stderr
            import codecs
            if hasattr(sys.stdout, 'detach'):
                sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
            if hasattr(sys.stderr, 'detach'):
                sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
                
        except Exception:
            pass

def is_arabic_text(text: str) -> bool:
    """فحص ما إذا كان النص يحتوي على أحرف عربية"""
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
    return bool(arabic_pattern.search(text))

def fix_arabic_display(text: str) -> str:
    """إصلاح عرض النص العربي في وحدة التحكم"""
    if not text or not is_arabic_text(text):
        return text
    
    try:
        # محاولة إصلاح اتجاه النص العربي
        if sys.platform == "win32":
            # إضافة علامة اتجاه النص من اليمين إلى اليسار
            return f"\u202E{text}\u202C"
        else:
            return text
    except Exception:
        return text

def print_arabic(text: str, **kwargs):
    """طباعة النص العربي مع الإعدادات الصحيحة"""
    try:
        # إعداد وحدة التحكم إذا لم يتم إعدادها
        setup_arabic_console()
        
        # إصلاح عرض النص العربي
        fixed_text = fix_arabic_display(text)
        
        # طباعة النص
        print(fixed_text, **kwargs)
        
    except Exception as e:
        # في حالة فشل الطباعة العربية، اطبع النص الأصلي
        try:
            print(text, **kwargs)
        except:
            print(f"[خطأ في عرض النص: {e}]", **kwargs)

def format_arabic_message(message: str, status: str = "info") -> str:
    """تنسيق الرسائل العربية مع الرموز المناسبة"""
    
    status_icons = {
        "success": "✅",
        "error": "❌", 
        "warning": "⚠️",
        "info": "ℹ️",
        "loading": "⏳",
        "done": "🎉"
    }
    
    icon = status_icons.get(status, "•")
    formatted = f"{icon} {message}"
    
    return fix_arabic_display(formatted)

def create_arabic_banner(title: str, width: int = 50) -> str:
    """إنشاء لافتة عربية منسقة"""
    
    # إصلاح عرض العنوان
    fixed_title = fix_arabic_display(title)
    
    # حساب الطول الفعلي للنص (مع مراعاة الأحرف العربية)
    title_length = len(title.encode('utf-8')) // 2 if is_arabic_text(title) else len(title)
    
    # إنشاء الحدود
    border = "=" * width
    padding = (width - title_length) // 2
    
    banner = f"""
{border}
{' ' * padding}{fixed_title}
{border}
"""
    
    return banner

def check_terminal_arabic_support() -> bool:
    """فحص ما إذا كان Terminal يدعم اللغة العربية بشكل صحيح"""
    try:
        # اختبار طباعة نص عربي بسيط
        test_text = "مرحبا"

        # محاولة ترميز النص
        test_text.encode('utf-8')

        # فحص متغيرات البيئة
        import os
        encoding = os.environ.get('PYTHONIOENCODING', '').lower()

        # فحص نوع Terminal
        term = os.environ.get('TERM', '').lower()
        term_program = os.environ.get('TERM_PROGRAM', '').lower()

        # Terminal types that generally support Arabic well
        good_terminals = [
            'windows terminal',
            'vscode',
            'code',
            'powershell',
            'pwsh'
        ]

        # Check if we're in a good terminal
        terminal_ok = any(good_term in term_program for good_term in good_terminals)

        # Check encoding
        encoding_ok = 'utf' in encoding or encoding == ''

        return terminal_ok and encoding_ok

    except Exception:
        return False

def get_language_preference() -> str:
    """الحصول على تفضيل اللغة من المستخدم مع واجهة تفاعلية محسنة"""
    try:
        from rich.console import Console
        from rich.prompt import Prompt
        from rich.panel import Panel
        from rich.table import Table
        from rich.align import Align

        console = Console()

        # إنشاء جدول اللغات مع تصميم جميل
        language_table = Table(show_header=True, header_style="bold magenta", box=None)
        language_table.add_column("Option", style="bold cyan", width=8, justify="center")
        language_table.add_column("Flag", style="white", width=6, justify="center")
        language_table.add_column("Language", style="bold green", width=20)
        language_table.add_column("Native Name", style="bold yellow", width=15)

        languages = [
            ("1", "🇺🇸", "English", "English"),
            ("2", "🇸🇦", "Arabic", "العربية"),
            ("3", "🇫🇷", "French", "Français"),
            ("4", "🇩🇪", "German", "Deutsch"),
            ("5", "🇪🇸", "Spanish", "Español"),
            ("6", "🇨🇳", "Chinese", "中文"),
            ("7", "🇳🇴", "Norwegian", "Norsk")
        ]

        for option, flag, lang_en, lang_native in languages:
            language_table.add_row(option, flag, lang_en, lang_native)

        # إنشاء لوحة جميلة
        title = "🌍 Language Selection / اختيار اللغة"
        subtitle = "Choose your preferred interface language\nاختر لغة الواجهة المفضلة لديك"

        panel_content = Align.center(language_table)
        language_panel = Panel(
            panel_content,
            title=f"[bold blue]{title}[/bold blue]",
            subtitle=f"[dim]{subtitle}[/dim]",
            border_style="bright_blue",
            padding=(1, 2),
            expand=False
        )

        console.print("\n")
        console.print(language_panel)

        # طلب الاختيار مع تحسينات
        choice = Prompt.ask(
            "\n[bold cyan]➤ Select language number / اختر رقم اللغة[/bold cyan]",
            choices=["1", "2", "3", "4", "5", "6", "7"],
            default="1",
            show_choices=False,
            show_default=True
        )

        lang_map = {
            '1': 'en', '2': 'ar', '3': 'fr', '4': 'de',
            '5': 'es', '6': 'zh', '7': 'no'
        }

        selected_lang = lang_map.get(choice, 'en')

        # عرض تأكيد الاختيار
        selected_info = next((lang_info for opt, flag, lang_en, lang_native in languages if opt == choice for lang_info in [(opt, flag, lang_en, lang_native)]), None)
        if selected_info:
            console.print(f"\n✅ [green]Language selected / تم اختيار اللغة:[/green] [bold]{selected_info[1]} {selected_info[2]} ({selected_info[3]})[/bold]")

        return selected_lang

    except ImportError:
        # Fallback إلى واجهة بسيطة
        print("\n🌍 Language Selection / اختيار اللغة")
        print("=" * 50)
        print("1. 🇺🇸 English (Default)")
        print("2. 🇸🇦 العربية (Arabic)")
        print("3. 🇫🇷 Français (French)")
        print("4. 🇩🇪 Deutsch (German)")
        print("5. 🇪🇸 Español (Spanish)")
        print("6. 🇨🇳 中文 (Chinese)")
        print("7. 🇳🇴 Norsk (Norwegian)")
        print("=" * 50)

        choice = input("➤ Select language number / اختر رقم اللغة (1-7, default=1): ").strip()

        lang_map = {
            '1': 'en', '2': 'ar', '3': 'fr', '4': 'de',
            '5': 'es', '6': 'zh', '7': 'no', '': 'en'
        }

        selected_lang = lang_map.get(choice, 'en')
        print(f"✅ Language selected: {selected_lang}")
        return selected_lang

    except Exception as e:
        print(f"Error in language selection: {e}")
        return 'en'  # افتراضي في حالة الخطأ

def test_arabic_support():
    """اختبار دعم اللغة العربية"""

    print(create_arabic_banner("🤖 اختبار دعم اللغة العربية"))

    test_messages = [
        ("مرحباً بك في نظام AION", "success"),
        ("تم تحميل النظام بنجاح", "done"),
        ("جاري معالجة البيانات...", "loading"),
        ("تحذير: تحقق من الإعدادات", "warning"),
        ("خطأ في الاتصال", "error"),
        ("معلومات النظام", "info")
    ]

    for message, status in test_messages:
        formatted = format_arabic_message(message, status)
        print_arabic(formatted)

    print_arabic(create_arabic_banner("🎯 انتهى الاختبار"))

if __name__ == "__main__":
    test_arabic_support()
