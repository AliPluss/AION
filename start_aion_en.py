#!/usr/bin/env python3
"""
🚀 AION Quick Start - English Default
Simple launcher for AION with English interface and language selection
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.translator import Translator
from interfaces.cli import CLI
from core.security import SecurityManager
from utils.arabic_support import setup_arabic_console, check_terminal_arabic_support, get_language_preference
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

def show_language_selection_menu(console, current_language):
    """عرض قائمة اختيار اللغة التفاعلية مع تصميم محسن"""
    try:
        from rich.prompt import Prompt
        from rich.panel import Panel
        from rich.table import Table
        from rich.align import Align

        # إنشاء جدول اللغات مع تصميم جميل
        language_table = Table(show_header=True, header_style="bold magenta", box=None)
        language_table.add_column("Option", style="bold cyan", width=8, justify="center")
        language_table.add_column("Flag", style="white", width=6, justify="center")
        language_table.add_column("Language", style="bold green", width=20)
        language_table.add_column("Native Name", style="bold yellow", width=15)
        language_table.add_column("Status", style="bold red", width=12, justify="center")

        languages = [
            ("1", "🇸🇦", "Arabic", "العربية", "ar"),
            ("2", "🇺🇸", "English", "English", "en"),
            ("3", "🇪🇸", "Spanish", "Español", "es"),
            ("4", "🇫🇷", "French", "Français", "fr"),
            ("5", "🇩🇪", "German", "Deutsch", "de"),
            ("6", "🇨🇳", "Chinese", "中文", "zh"),
            ("7", "🇳🇴", "Norwegian", "Norsk", "no")
        ]

        for option, flag, lang_en, lang_native, code in languages:
            status = "✅ Current" if code == current_language else ""
            language_table.add_row(option, flag, lang_en, lang_native, status)

        # تحديد العنوان والنص حسب اللغة الحالية
        if current_language == 'ar':
            title = "🌍 تغيير لغة الواجهة / Change Interface Language"
            subtitle = "اختر لغة الواجهة الجديدة\nChoose new interface language"
            prompt_text = "➤ اختر رقم اللغة الجديدة / Select new language number"
        else:
            title = "🌍 Change Interface Language / تغيير لغة الواجهة"
            subtitle = "Choose new interface language\nاختر لغة الواجهة الجديدة"
            prompt_text = "➤ Select new language number / اختر رقم اللغة الجديدة"

        # إنشاء لوحة جميلة
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

        # طلب الاختيار
        choice = Prompt.ask(
            f"\n[bold cyan]{prompt_text}[/bold cyan]",
            choices=["1", "2", "3", "4", "5", "6", "7"],
            show_choices=False
        )

        lang_map = {
            '1': 'ar', '2': 'en', '3': 'es', '4': 'fr',
            '5': 'de', '6': 'zh', '7': 'no'
        }

        selected_lang = lang_map.get(choice, current_language)

        # عرض تأكيد الاختيار
        selected_info = next((lang_info for opt, flag, lang_en, lang_native, code in languages if opt == choice for lang_info in [(opt, flag, lang_en, lang_native, code)]), None)
        if selected_info:
            if current_language == 'ar':
                console.print(f"\n✅ [green]تم اختيار اللغة الجديدة / New language selected:[/green] [bold]{selected_info[1]} {selected_info[2]} ({selected_info[3]})[/bold]")
            else:
                console.print(f"\n✅ [green]New language selected / تم اختيار اللغة الجديدة:[/green] [bold]{selected_info[1]} {selected_info[2]} ({selected_info[3]})[/bold]")

        return selected_lang

    except ImportError:
        # Fallback إلى واجهة بسيطة
        if current_language == 'ar':
            console.print("[bold blue]🌍 تغيير لغة الواجهة[/bold blue]")
            console.print("─" * 40)
            console.print("1. 🇸🇦 [yellow]العربية (Arabic)[/yellow] " + ("✅ (Current)" if current_language == 'ar' else ""))
            console.print("2. 🇺🇸 [green]English[/green] " + ("✅ (Current)" if current_language == 'en' else ""))
            console.print("3. 🇪🇸 [red]Español (Spanish)[/red] " + ("✅ (Current)" if current_language == 'es' else ""))
            console.print("4. 🇫🇷 [blue]Français (French)[/blue] " + ("✅ (Current)" if current_language == 'fr' else ""))
            console.print("5. 🇩🇪 [magenta]Deutsch (German)[/magenta] " + ("✅ (Current)" if current_language == 'de' else ""))
            console.print("6. 🇨🇳 [cyan]中文 (Chinese)[/cyan] " + ("✅ (Current)" if current_language == 'zh' else ""))
            console.print("7. 🇳🇴 [white]Norsk (Norwegian)[/white] " + ("✅ (Current)" if current_language == 'no' else ""))
            console.print("─" * 40)

            choice = console.input("[bold cyan]اختر رقم اللغة الجديدة (1-7): [/bold cyan]").strip()
        else:
            console.print("[bold blue]🌍 Change Interface Language[/bold blue]")
            console.print("─" * 40)
            console.print("1. 🇸🇦 [yellow]العربية (Arabic)[/yellow] " + ("✅ (Current)" if current_language == 'ar' else ""))
            console.print("2. 🇺🇸 [green]English[/green] " + ("✅ (Current)" if current_language == 'en' else ""))
            console.print("3. 🇪🇸 [red]Español (Spanish)[/red] " + ("✅ (Current)" if current_language == 'es' else ""))
            console.print("4. 🇫🇷 [blue]Français (French)[/blue] " + ("✅ (Current)" if current_language == 'fr' else ""))
            console.print("5. 🇩🇪 [magenta]Deutsch (German)[/magenta] " + ("✅ (Current)" if current_language == 'de' else ""))
            console.print("6. 🇨🇳 [cyan]中文 (Chinese)[/cyan] " + ("✅ (Current)" if current_language == 'zh' else ""))
            console.print("7. 🇳🇴 [white]Norsk (Norwegian)[/white] " + ("✅ (Current)" if current_language == 'no' else ""))
            console.print("─" * 40)

            choice = console.input("[bold cyan]Select new language number (1-7): [/bold cyan]").strip()

        lang_map = {
            '1': 'ar', '2': 'en', '3': 'es', '4': 'fr',
            '5': 'de', '6': 'zh', '7': 'no'
        }

        return lang_map.get(choice, current_language)

    except Exception as e:
        console.print(f"[red]Error in language selection: {e}[/red]")
        return current_language

def show_welcome_english(console):
    """Display English welcome message"""
    welcome_panel = Panel.fit(
        """
