#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 AION - AI Operating Node
Main Application File
"""

import os
import sys
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
import typer

# Setup encoding for Arabic support
if sys.platform == "win32":
    os.system('chcp 65001 >nul 2>&1')
    os.environ["PYTHONIOENCODING"] = "utf-8"

console = Console()
app = typer.Typer(rich_markup_mode="rich")

class AIONApp:
    def __init__(self):
        self.config_dir = Path("config")
        self.load_config()
        self.load_language()
    
    def load_config(self):
        """Load configuration"""
        try:
            with open(self.config_dir / "config.json", "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {"app": {"language": "ar"}}
    
    def load_language(self):
        """Load language translations"""
        lang = self.config.get("app", {}).get("language", "ar")
        try:
            with open(self.config_dir / f"lang_{lang}.json", "r", encoding="utf-8") as f:
                self.lang = json.load(f)
        except FileNotFoundError:
            self.lang = {"welcome": "Welcome to AION"}
    
    def show_welcome(self):
        """Show welcome screen"""
        welcome_text = f"""
[bold blue]🧠 AION - AI Operating Node[/bold blue]
[green]{self.lang.get('welcome', 'Welcome to AION')}[/green]
[yellow]Enhanced Terminal Assistant v2.0.0[/yellow]
        """
        
        panel = Panel(
            welcome_text.strip(),
            title="🤖 AION",
            border_style="bright_blue"
        )
        
        console.print(panel)
    
    def show_menu(self):
        """Show main menu"""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("🔢", style="cyan", width=4)
        table.add_column("الوظيفة | Function", style="green", width=25)
        table.add_column("الوصف | Description", style="white", width=35)
        
        menu_items = [
            ("1", "🤖 " + self.lang.get("ai_assistant", "AI Assistant"), "محادثة مع الذكاء الاصطناعي"),
            ("2", "⚡ " + self.lang.get("code_execution", "Code Execution"), "تنفيذ الأكواد البرمجية"),
            ("3", "🧩 " + self.lang.get("plugin_manager", "Plugin Manager"), "إدارة الإضافات والتوسعات"),
            ("4", "🎤 " + self.lang.get("voice_mode", "Voice Mode"), "التحكم بالأوامر الصوتية"),
            ("5", "⚙️ " + self.lang.get("settings", "Settings"), "الإعدادات والتخصيص"),
            ("6", "❓ " + self.lang.get("help", "Help"), "المساعدة والدليل"),
            ("0", "🚪 " + self.lang.get("exit", "Exit"), "خروج من البرنامج")
        ]
        
        for num, func, desc in menu_items:
            table.add_row(num, func, desc)
        
        menu_panel = Panel(
            table,
            title="[bold blue]🎯 القائمة الرئيسية | Main Menu[/bold blue]",
            border_style="green"
        )
        
        console.print(menu_panel)
    
    async def run(self):
        """Run the main application"""
        self.show_welcome()

        while True:
            console.print()
            self.show_menu()

            choice = Prompt.ask(
                "\n[cyan]اختر رقم الوظيفة | Select function number[/cyan]",
                choices=["0", "1", "2", "3", "4", "5", "6"],
                default="1"
            )

            if choice == "0":
                console.print("\n[green]🙏 شكراً لاستخدام AION! | Thank you for using AION![/green]")
                break
            elif choice == "1":
                console.print("\n[yellow]🤖 بدء مساعد الذكاء الاصطناعي...[/yellow]")
                console.print("[dim]⚠️ هذه الميزة قيد التطوير | This feature is under development[/dim]")
            elif choice == "2":
                await self.show_code_execution()
            elif choice == "3":
                self.show_plugin_manager()
            elif choice == "4":
                console.print("\n[yellow]🎤 بدء الوضع الصوتي...[/yellow]")
                console.print("[dim]⚠️ هذه الميزة قيد التطوير | This feature is under development[/dim]")
            elif choice == "5":
                self.show_settings()
            elif choice == "6":
                self.show_help()

    async def show_code_execution(self):
        """Show code execution interface with enhanced Rust and C++ support"""
        console.print("\n[bold blue]⚡ تنفيذ الكود متعدد اللغات | Multi-Language Code Execution[/bold blue]")

        # Simple built-in code execution for now
        available_languages = {
            "python": {"name": "Python", "icon": "🐍", "performance": "متوسط", "available": True},
            "javascript": {"name": "JavaScript", "icon": "🟨", "performance": "متوسط", "available": True},
            "rust": {"name": "Rust", "icon": "🦀", "performance": "عالي جداً", "available": False},
            "cpp": {"name": "C++", "icon": "⚡", "performance": "عالي جداً", "available": False}
        }

        # Check for available compilers
        import subprocess
        try:
            subprocess.run(["rustc", "--version"], capture_output=True, check=True)
            available_languages["rust"]["available"] = True
        except:
            pass

        try:
            subprocess.run(["g++", "--version"], capture_output=True, check=True)
            available_languages["cpp"]["available"] = True
        except:
            pass

        while True:
            console.print("\n" + "="*60)
            console.print("[bold cyan]🚀 مشغل الكود AION | AION Code Executor[/bold cyan]")
            console.print("="*60)

            table = Table(show_header=True, header_style="bold magenta", width=55)
            table.add_column("الخيار | Option", style="cyan", width=8)
            table.add_column("الوظيفة | Function", style="green", width=25)
            table.add_column("الوصف | Description", style="white", width=22)

            menu_items = [
                ("1", "🏃 " + "تشغيل كود | Run Code", "تنفيذ كود تفاعلي"),
                ("2", "🌐 " + "اللغات المتاحة | Languages", "عرض اللغات المدعومة"),
                ("3", "📝 " + "أمثلة الكود | Samples", "عرض أمثلة جاهزة"),
                ("0", "🔙 " + "العودة | Back", "العودة للقائمة الرئيسية")
            ]

            for option, function, description in menu_items:
                table.add_row(option, function, description)

            console.print(table)

            choice = Prompt.ask("\n[bold yellow]اختر خيار | Choose option[/bold yellow]",
                              choices=["0", "1", "2", "3"], default="1")

            if choice == "0":
                break
            elif choice == "1":
                await self._run_simple_code()
            elif choice == "2":
                self._show_available_languages(available_languages)
            elif choice == "3":
                self._show_code_samples()

            input("\n[dim]اضغط Enter للمتابعة | Press Enter to continue...[/dim]")

    async def _run_simple_code(self):
        """Simple code execution"""
        console.print("\n[bold green]💻 تشغيل الكود | Code Execution[/bold green]")

        # Language selection
        languages = ["python", "javascript"]
        console.print("اختر لغة البرمجة:")
        console.print("1. 🐍 Python")
        console.print("2. 🟨 JavaScript")

        choice = Prompt.ask("اختر رقم اللغة", choices=["1", "2"], default="1")

        if choice == "1":
            lang = "python"
            console.print("✅ تم اختيار Python")
        else:
            lang = "javascript"
            console.print("✅ تم اختيار JavaScript")

        console.print("أدخل الكود (اكتب 'END' في سطر منفصل للانتهاء):")

        code_lines = []
        while True:
            try:
                line = input()
                if line.strip() == "END":
                    break
                code_lines.append(line)
            except KeyboardInterrupt:
                console.print("\n❌ تم الإلغاء")
                return

        code = "\n".join(code_lines)
        if not code.strip():
            console.print("❌ لم يتم إدخال أي كود")
            return

        # Execute code
        console.print(f"\n🚀 تشغيل كود {lang.upper()}...")

        try:
            import tempfile
            import subprocess

            with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{lang}', delete=False, encoding='utf-8') as f:
                f.write(code)
                temp_file = f.name

            if lang == "python":
                result = subprocess.run([sys.executable, temp_file],
                                      capture_output=True, text=True, timeout=30, encoding='utf-8')
            else:  # javascript
                result = subprocess.run(["node", temp_file],
                                      capture_output=True, text=True, timeout=30, encoding='utf-8')

            # Display results
            if result.returncode == 0:
                console.print(f"[green]✅ تم تنفيذ الكود بنجاح![/green]")
                if result.stdout:
                    console.print(f"[blue]📤 المخرجات:[/blue]\n{result.stdout}")
            else:
                console.print(f"[red]❌ خطأ في التنفيذ![/red]")
                if result.stderr:
                    console.print(f"[red]🚨 الخطأ:[/red]\n{result.stderr}")

            # Cleanup
            import os
            os.unlink(temp_file)

        except subprocess.TimeoutExpired:
            console.print("[red]❌ انتهت مهلة التنفيذ (30 ثانية)[/red]")
        except FileNotFoundError:
            console.print(f"[red]❌ {lang} غير مثبت على النظام[/red]")
        except Exception as e:
            console.print(f"[red]❌ خطأ: {str(e)}[/red]")

    def _show_available_languages(self, languages):
        """Show available programming languages"""
        console.print("\n[bold cyan]🌐 اللغات المتاحة | Available Languages[/bold cyan]")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("اللغة | Language", style="cyan")
        table.add_column("الأداء | Performance", justify="center")
        table.add_column("الحالة | Status", justify="center")

        for lang_key, lang_info in languages.items():
            status = "✅ متاح" if lang_info["available"] else "❌ غير مثبت"
            status_style = "green" if lang_info["available"] else "red"

            table.add_row(
                f"{lang_info['icon']} {lang_info['name']}",
                lang_info["performance"],
                f"[{status_style}]{status}[/{status_style}]"
            )

        console.print(table)

        console.print("\n[yellow]💡 لتثبيت اللغات المفقودة:[/yellow]")
        console.print("• Rust: https://rustup.rs/")
        console.print("• C++: Visual Studio Build Tools أو MinGW-w64")

    def _show_code_samples(self):
        """Show code samples"""
        console.print("\n[bold green]📝 أمثلة الكود | Code Samples[/bold green]")

        samples = {
            "Python": '''# مثال Python - حساب الأعداد الأولية
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

primes = [i for i in range(2, 50) if is_prime(i)]
print("الأعداد الأولية:", primes)''',

            "JavaScript": '''// مثال JavaScript - حساب فيبوناتشي
function fibonacci(n) {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
}

console.log("سلسلة فيبوناتشي:");
for (let i = 0; i < 10; i++) {
    console.log(`F(${i}) = ${fibonacci(i)}`);
}''',

            "Rust": '''// مثال Rust - أداء عالي
fn main() {
    let numbers: Vec<i32> = (1..=1000000).collect();
    let sum: i32 = numbers.iter().sum();
    println!("مجموع الأرقام: {}", sum);

    let squares: Vec<i32> = numbers.iter()
        .map(|x| x * x)
        .take(10)
        .collect();
    println!("المربعات الأولى: {:?}", squares);
}''',

            "C++": '''// مثال C++ - أداء عالي
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> numbers;
    for (int i = 1; i <= 1000000; ++i) {
        numbers.push_back(i);
    }

    long long sum = 0;
    for (int n : numbers) {
        sum += n;
    }

    std::cout << "مجموع الأرقام: " << sum << std::endl;
    return 0;
}'''
        }

        for lang, code in samples.items():
            console.print(f"\n[bold yellow]{lang}:[/bold yellow]")
            console.print(Panel(code, border_style="blue"))

    def show_plugin_manager(self):
        """Show plugin manager interface"""
        try:
            # Import plugin manager
            sys.path.append(str(Path("src/plugins")))
            from plugin_manager import PluginManager

            plugin_manager = PluginManager()

            while True:
                console.print("\n[bold blue]🧩 مدير الإضافات | Plugin Manager[/bold blue]")

                # Plugin management menu
                plugin_table = Table(show_header=True, header_style="bold magenta")
                plugin_table.add_column("🔢", style="cyan", width=4)
                plugin_table.add_column("الوظيفة | Function", style="green", width=25)
                plugin_table.add_column("الوصف | Description", style="white", width=35)

                plugin_menu_items = [
                    ("1", "📋 عرض الإضافات | List Plugins", "عرض جميع الإضافات المتاحة"),
                    ("2", "🔄 تحميل الإضافات | Load Plugins", "تحميل جميع الإضافات"),
                    ("3", "🧮 تجربة الآلة الحاسبة | Try Calculator", "تجربة إضافة الآلة الحاسبة"),
                    ("4", "📊 أوامر الإضافات | Plugin Commands", "عرض أوامر الإضافات"),
                    ("0", "🔙 العودة | Back", "العودة للقائمة الرئيسية")
                ]

                for num, func, desc in plugin_menu_items:
                    plugin_table.add_row(num, func, desc)

                plugin_panel = Panel(
                    plugin_table,
                    title="[bold blue]🧩 إدارة الإضافات | Plugin Management[/bold blue]",
                    border_style="cyan"
                )

                console.print(plugin_panel)

                plugin_choice = Prompt.ask(
                    "\n[cyan]اختر رقم الوظيفة | Select function number[/cyan]",
                    choices=["0", "1", "2", "3", "4"],
                    default="1"
                )

                if plugin_choice == "0":
                    break
                elif plugin_choice == "1":
                    console.print("\n[yellow]📋 عرض الإضافات المتاحة...[/yellow]")
                    plugin_manager.list_plugins()
                elif plugin_choice == "2":
                    console.print("\n[yellow]🔄 تحميل الإضافات...[/yellow]")
                    loaded_count = plugin_manager.load_all_plugins()
                    console.print(f"[green]✅ تم تحميل {loaded_count} إضافة بنجاح[/green]")
                elif plugin_choice == "3":
                    self.demo_calculator_plugin(plugin_manager)
                elif plugin_choice == "4":
                    console.print("\n[yellow]📊 أوامر الإضافات المتاحة...[/yellow]")
                    commands = plugin_manager.get_all_commands()
                    if commands:
                        for plugin_name, plugin_commands in commands.items():
                            console.print(f"[cyan]🧩 {plugin_name}:[/cyan] {', '.join(plugin_commands)}")
                    else:
                        console.print("[yellow]⚠️ لا توجد إضافات محملة[/yellow]")

        except ImportError as e:
            console.print(f"[red]❌ خطأ في تحميل مدير الإضافات: {e}[/red]")
            console.print("[yellow]💡 تأكد من تشغيل الإعداد بشكل صحيح[/yellow]")

    def demo_calculator_plugin(self, plugin_manager):
        """Demo calculator plugin functionality"""
        console.print("\n[bold blue]🧮 تجربة إضافة الآلة الحاسبة | Calculator Plugin Demo[/bold blue]")

        # Load calculator plugin if not loaded
        if "calculator_plugin" not in plugin_manager.loaded_plugins:
            if not plugin_manager.load_plugin("calculator_plugin"):
                console.print("[red]❌ فشل في تحميل إضافة الآلة الحاسبة[/red]")
                return

        while True:
            console.print("\n[green]أمثلة على العمليات الحسابية:[/green]")
            console.print("• add 5 3 2 (الجمع)")
            console.print("• subtract 10 3 (الطرح)")
            console.print("• multiply 4 5 (الضرب)")
            console.print("• divide 15 3 (القسمة)")
            console.print("• sqrt 16 (الجذر التربيعي)")
            console.print("• power 2 3 (الأس)")
            console.print("• exit (للخروج)")

            user_input = Prompt.ask("\n[cyan]أدخل العملية | Enter operation[/cyan]")

            if user_input.lower() == "exit":
                break

            parts = user_input.split()
            if len(parts) < 2:
                console.print("[red]❌ صيغة خاطئة. مثال: add 5 3[/red]")
                continue

            command = parts[0]
            args = parts[1:]

            result = plugin_manager.execute_plugin_command("calculator_plugin", command, args)

            if result and result.get("success"):
                console.print(f"[green]✅ النتيجة: {result['result']} ({result['operation']})[/green]")
            elif result:
                console.print(f"[red]❌ خطأ: {result.get('error', 'Unknown error')}[/red]")
            else:
                console.print("[red]❌ فشل في تنفيذ العملية[/red]")
    
    def show_help(self):
        """Show help information"""
        help_text = """
