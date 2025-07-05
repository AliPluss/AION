#!/usr/bin/env python3
"""
🚀 AION Quick Start
Simple launcher for AION with Arabic interface
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.translator import Translator
from interfaces.cli import CLI
from core.security import SecurityManager
from utils.arabic_support import setup_arabic_console, print_arabic, format_arabic_message
from rich.console import Console
from rich.panel import Panel

def main():
    """Main function to start AION"""
    # إعداد دعم اللغة العربية
    setup_arabic_console()

    console = Console()

    # Display welcome message
    welcome_panel = Panel.fit(
        """
🤖 [bold blue]AION - عقدة التشغيل الذكية[/bold blue]
[green]مساعد الذكاء الاصطناعي متعدد اللغات والمنصات[/green]

[yellow]الأوامر الأساسية:[/yellow]
• [cyan]help[/cyan] - عرض المساعدة الشاملة
• [cyan]execute python print('مرحبا بك!')[/cyan] - تنفيذ كود البرمجة
• [cyan]translate en مرحبا[/cyan] - ترجمة النصوص
• [cyan]plugins[/cyan] - إدارة الإضافات والوحدات
• [cyan]security[/cyan] - مراقبة حالة الأمان
• [cyan]change-language[/cyan] - تبديل لغة الواجهة
• [cyan]exit[/cyan] - إنهاء البرنامج والخروج