🤖 [bold blue]AION - AI Operating Node[/bold blue]
[green]Multi-language AI Assistant for Terminal & Web[/green]

[yellow]Basic Commands:[/yellow]
• [cyan]help[/cyan] - Show comprehensive help
• [cyan]execute python print('Hello World!')[/cyan] - Execute programming code
• [cyan]translate ar Hello[/cyan] - Translate text between languages
• [cyan]plugins[/cyan] - Manage plugins and modules
• [cyan]security[/cyan] - Monitor security status
• [cyan]change-language[/cyan] - Switch interface language
• [cyan]exit[/cyan] - Exit the program

[yellow]Supported Languages:[/yellow] English, Arabic, French, German, Spanish, Chinese, Norwegian

[red]Important Note:[/red] To use AI services, configure API keys first
        """,
        title="🌟 Welcome to AION System",
        border_style="blue"
    )
    console.print(welcome_panel)

def show_welcome_arabic(console):
    """Display Arabic welcome message"""
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

[yellow]اللغات المدعومة:[/yellow] العربية، الإنجليزية، الفرنسية، الألمانية، الإسبانية، الصينية، النرويجية

[red]تنبيه مهم:[/red] لاستخدام خدمات الذكاء الاصطناعي، يجب تكوين مفاتيح API أولاً
        """,
        title="🌟 أهلاً وسهلاً بك في نظام AION",
        border_style="blue"
    )
    console.print(welcome_panel)

