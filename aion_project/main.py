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
            self.config = {"app": {"language": "en"}}
    
    def load_language(self):
        """Load language translations"""
        lang = self.config.get("app", {}).get("language", "en")
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
        table.add_column("Function", style="green", width=25)
        table.add_column("Description", style="white", width=35)
        
        menu_items = [
            ("1", "🤖 " + self.lang.get("ai_assistant", "AI Assistant"), "Chat with AI assistant"),
            ("2", "⚡ " + self.lang.get("code_execution", "Code Execution"), "Execute programming code"),
            ("3", "🧩 " + self.lang.get("plugin_manager", "Plugin Manager"), "Manage plugins and extensions"),
            ("4", "🎤 " + self.lang.get("voice_mode", "Voice Mode"), "Voice command control"),
            ("5", "⚙️ " + self.lang.get("settings", "Settings"), "Settings and customization"),
            ("6", "❓ " + self.lang.get("help", "Help"), "Help and guide"),
            ("0", "🚪 " + self.lang.get("exit", "Exit"), "Exit the program")
        ]
        
        for num, func, desc in menu_items:
            table.add_row(num, func, desc)
        
        menu_panel = Panel(
            table,
            title="[bold blue]🎯 Main Menu[/bold blue]",
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
                "\n[cyan]Select function number[/cyan]",
                choices=["0", "1", "2", "3", "4", "5", "6"],
                default="1"
            )

            if choice == "0":
                console.print("\n[green]🙏 Thank you for using AION![/green]")
                break
            elif choice == "1":
                console.print("\n[yellow]🤖 Starting AI assistant...[/yellow]")
                console.print("[dim]⚠️ This feature is under development[/dim]")
            elif choice == "2":
                await self.show_code_execution()
            elif choice == "3":
                self.show_plugin_manager()
            elif choice == "4":
                console.print("\n[yellow]🎤 Starting voice mode...[/yellow]")
                console.print("[dim]⚠️ This feature is under development[/dim]")
            elif choice == "5":
                self.show_settings()
            elif choice == "6":
                self.show_help()

    async def show_code_execution(self):
        """Show code execution interface with enhanced Rust and C++ support"""
        console.print("\n[bold blue]⚡ Multi-Language Code Execution[/bold blue]")

        # Simple built-in code execution for now
        available_languages = {
            "python": {"name": "Python", "icon": "🐍", "performance": "Medium", "available": True},
            "javascript": {"name": "JavaScript", "icon": "🟨", "performance": "Medium", "available": True},
            "rust": {"name": "Rust", "icon": "🦀", "performance": "Very High", "available": False},
            "cpp": {"name": "C++", "icon": "⚡", "performance": "Very High", "available": False}
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
            console.print("[bold cyan]🚀 AION Code Executor[/bold cyan]")
            console.print("="*60)

            table = Table(show_header=True, header_style="bold magenta", width=55)
            table.add_column("Option", style="cyan", width=8)
            table.add_column("Function", style="green", width=25)
            table.add_column("Description", style="white", width=22)

            menu_items = [
                ("1", "🏃 Run Code", "Execute interactive code"),
                ("2", "🌐 Languages", "Show supported languages"),
                ("3", "📝 Samples", "Show code samples"),
                ("0", "🔙 Back", "Back to main menu")
            ]

            for option, function, description in menu_items:
                table.add_row(option, function, description)

            console.print(table)

            choice = Prompt.ask("\n[bold yellow]Choose option[/bold yellow]",
                              choices=["0", "1", "2", "3"], default="1")

            if choice == "0":
                break
            elif choice == "1":
                await self._run_simple_code()
            elif choice == "2":
                self._show_available_languages(available_languages)
            elif choice == "3":
                self._show_code_samples()

            input("\n[dim]Press Enter to continue...[/dim]")

    async def _run_simple_code(self):
        """Simple code execution"""
        console.print("\n[bold green]💻 Code Execution[/bold green]")

        # Language selection
        languages = ["python", "javascript"]
        console.print("Choose programming language:")
        console.print("1. 🐍 Python")
        console.print("2. 🟨 JavaScript")

        choice = Prompt.ask("Choose language number", choices=["1", "2"], default="1")

        if choice == "1":
            lang = "python"
            console.print("✅ Python selected")
        else:
            lang = "javascript"
            console.print("✅ JavaScript selected")

        console.print("Enter code (type 'END' on a separate line to finish):")

        code_lines = []
        while True:
            try:
                line = input()
                if line.strip() == "END":
                    break
                code_lines.append(line)
            except KeyboardInterrupt:
                console.print("\n❌ Cancelled")
                return

        code = "\n".join(code_lines)
        if not code.strip():
            console.print("❌ No code entered")
            return

        # Execute code
        console.print(f"\n🚀 Running {lang.upper()} code...")

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
                console.print(f"[green]✅ Code executed successfully![/green]")
                if result.stdout:
                    console.print(f"[blue]📤 Output:[/blue]\n{result.stdout}")
            else:
                console.print(f"[red]❌ Execution error![/red]")
                if result.stderr:
                    console.print(f"[red]🚨 Error:[/red]\n{result.stderr}")

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
                    ("1", "📋 List Plugins", "Show all available plugins"),
                    ("2", "🔄 Load Plugins", "Load all plugins"),
                    ("3", "🧮 Try Calculator", "Test calculator plugin"),
                    ("4", "📊 Plugin Commands", "Show plugin commands"),
                    ("0", "🔙 Back", "Back to main menu")
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
                    "\n[cyan]Select function number[/cyan]",
                    choices=["0", "1", "2", "3", "4"],
                    default="1"
                )

                if plugin_choice == "0":
                    break
                elif plugin_choice == "1":
                    console.print("\n[yellow]📋 Listing available plugins...[/yellow]")
                    plugin_manager.list_plugins()
                elif plugin_choice == "2":
                    console.print("\n[yellow]🔄 Loading plugins...[/yellow]")
                    loaded_count = plugin_manager.load_all_plugins()
                    console.print(f"[green]✅ Successfully loaded {loaded_count} plugins[/green]")
                elif plugin_choice == "3":
                    self.demo_calculator_plugin(plugin_manager)
                elif plugin_choice == "4":
                    console.print("\n[yellow]📊 Available plugin commands...[/yellow]")
                    commands = plugin_manager.get_all_commands()
                    if commands:
                        for plugin_name, plugin_commands in commands.items():
                            console.print(f"[cyan]🧩 {plugin_name}:[/cyan] {', '.join(plugin_commands)}")
                    else:
                        console.print("[yellow]⚠️ No plugins loaded[/yellow]")

        except ImportError as e:
            console.print(f"[red]❌ Error loading plugin manager: {e}[/red]")
            console.print("[yellow]💡 Make sure to run setup correctly[/yellow]")

    def demo_calculator_plugin(self, plugin_manager):
        """Demo calculator plugin functionality"""
        console.print("\n[bold blue]🧮 Calculator Plugin Demo[/bold blue]")

        # Load calculator plugin if not loaded
        if "calculator_plugin" not in plugin_manager.loaded_plugins:
            if not plugin_manager.load_plugin("calculator_plugin"):
                console.print("[red]❌ Failed to load calculator plugin[/red]")
                return

        while True:
            console.print("\n[green]Mathematical operation examples:[/green]")
            console.print("• add 5 3 2 (addition)")
            console.print("• subtract 10 3 (subtraction)")
            console.print("• multiply 4 5 (multiplication)")
            console.print("• divide 15 3 (division)")
            console.print("• sqrt 16 (square root)")
            console.print("• power 2 3 (exponentiation)")
            console.print("• exit (to exit)")

            user_input = Prompt.ask("\n[cyan]Enter operation[/cyan]")

            if user_input.lower() == "exit":
                break

            parts = user_input.split()
            if len(parts) < 2:
                console.print("[red]❌ Wrong format. Example: add 5 3[/red]")
                continue

            command = parts[0]
            args = parts[1:]

            result = plugin_manager.execute_plugin_command("calculator_plugin", command, args)

            if result and result.get("success"):
                console.print(f"[green]✅ Result: {result['result']} ({result['operation']})[/green]")
            elif result:
                console.print(f"[red]❌ Error: {result.get('error', 'Unknown error')}[/red]")
            else:
                console.print("[red]❌ Failed to execute operation[/red]")
    
    def show_help(self):
        """Show help information"""
        help_text = """
[bold blue]🧠 AION - Help Guide[/bold blue]

[green]Available Functions:[/green]
• AI Assistant - Smart conversation with AI
• Code Execution - Run multi-language code
• Voice Mode - Voice command control
• Settings - Customize system to your needs

[yellow]For more information, visit the official documentation[/yellow]
        """

        help_panel = Panel(
            help_text.strip(),
            title="[bold blue]❓ Help[/bold blue]",
            border_style="yellow"
        )

        console.print(help_panel)
        input("\nPress Enter to continue...")

    def show_settings(self):
        """Show settings menu"""
        while True:
            console.clear()
            console.print(Panel(
                f"🧠 AION - AI Operating Node\nWelcome to AION\n\nEnhanced Terminal Assistant v{self.config['app']['version']}",
                title="🤖 AION",
                border_style="cyan"
            ))

            # Create settings table
            settings_table = Table(show_header=True, header_style="bold magenta")
            settings_table.add_column("🔢", style="cyan", width=6)
            settings_table.add_column("Function", style="white", width=25)
            settings_table.add_column("Description", style="dim white", width=35)

            settings_table.add_row("1", "🤖 AI Model Selection", "Change AI model")
            settings_table.add_row("2", "🌐 Change Language", "Change interface language")
            settings_table.add_row("3", "🎨 Change Theme", "Change application theme")
            settings_table.add_row("0", "🔙 Back", "Back to main menu")

            console.print(Panel(settings_table, title="⚙️ Settings", border_style="green"))

            choice = Prompt.ask(
                "Select function number [0/1/2/3]",
                choices=["0", "1", "2", "3"],
                default="1"
            )

            if choice == "0":
                break
            elif choice == "1":
                self.show_ai_model_selection()
            elif choice == "2":
                console.print("\n[yellow]🌐 Changing language...[/yellow]")
                console.print("[dim]⚠️ This feature is under development[/dim]")
                input("\nPress Enter to continue...")
            elif choice == "3":
                console.print("\n[yellow]🎨 Changing theme...[/yellow]")
                console.print("[dim]⚠️ This feature is under development[/dim]")
                input("\nPress Enter to continue...")

    def show_ai_model_selection(self):
        """Show AI model selection interface"""
        while True:
            console.clear()
            console.print(Panel(
                f"🤖 AI Model Selection\n\nCurrent Model: {self.config['ai']['current_model']}",
                title="🧠 AION AI Models",
                border_style="cyan"
            ))

            # Show available providers
            providers_table = Table(show_header=True, header_style="bold magenta")
            providers_table.add_column("🔢", style="cyan", width=6)
            providers_table.add_column("Provider", style="white", width=20)
            providers_table.add_column("Description", style="dim white", width=30)

            provider_list = list(self.config['ai']['providers'].keys())
            for i, provider_key in enumerate(provider_list, 1):
                provider = self.config['ai']['providers'][provider_key]
                providers_table.add_row(str(i), provider['name'], f"Models: {len(provider['models'])}")

            providers_table.add_row("0", "🔙 Back", "Back to settings")

            console.print(Panel(providers_table, title="🏢 AI Providers", border_style="blue"))

            choice = Prompt.ask(
                f"Select provider [0-{len(provider_list)}]",
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
                f"🤖 {provider['name']} Models\n\nCurrent Model: {self.config['ai']['current_model']}",
                title=f"🧠 {provider['name']}",
                border_style="cyan"
            ))

            # Show available models
            models_table = Table(show_header=True, header_style="bold magenta")
            models_table.add_column("🔢", style="cyan", width=6)
            models_table.add_column("Model", style="white", width=20)
            models_table.add_column("Description", style="dim white", width=30)
            models_table.add_column("Cost", style="yellow", width=10)

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

            models_table.add_row("0", "🔙 Back", "Back to provider selection", "")

            console.print(Panel(models_table, title=f"🤖 {provider['name']} Models", border_style="green"))

            choice = Prompt.ask(
                f"Select model [0-{len(model_list)}]",
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

            console.print(f"\n✅ [green]Model changed successfully![/green]")
            console.print(f"🤖 New Model: {model_info['name']}")
            console.print(f"📝 Description: {model_info['description']}")
            console.print(f"💰 Cost: {model_info['cost']}")
            console.print(f"🔢 Max Tokens: {model_info['max_tokens']}")

            input("\nPress Enter to continue...")

        except Exception as e:
            console.print(f"\n❌ [red]Error changing model: {str(e)}[/red]")
            input("\nPress Enter to continue...")

@app.command()
def start():
    """🚀 Start AION interactive mode"""
    import asyncio
    aion_app = AIONApp()
    asyncio.run(aion_app.run())

@app.command()
def ai():
    """🤖 Quick AI assistant"""
    console.print("\n[yellow]🤖 Starting AI assistant...[/yellow]")
    console.print("[dim]⚠️ This feature is under development[/dim]")

@app.command()
def version():
    """📋 Show version information"""
    console.print("[bold blue]🧠 AION v2.0.0[/bold blue]")
    console.print("[green]AI Operating Node - Enhanced Terminal Assistant[/green]")

if __name__ == "__main__":
    app()