[bold blue]🧠 AION - دليل المساعدة | Help Guide[/bold blue]

[green]الوظائف المتاحة | Available Functions:[/green]
• مساعد الذكاء الاصطناعي - محادثة ذكية مع AI
• تنفيذ الكود - تشغيل أكواد متعددة اللغات  
• الوضع الصوتي - التحكم بالأوامر الصوتية
• الإعدادات - تخصيص النظام حسب احتياجاتك

[yellow]للمزيد من المعلومات، قم بزيارة الوثائق الرسمية[/yellow]
        """
        
        help_panel = Panel(
            help_text.strip(),
            title="[bold blue]❓ المساعدة | Help[/bold blue]",
            border_style="yellow"
        )
        
        console.print(help_panel)
        input("\nاضغط Enter للمتابعة | Press Enter to continue...")

    def show_settings(self):
        """عرض قائمة الإعدادات"""
        while True:
            console.clear()
            console.print(Panel(
                f"🧠 AION - AI Operating Node\nمرحباً بك في AION\n\nEnhanced Terminal Assistant v{self.config['app']['version']}",
                title="🤖 AION",
                border_style="cyan"
            ))

            # إنشاء جدول الإعدادات
            settings_table = Table(show_header=True, header_style="bold magenta")
            settings_table.add_column("🔢", style="cyan", width=6)
            settings_table.add_column("الوظيفة | Function", style="white", width=25)
            settings_table.add_column("الوصف | Description", style="dim white", width=35)

            settings_table.add_row("1", "🤖 اختيار نموذج الذكاء الاصطناعي", "تغيير نموذج الذكاء الاصطناعي")
            settings_table.add_row("2", "🌐 تغيير اللغة | Change Language", "تغيير لغة الواجهة")
            settings_table.add_row("3", "🎨 تغيير المظهر | Change Theme", "تغيير مظهر التطبيق")
            settings_table.add_row("0", "🔙 العودة | Back", "العودة للقائمة الرئيسية")

            console.print(Panel(settings_table, title="⚙️ الإعدادات | Settings", border_style="green"))

            choice = Prompt.ask(
                "اختر رقم الوظيفة | Select function number [0/1/2/3]",
                choices=["0", "1", "2", "3"],
                default="1"
            )

            if choice == "0":
                break
            elif choice == "1":
                self.show_ai_model_selection()
            elif choice == "2":
                console.print("\n[yellow]🌐 تغيير اللغة...[/yellow]")
                console.print("[dim]⚠️ هذه الميزة قيد التطوير | This feature is under development[/dim]")
                input("\nاضغط Enter للمتابعة | Press Enter to continue...")
            elif choice == "3":
                console.print("\n[yellow]🎨 تغيير المظهر...[/yellow]")
                console.print("[dim]⚠️ هذه الميزة قيد التطوير | This feature is under development[/dim]")
                input("\nاضغط Enter للمتابعة | Press Enter to continue...")

    def show_ai_model_selection(self):
        """عرض واجهة اختيار نموذج الذكاء الاصطناعي"""
        while True:
            console.clear()
            console.print(Panel(
                f"🤖 اختيار نموذج الذكاء الاصطناعي | AI Model Selection\n\nالنموذج الحالي: {self.config['ai']['current_model']}",
                title="🧠 AION AI Models",
                border_style="cyan"
            ))

            # عرض المزودين المتاحين
            providers_table = Table(show_header=True, header_style="bold magenta")
            providers_table.add_column("🔢", style="cyan", width=6)
            providers_table.add_column("المزود | Provider", style="white", width=20)
            providers_table.add_column("الوصف | Description", style="dim white", width=30)

            provider_list = list(self.config['ai']['providers'].keys())
            for i, provider_key in enumerate(provider_list, 1):
                provider = self.config['ai']['providers'][provider_key]
                providers_table.add_row(str(i), provider['name'], f"عدد النماذج: {len(provider['models'])}")

            providers_table.add_row("0", "🔙 العودة | Back", "العودة للإعدادات")

            console.print(Panel(providers_table, title="🏢 مزودي الذكاء الاصطناعي | AI Providers", border_style="blue"))

            choice = Prompt.ask(
                f"اختر المزود | Select provider [0-{len(provider_list)}]",
                choices=[str(i) for i in range(len(provider_list) + 1)],
                default="1"
            )

            if choice == "0":
                break
            else:
                provider_key = provider_list[int(choice) - 1]
                self.show_model_selection(provider_key)

    def show_model_selection(self, provider_key):
        """عرض نماذج مزود معين"""
        provider = self.config['ai']['providers'][provider_key]

        while True:
            console.clear()
            console.print(Panel(
                f"🤖 نماذج {provider['name']} | {provider['name']} Models\n\nالنموذج الحالي: {self.config['ai']['current_model']}",
                title=f"🧠 {provider['name']}",
                border_style="cyan"
            ))

            # عرض النماذج المتاحة
            models_table = Table(show_header=True, header_style="bold magenta")
            models_table.add_column("🔢", style="cyan", width=6)
            models_table.add_column("النموذج | Model", style="white", width=20)
            models_table.add_column("الوصف | Description", style="dim white", width=30)
            models_table.add_column("التكلفة | Cost", style="yellow", width=10)

            model_list = list(provider['models'].keys())
            for i, model_key in enumerate(model_list, 1):
                model = provider['models'][model_key]
                current_indicator = "✅ " if model_key == self.config['ai']['current_model'] else ""
                models_table.add_row(
                    str(i),
                    f"{current_indicator}{model['name']}",
                    model['description'],
                    model['cost']
                )

            models_table.add_row("0", "🔙 العودة | Back", "العودة لاختيار المزود", "")

            console.print(Panel(models_table, title=f"🤖 نماذج {provider['name']} | {provider['name']} Models", border_style="green"))

            choice = Prompt.ask(
                f"اختر النموذج | Select model [0-{len(model_list)}]",
                choices=[str(i) for i in range(len(model_list) + 1)],
                default="1"
            )

            if choice == "0":
                break
            else:
                model_key = model_list[int(choice) - 1]
                self.change_ai_model(provider_key, model_key)

    def change_ai_model(self, provider_key, model_key):
        """تغيير نموذج الذكاء الاصطناعي"""
        try:
            # تحديث الإعدادات
            self.config['ai']['default_provider'] = provider_key
            self.config['ai']['current_model'] = model_key

            # حفظ الإعدادات
            config_path = self.config_dir / "config.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)

            model_info = self.config['ai']['providers'][provider_key]['models'][model_key]

            console.print(f"\n✅ [green]تم تغيير النموذج بنجاح![/green]")
            console.print(f"🤖 النموذج الجديد: {model_info['name']}")
            console.print(f"📝 الوصف: {model_info['description']}")
            console.print(f"💰 التكلفة: {model_info['cost']}")
            console.print(f"🔢 أقصى رموز: {model_info['max_tokens']}")

            input("\nاضغط Enter للمتابعة | Press Enter to continue...")

        except Exception as e:
            console.print(f"\n❌ [red]خطأ في تغيير النموذج: {str(e)}[/red]")
            input("\nاضغط Enter للمتابعة | Press Enter to continue...")

@app.command()
def start():
    """🚀 Start AION interactive mode"""
    import asyncio
    aion_app = AIONApp()
    asyncio.run(aion_app.run())

@app.command()
def ai():
    """🤖 Quick AI assistant"""
    console.print("\n[yellow]🤖 بدء مساعد الذكاء الاصطناعي...[/yellow]")
    console.print("[dim]⚠️ هذه الميزة قيد التطوير | This feature is under development[/dim]")

@app.command()
def version():
    """📋 Show version information"""
    console.print("[bold blue]🧠 AION v2.0.0[/bold blue]")
    console.print("[green]AI Operating Node - Enhanced Terminal Assistant[/green]")

if __name__ == "__main__":
    app()