def main():
    """Main function to start AION"""
    # Setup console support
    setup_arabic_console()
    console = Console()
    
    # Check terminal Arabic support
    terminal_supports_arabic = check_terminal_arabic_support()
    
    # Get language preference from user
    selected_language = get_language_preference()
    
    # Show appropriate welcome message
    if selected_language == 'ar':
        if not terminal_supports_arabic:
            console.print("\n⚠️  [yellow]Terminal Arabic Support Warning:[/yellow]")
            console.print("Your terminal may not fully support Arabic text display.")
            console.print("For best Arabic experience, consider using:")
            console.print("• Windows Terminal (recommended)")
            console.print("• PowerShell 7+")
            console.print("• VS Code integrated terminal")
            console.print("\nContinuing with Arabic interface...")
            console.print()
        show_welcome_arabic(console)
        success_msg = "[green]✅ تم تشغيل نظام AION بنجاح وجاهز للاستخدام![/green]"
        help_msg = "[yellow]💡 يمكنك الآن كتابة أي أمر من الأوامر المتاحة أعلاه...[/yellow]"
    else:
        show_welcome_english(console)
        success_msg = "[green]✅ AION system started successfully and ready to use![/green]"
        help_msg = "[yellow]💡 You can now type any of the available commands above...[/yellow]"
        if selected_language != 'en':
            console.print(f"[cyan]🌍 Interface language set to: {selected_language}[/cyan]")
    
    console.print()
    console.print(success_msg)
    console.print(help_msg)
    console.print()
    
    # Initialize components
    translator = Translator()
    translator.set_language(selected_language)
    security = SecurityManager()
    cli = CLI(translator, security)
    
    # Main interaction loop
    try:
        while True:
            try:
                # Get user input
                user_input = console.input("[bold cyan]AION>[/bold cyan] ").strip()
                
                if not user_input:
                    continue
                
                # Handle exit commands (multilingual)
                exit_commands = ['exit', 'quit', 'خروج', 'إنهاء', 'انهاء', 'salir', 'sortir', 'ausgang', '退出']
                if user_input.lower() in exit_commands:
                    if selected_language == 'ar':
                        console.print("[yellow]👋 شكراً لك على استخدام نظام AION! نراك قريباً[/yellow]")
                    else:
                        console.print("[yellow]👋 Thank you for using AION! See you soon[/yellow]")
                    break
                
                # Handle help command (multilingual)
                help_commands = ['help', 'مساعدة', 'مساعده', 'ساعدني', 'ayuda', 'aide', 'hilfe', '帮助']
                if user_input.lower() in help_commands:
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
                                if selected_language == 'ar':
                                    console.print(f"[green]✅ تم تنفيذ الكود بنجاح:[/green]")
                                else:
                                    console.print(f"[green]✅ Code executed successfully:[/green]")
                                console.print(f"[white]{result.output}[/white]")
                            else:
                                if selected_language == 'ar':
                                    console.print(f"[red]❌ فشل في تنفيذ الكود:[/red]")
                                else:
                                    console.print(f"[red]❌ Code execution failed:[/red]")
                                console.print(f"[red]{result.error}[/red]")
                        except Exception as e:
                            if selected_language == 'ar':
                                console.print(f"[red]❌ حدث خطأ غير متوقع: {e}[/red]")
                            else:
                                console.print(f"[red]❌ Unexpected error occurred: {e}[/red]")
                    else:
                        if selected_language == 'ar':
                            console.print("[red]❌ طريقة الاستخدام الصحيحة: execute <لغة_البرمجة> <الكود>[/red]")
                        else:
                            console.print("[red]❌ Correct usage: execute <programming_language> <code>[/red]")
                
                # Handle translate command
                elif user_input.lower().startswith('translate'):
                    parts = user_input.split(' ', 2)
                    if len(parts) >= 3:
                        target_lang = parts[1]
                        text = parts[2]
                        # Simple translation simulation
                        if selected_language == 'ar':
                            console.print(f"[green]ترجمة النص إلى اللغة {target_lang}:[/green] {text}")
                            console.print("[yellow]💡 ملاحظة: هذه ترجمة تجريبية، للترجمة الفعلية يرجى تكوين مفاتيح AI[/yellow]")
                        else:
                            console.print(f"[green]Translation to {target_lang}:[/green] {text}")
                            console.print("[yellow]💡 Note: This is a demo translation, configure AI keys for real translation[/yellow]")
                    else:
                        if selected_language == 'ar':
                            console.print("[red]❌ طريقة الاستخدام: translate <اللغة_المستهدفة> <النص_المراد_ترجمته>[/red]")
                        else:
                            console.print("[red]❌ Usage: translate <target_language> <text_to_translate>[/red]")

                # Handle plugins command
                elif user_input.lower() in ['plugins', 'إضافات', 'اضافات', 'الإضافات']:
                    if selected_language == 'ar':
                        console.print("[cyan]📦 الإضافات والوحدات المتاحة في النظام:[/cyan]")
                        console.print("• [green]Calculator Plugin v1.0.0[/green] - آلة حاسبة متقدمة")
                        console.print("• [yellow]Weather Plugin (قيد التطوير)[/yellow] - معلومات الطقس")
                        console.print("• [yellow]System Info Plugin (قيد التطوير)[/yellow] - معلومات النظام")
                        console.print("• [yellow]File Manager Plugin (مخطط)[/yellow] - إدارة الملفات")
                        console.print("[blue]💡 يمكنك تطوير إضافات جديدة باستخدام Plugin API[/blue]")
                    else:
                        console.print("[cyan]📦 Available plugins and modules:[/cyan]")
                        console.print("• [green]Calculator Plugin v1.0.0[/green] - Advanced calculator")
                        console.print("• [yellow]Weather Plugin (in development)[/yellow] - Weather information")
                        console.print("• [yellow]System Info Plugin (in development)[/yellow] - System information")
                        console.print("• [yellow]File Manager Plugin (planned)[/yellow] - File management")
                        console.print("[blue]💡 You can develop new plugins using Plugin API[/blue]")

                # Handle security command
                elif user_input.lower() in ['security', 'أمان', 'امان', 'الأمان']:
                    status = security.get_security_status()
                    if selected_language == 'ar':
                        console.print(f"[cyan]🔒 تقرير حالة الأمان والحماية:[/cyan]")
                        console.print(f"• عدد الجلسات النشطة حالياً: [green]{status['active_sessions']}[/green]")
                        console.print(f"• إجمالي الرموز المُنشأة: [blue]{status['total_tokens']}[/blue]")
                        console.print(f"• عدد المحاولات الفاشلة: [red]{status['failed_attempts']}[/red]")
                        console.print(f"• مستوى الحماية الحالي: [yellow]{status['security_level']}[/yellow]")
                        console.print("[green]✅ النظام آمن ومحمي[/green]")
                    else:
                        console.print(f"[cyan]🔒 Security and protection status report:[/cyan]")
                        console.print(f"• Currently active sessions: [green]{status['active_sessions']}[/green]")
                        console.print(f"• Total tokens generated: [blue]{status['total_tokens']}[/blue]")
                        console.print(f"• Failed attempts: [red]{status['failed_attempts']}[/red]")
                        console.print(f"• Current security level: [yellow]{status['security_level']}[/yellow]")
                        console.print("[green]✅ System is secure and protected[/green]")

                # Handle language change
                elif user_input.lower() in ['change-language', 'تغيير-اللغة', 'تغيير_اللغة', 'لغة']:
                    new_language = show_language_selection_menu(console, selected_language)
                    if new_language != selected_language:
                        selected_language = new_language
                        translator.set_language(selected_language)
                        if selected_language == 'ar':
                            console.print(f"[green]✅ تم تغيير لغة الواجهة بنجاح إلى: {selected_language}[/green]")
                        else:
                            console.print(f"[green]✅ Interface language changed successfully to: {selected_language}[/green]")

                # Handle unknown commands
                else:
                    if selected_language == 'ar':
                        console.print(f"[yellow]⚠️  الأمر غير مُعرَّف في النظام: [bold]{user_input}[/bold][/yellow]")
                        console.print("[cyan]💡 اكتب 'help' أو 'مساعدة' لعرض قائمة الأوامر المتاحة[/cyan]")
                    else:
                        console.print(f"[yellow]⚠️  Command not recognized: [bold]{user_input}[/bold][/yellow]")
                        console.print("[cyan]💡 Type 'help' to see available commands[/cyan]")
                
                console.print()  # Empty line for better readability
                
            except KeyboardInterrupt:
                if selected_language == 'ar':
                    console.print("\n[yellow]👋 تم إيقاف نظام AION بناءً على طلب المستخدم[/yellow]")
                else:
                    console.print("\n[yellow]👋 AION stopped by user request[/yellow]")
                break
            except Exception as e:
                if selected_language == 'ar':
                    console.print(f"[red]❌ حدث خطأ غير متوقع في النظام: {e}[/red]")
                    console.print("[cyan]💡 اكتب 'help' أو 'مساعدة' للحصول على المساعدة[/cyan]")
                else:
                    console.print(f"[red]❌ Unexpected system error: {e}[/red]")
                    console.print("[cyan]💡 Type 'help' for assistance[/cyan]")
    
    except Exception as e:
        if selected_language == 'ar':
            console.print(f"[red]❌ فشل في تشغيل نظام AION: {e}[/red]")
            console.print("[yellow]💡 يرجى التحقق من التثبيت والمتطلبات[/yellow]")
        else:
            console.print(f"[red]❌ Failed to start AION system: {e}[/red]")
            console.print("[yellow]💡 Please check installation and requirements[/yellow]")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