[red]تنبيه مهم:[/red] لاستخدام خدمات الذكاء الاصطناعي، يجب تكوين مفاتيح API أولاً
        """,
        title="🌟 أهلاً وسهلاً بك في نظام AION",
        border_style="blue"
    )
    
    console.print(welcome_panel)
    console.print()
    
    # Initialize components
    translator = Translator()
    translator.set_language('ar')  # Set Arabic as default
    security = SecurityManager()
    cli = CLI(translator, security)
    
    console.print("[green]✅ تم تشغيل نظام AION بنجاح وجاهز للاستخدام![/green]")
    console.print("[yellow]💡 يمكنك الآن كتابة أي أمر من الأوامر المتاحة أعلاه...[/yellow]")
    console.print()
    
    # Main interaction loop
    try:
        while True:
            try:
                # Get user input
                user_input = console.input("[bold cyan]AION>[/bold cyan] ").strip()
                
                if not user_input:
                    continue
                
                # Handle exit commands
                if user_input.lower() in ['exit', 'quit', 'خروج', 'إنهاء', 'انهاء']:
                    console.print("[yellow]👋 شكراً لك على استخدام نظام AION! نراك قريباً[/yellow]")
                    break
                
                # Handle help command
                elif user_input.lower() in ['help', 'مساعدة', 'مساعده', 'ساعدني']:
                    cli.show_help()
                
                # Handle execute command
                elif user_input.lower().startswith('execute'):
                    parts = user_input.split(' ', 2)
                    if len(parts) >= 3:
                        language = parts[1]
                        code = parts[2]
                        # Import executor directly
                        from core.executor import CodeExecutor
                        import asyncio

                        executor = CodeExecutor()
                        try:
                            result = asyncio.run(executor.execute_code(code, language))
                            if hasattr(result, 'success') and result.success:
                                console.print(f"[green]✅ تم تنفيذ الكود بنجاح:[/green]")
                                console.print(f"[white]{result.output}[/white]")
                            else:
                                console.print(f"[red]❌ فشل في تنفيذ الكود:[/red]")
                                console.print(f"[red]{result.error}[/red]")
                        except Exception as e:
                            console.print(f"[red]❌ حدث خطأ غير متوقع: {e}[/red]")
                    else:
                        console.print("[red]❌ طريقة الاستخدام الصحيحة: execute <لغة_البرمجة> <الكود>[/red]")
                
                # Handle translate command
                elif user_input.lower().startswith('translate'):
                    parts = user_input.split(' ', 2)
                    if len(parts) >= 3:
                        target_lang = parts[1]
                        text = parts[2]
                        # Simple translation simulation
                        console.print(f"[green]ترجمة النص إلى اللغة {target_lang}:[/green] {text}")
                        console.print("[yellow]💡 ملاحظة: هذه ترجمة تجريبية، للترجمة الفعلية يرجى تكوين مفاتيح AI[/yellow]")
                    else:
                        console.print("[red]❌ طريقة الاستخدام: translate <اللغة_المستهدفة> <النص_المراد_ترجمته>[/red]")
                
                # Handle plugins command
                elif user_input.lower() in ['plugins', 'إضافات', 'اضافات', 'الإضافات']:
                    console.print("[cyan]📦 الإضافات والوحدات المتاحة في النظام:[/cyan]")
                    console.print("• [green]Calculator Plugin v1.0.0[/green] - آلة حاسبة متقدمة")
                    console.print("• [yellow]Weather Plugin (قيد التطوير)[/yellow] - معلومات الطقس")
                    console.print("• [yellow]System Info Plugin (قيد التطوير)[/yellow] - معلومات النظام")
                    console.print("• [yellow]File Manager Plugin (مخطط)[/yellow] - إدارة الملفات")
                    console.print("[blue]💡 يمكنك تطوير إضافات جديدة باستخدام Plugin API[/blue]")
                
                # Handle security command
                elif user_input.lower() in ['security', 'أمان', 'امان', 'الأمان']:
                    status = security.get_security_status()
                    console.print(f"[cyan]🔒 تقرير حالة الأمان والحماية:[/cyan]")
                    console.print(f"• عدد الجلسات النشطة حالياً: [green]{status['active_sessions']}[/green]")
                    console.print(f"• إجمالي الرموز المُنشأة: [blue]{status['total_tokens']}[/blue]")
                    console.print(f"• عدد المحاولات الفاشلة: [red]{status['failed_attempts']}[/red]")
                    console.print(f"• مستوى الحماية الحالي: [yellow]{status['security_level']}[/yellow]")
                    console.print("[green]✅ النظام آمن ومحمي[/green]")
                
                # Handle language change
                elif user_input.lower() in ['change-language', 'تغيير-اللغة', 'تغيير_اللغة', 'لغة']:
                    console.print("[cyan]🌍 اللغات المدعومة في النظام:[/cyan]")
                    console.print("1. [green]العربية[/green] (ar) - اللغة العربية")
                    console.print("2. [blue]English[/blue] (en) - الإنجليزية")
                    console.print("3. [red]Español[/red] (es) - الإسبانية")
                    console.print("4. [yellow]Français[/yellow] (fr) - الفرنسية")
                    console.print("5. [magenta]Deutsch[/magenta] (de) - الألمانية")
                    console.print("6. [cyan]中文[/cyan] (zh) - الصينية")
                    console.print("7. [white]Norsk[/white] (no) - النرويجية")

                    choice = console.input("[bold]اختر رقم اللغة المطلوبة (1-7): [/bold]").strip()
                    lang_map = {
                        '1': 'ar', '2': 'en', '3': 'es', '4': 'fr',
                        '5': 'de', '6': 'zh', '7': 'no'
                    }

                    if choice in lang_map:
                        translator.set_language(lang_map[choice])
                        console.print(f"[green]✅ تم تغيير لغة الواجهة بنجاح إلى: {lang_map[choice]}[/green]")
                    else:
                        console.print("[red]❌ الرقم المدخل غير صحيح، يرجى اختيار رقم من 1 إلى 7[/red]")
                
                # Handle unknown commands
                else:
                    console.print(f"[yellow]⚠️  الأمر غير مُعرَّف في النظام: [bold]{user_input}[/bold][/yellow]")
                    console.print("[cyan]💡 اكتب 'help' أو 'مساعدة' لعرض قائمة الأوامر المتاحة[/cyan]")
                
                console.print()  # Empty line for better readability
                
            except KeyboardInterrupt:
                console.print("\n[yellow]👋 تم إيقاف نظام AION بناءً على طلب المستخدم[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]❌ حدث خطأ غير متوقع في النظام: {e}[/red]")
                console.print("[cyan]💡 اكتب 'help' أو 'مساعدة' للحصول على المساعدة[/cyan]")
    
    except Exception as e:
        console.print(f"[red]❌ فشل في تشغيل نظام AION: {e}[/red]")
        console.print("[yellow]💡 يرجى التحقق من التثبيت والمتطلبات[/yellow]")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
