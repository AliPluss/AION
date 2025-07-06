#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 AION - AI Operating Node Setup Script (Fixed Version)
Enhanced Terminal Assistant Setup
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()

def main():
    """Main setup function"""
    console.print(Panel.fit(
        "[bold blue]🧠 AION - AI Operating Node[/bold blue]\n"
        "[green]Enhanced Setup Script[/green]\n"
        "[yellow]Setting up your AI assistant...[/yellow]",
        title="🚀 AION Setup"
    ))
    
    try:
        # Create project structure
        create_project_structure()
        
        # Install dependencies
        install_dependencies()
        
        # Create configuration files
        create_config_files()

        # Create plugin system
        create_plugin_system()

        # Create sample plugins
        create_sample_plugins()

        # Create main application file
        create_main_app()
        
        # Success message
        show_success_message()
        
    except Exception as e:
        console.print(f"[red]❌ Setup failed: {e}[/red]")
        sys.exit(1)

def create_project_structure():
    """Create the project directory structure"""
    console.print("[cyan]📁 Creating project structure...[/cyan]")
    
    directories = [
        "aion_project",
        "aion_project/src",
        "aion_project/src/ai",
        "aion_project/src/plugins",
        "aion_project/src/utils",
        "aion_project/config",
        "aion_project/data",
        "aion_project/logs",
        "aion_project/exports"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        console.print(f"  ✅ Created: {directory}")

def install_dependencies():
    """Install required Python packages"""
    console.print("[cyan]📦 Installing dependencies...[/cyan]")
    
    # Core dependencies
    core_packages = [
        "rich>=13.0.0",
        "typer>=0.9.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "textual>=0.40.0",
        "openai>=1.0.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "aiofiles>=23.0.0"
    ]
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Installing packages...", total=len(core_packages))
        
        for package in core_packages:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                             check=True, capture_output=True)
                progress.advance(task)
                console.print(f"  ✅ Installed: {package}")
            except subprocess.CalledProcessError as e:
                console.print(f"  ⚠️ Failed to install {package}: {e}")

def create_config_files():
    """Create configuration files"""
    console.print("[cyan]⚙️ Creating configuration files...[/cyan]")
    
    # Main config
    config = {
        "app": {
            "name": "AION",
            "version": "2.0.0",
            "language": "ar",
            "theme": "dark"
        },
        "ai": {
            "default_provider": "openai",
            "providers": {
                "openai": {
                    "api_key": "",
                    "model": "gpt-3.5-turbo",
                    "max_tokens": 1000
                }
            }
        },
        "features": {
            "voice_enabled": True,
            "web_interface": True,
            "plugins_enabled": True,
            "export_enabled": True
        }
    }
    
    with open("aion_project/config/config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    # Language files
    languages = {
        "ar": {
            "welcome": "مرحباً بك في AION",
            "ai_assistant": "مساعد الذكاء الاصطناعي",
            "code_execution": "تنفيذ الكود",
            "plugin_manager": "مدير الإضافات",
            "voice_mode": "الوضع الصوتي",
            "settings": "الإعدادات",
            "help": "المساعدة",
            "exit": "خروج"
        },
        "en": {
            "welcome": "Welcome to AION",
            "ai_assistant": "AI Assistant",
            "code_execution": "Code Execution",
            "plugin_manager": "Plugin Manager",
            "voice_mode": "Voice Mode",
            "settings": "Settings",
            "help": "Help",
            "exit": "Exit"
        }
    }
    
    for lang, translations in languages.items():
        with open(f"aion_project/config/lang_{lang}.json", "w", encoding="utf-8") as f:
            json.dump(translations, f, indent=2, ensure_ascii=False)
    
    console.print("  ✅ Configuration files created")

def create_plugin_system():
    """Create the plugin system"""
    console.print("[cyan]🧩 Creating plugin system...[/cyan]")

    # Create base plugin class
    base_plugin_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧩 AION Plugin System - Base Plugin Class
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import json
import os

class BasePlugin(ABC):
    """Base class for all AION plugins"""

    def __init__(self):
        self.name = "Unknown Plugin"
        self.version = "1.0.0"
        self.description = "A plugin for AION"
        self.author = "Unknown"
        self.enabled = True
        self.config = {}

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the plugin"""
        pass

    @abstractmethod
    def execute(self, command: str, args: List[str]) -> Dict[str, Any]:
        """Execute plugin command"""
        pass

    @abstractmethod
    def get_commands(self) -> List[str]:
        """Get list of available commands"""
        pass

    def get_info(self) -> Dict[str, Any]:
        """Get plugin information"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "enabled": self.enabled,
            "commands": self.get_commands()
        }

    def load_config(self, config_path: str) -> bool:
        """Load plugin configuration"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading config: {e}")
            return False

    def save_config(self, config_path: str) -> bool:
        """Save plugin configuration"""
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
'''

    with open("aion_project/src/plugins/base_plugin.py", "w", encoding="utf-8") as f:
        f.write(base_plugin_content)

    # Create plugin manager
    plugin_manager_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧩 AION Plugin Manager
"""

import os
import sys
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class PluginManager:
    """Manages AION plugins"""

    def __init__(self, plugins_dir: str = "src/plugins"):
        self.plugins_dir = Path(plugins_dir)
        self.loaded_plugins: Dict[str, Any] = {}
        self.plugin_configs: Dict[str, Dict] = {}

    def discover_plugins(self) -> List[str]:
        """Discover available plugins"""
        plugins = []
        if not self.plugins_dir.exists():
            return plugins

        for file_path in self.plugins_dir.glob("*.py"):
            if file_path.name not in ["__init__.py", "base_plugin.py"]:
                plugins.append(file_path.stem)
        return plugins

    def load_plugin(self, plugin_name: str) -> bool:
        """Load a specific plugin"""
        try:
            plugin_path = self.plugins_dir / f"{plugin_name}.py"
            if not plugin_path.exists():
                console.print(f"[red]❌ Plugin {plugin_name} not found[/red]")
                return False

            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find plugin class
            plugin_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and
                    hasattr(attr, 'initialize') and
                    attr_name != 'BasePlugin'):
                    plugin_class = attr
                    break

            if plugin_class:
                plugin_instance = plugin_class()
                if plugin_instance.initialize():
                    self.loaded_plugins[plugin_name] = plugin_instance
                    console.print(f"[green]✅ Plugin {plugin_name} loaded successfully[/green]")
                    return True

            console.print(f"[red]❌ Failed to initialize plugin {plugin_name}[/red]")
            return False

        except Exception as e:
            console.print(f"[red]❌ Error loading plugin {plugin_name}: {e}[/red]")
            return False

    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a specific plugin"""
        if plugin_name in self.loaded_plugins:
            del self.loaded_plugins[plugin_name]
            console.print(f"[yellow]🔄 Plugin {plugin_name} unloaded[/yellow]")
            return True
        return False

    def load_all_plugins(self) -> int:
        """Load all available plugins"""
        plugins = self.discover_plugins()
        loaded_count = 0

        for plugin_name in plugins:
            if self.load_plugin(plugin_name):
                loaded_count += 1

        return loaded_count

    def execute_plugin_command(self, plugin_name: str, command: str, args: List[str]) -> Optional[Dict[str, Any]]:
        """Execute a command from a specific plugin"""
        if plugin_name not in self.loaded_plugins:
            console.print(f"[red]❌ Plugin {plugin_name} not loaded[/red]")
            return None

        try:
            return self.loaded_plugins[plugin_name].execute(command, args)
        except Exception as e:
            console.print(f"[red]❌ Error executing command: {e}[/red]")
            return None

    def list_plugins(self) -> None:
        """Display list of available and loaded plugins"""
        table = Table(title="🧩 AION Plugins")
        table.add_column("Plugin Name", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Version", style="yellow")
        table.add_column("Description", style="white")

        all_plugins = self.discover_plugins()

        for plugin_name in all_plugins:
            if plugin_name in self.loaded_plugins:
                plugin = self.loaded_plugins[plugin_name]
                info = plugin.get_info()
                table.add_row(
                    info["name"],
                    "✅ Loaded",
                    info["version"],
                    info["description"]
                )
            else:
                table.add_row(
                    plugin_name,
                    "❌ Not Loaded",
                    "Unknown",
                    "Plugin not loaded"
                )

        console.print(table)

    def get_plugin_commands(self, plugin_name: str) -> List[str]:
        """Get available commands for a plugin"""
        if plugin_name in self.loaded_plugins:
            return self.loaded_plugins[plugin_name].get_commands()
        return []

    def get_all_commands(self) -> Dict[str, List[str]]:
        """Get all available commands from all loaded plugins"""
        commands = {}
        for plugin_name, plugin in self.loaded_plugins.items():
            commands[plugin_name] = plugin.get_commands()
        return commands
'''

    with open("aion_project/src/plugins/plugin_manager.py", "w", encoding="utf-8") as f:
        f.write(plugin_manager_content)

    console.print("  ✅ Plugin system created")

def create_sample_plugins():
    """Create sample plugins"""
    console.print("[cyan]🔌 Creating sample plugins...[/cyan]")

    # Calculator plugin
    calculator_plugin = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧮 Calculator Plugin for AION
"""

from src.plugins.base_plugin import BasePlugin
from typing import Dict, List, Any
import math

class CalculatorPlugin(BasePlugin):
    """Simple calculator plugin"""

    def __init__(self):
        super().__init__()
        self.name = "Calculator"
        self.version = "1.0.0"
        self.description = "Simple calculator with basic math operations"
        self.author = "AION Team"

    def initialize(self) -> bool:
        """Initialize calculator plugin"""
        return True

    def execute(self, command: str, args: List[str]) -> Dict[str, Any]:
        """Execute calculator command"""
        try:
            if command == "add" and len(args) >= 2:
                result = sum(float(arg) for arg in args)
                return {"success": True, "result": result, "operation": "addition"}

            elif command == "subtract" and len(args) == 2:
                result = float(args[0]) - float(args[1])
                return {"success": True, "result": result, "operation": "subtraction"}

            elif command == "multiply" and len(args) >= 2:
                result = 1
                for arg in args:
                    result *= float(arg)
                return {"success": True, "result": result, "operation": "multiplication"}

            elif command == "divide" and len(args) == 2:
                if float(args[1]) == 0:
                    return {"success": False, "error": "Division by zero"}
                result = float(args[0]) / float(args[1])
                return {"success": True, "result": result, "operation": "division"}

            elif command == "sqrt" and len(args) == 1:
                result = math.sqrt(float(args[0]))
                return {"success": True, "result": result, "operation": "square root"}

            elif command == "power" and len(args) == 2:
                result = float(args[0]) ** float(args[1])
                return {"success": True, "result": result, "operation": "power"}

            else:
                return {"success": False, "error": "Invalid command or arguments"}

        except ValueError:
            return {"success": False, "error": "Invalid number format"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_commands(self) -> List[str]:
        """Get available calculator commands"""
        return ["add", "subtract", "multiply", "divide", "sqrt", "power"]
'''

    with open("aion_project/src/plugins/calculator_plugin.py", "w", encoding="utf-8") as f:
        f.write(calculator_plugin)

    console.print("  ✅ Sample plugins created")

def create_main_app():
    """Create the main application file"""
    console.print("[cyan]🚀 Creating main application...[/cyan]")
    
    main_app_content = '''#!/usr/bin/env python3
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
    
    def run(self):
        """Run the main application"""
        self.show_welcome()
        
        while True:
            console.print()
            self.show_menu()
            
            choice = Prompt.ask(
                "\\n[cyan]اختر رقم الوظيفة | Select function number[/cyan]",
                choices=["0", "1", "2", "3", "4", "5", "6"],
                default="1"
            )

            if choice == "0":
                console.print("\\n[green]🙏 شكراً لاستخدام AION! | Thank you for using AION![/green]")
                break
            elif choice == "1":
                console.print("\\n[yellow]🤖 بدء مساعد الذكاء الاصطناعي...[/yellow]")
                console.print("[dim]⚠️ هذه الميزة قيد التطوير | This feature is under development[/dim]")
            elif choice == "2":
                console.print("\\n[yellow]⚡ بدء تنفيذ الكود...[/yellow]")
                console.print("[dim]⚠️ هذه الميزة قيد التطوير | This feature is under development[/dim]")
            elif choice == "3":
                self.show_plugin_manager()
            elif choice == "4":
                console.print("\\n[yellow]🎤 بدء الوضع الصوتي...[/yellow]")
                console.print("[dim]⚠️ هذه الميزة قيد التطوير | This feature is under development[/dim]")
            elif choice == "5":
                console.print("\\n[yellow]⚙️ فتح الإعدادات...[/yellow]")
                console.print("[dim]⚠️ هذه الميزة قيد التطوير | This feature is under development[/dim]")
            elif choice == "6":
                self.show_help()

    def show_plugin_manager(self):
        """Show plugin manager interface"""
        try:
            # Import plugin manager
            sys.path.append(str(Path("src/plugins")))
            from plugin_manager import PluginManager

            plugin_manager = PluginManager()

            while True:
                console.print("\\n[bold blue]🧩 مدير الإضافات | Plugin Manager[/bold blue]")

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
                    "\\n[cyan]اختر رقم الوظيفة | Select function number[/cyan]",
                    choices=["0", "1", "2", "3", "4"],
                    default="1"
                )

                if plugin_choice == "0":
                    break
                elif plugin_choice == "1":
                    console.print("\\n[yellow]📋 عرض الإضافات المتاحة...[/yellow]")
                    plugin_manager.list_plugins()
                elif plugin_choice == "2":
                    console.print("\\n[yellow]🔄 تحميل الإضافات...[/yellow]")
                    loaded_count = plugin_manager.load_all_plugins()
                    console.print(f"[green]✅ تم تحميل {loaded_count} إضافة بنجاح[/green]")
                elif plugin_choice == "3":
                    self.demo_calculator_plugin(plugin_manager)
                elif plugin_choice == "4":
                    console.print("\\n[yellow]📊 أوامر الإضافات المتاحة...[/yellow]")
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
        console.print("\\n[bold blue]🧮 تجربة إضافة الآلة الحاسبة | Calculator Plugin Demo[/bold blue]")

        # Load calculator plugin if not loaded
        if "calculator_plugin" not in plugin_manager.loaded_plugins:
            if not plugin_manager.load_plugin("calculator_plugin"):
                console.print("[red]❌ فشل في تحميل إضافة الآلة الحاسبة[/red]")
                return

        while True:
            console.print("\\n[green]أمثلة على العمليات الحسابية:[/green]")
            console.print("• add 5 3 2 (الجمع)")
            console.print("• subtract 10 3 (الطرح)")
            console.print("• multiply 4 5 (الضرب)")
            console.print("• divide 15 3 (القسمة)")
            console.print("• sqrt 16 (الجذر التربيعي)")
            console.print("• power 2 3 (الأس)")
            console.print("• exit (للخروج)")

            user_input = Prompt.ask("\\n[cyan]أدخل العملية | Enter operation[/cyan]")

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

@app.command()
def start():
    """🚀 Start AION interactive mode"""
    aion_app = AIONApp()
    aion_app.run()

@app.command()
def ai():
    """🤖 Quick AI assistant"""
    console.print("\\n[yellow]🤖 بدء مساعد الذكاء الاصطناعي...[/yellow]")
    console.print("[dim]⚠️ هذه الميزة قيد التطوير | This feature is under development[/dim]")

@app.command()
def version():
    """📋 Show version information"""
    console.print("[bold blue]🧠 AION v2.0.0[/bold blue]")
    console.print("[green]AI Operating Node - Enhanced Terminal Assistant[/green]")

if __name__ == "__main__":
    app()
'''
    
    with open("aion_project/main.py", "w", encoding="utf-8") as f:
        f.write(main_app_content)
    
    console.print("  ✅ Main application created")

def show_success_message():
    """Show setup completion message"""
    success_table = Table(show_header=True, header_style="bold green")
    success_table.add_column("✅", style="green", width=4)
    success_table.add_column("المكون | Component", style="cyan", width=25)
    success_table.add_column("الحالة | Status", style="green", width=15)
    
    components = [
        ("✅", "Project Structure", "تم إنشاؤه | Created"),
        ("✅", "Dependencies", "تم تثبيتها | Installed"),
        ("✅", "Configuration", "تم إعدادها | Configured"),
        ("✅", "Main Application", "جاهز | Ready"),
        ("✅", "Arabic Support", "مفعل | Enabled")
    ]
    
    for icon, component, status in components:
        success_table.add_row(icon, component, status)
    
    success_panel = Panel(
        success_table,
        title="[bold green]🎉 تم الإعداد بنجاح | Setup Completed Successfully[/bold green]",
        border_style="bright_green"
    )
    
    console.print("\n")
    console.print(success_panel)
    
    # Usage instructions
    usage_text = """
[bold cyan]🚀 كيفية الاستخدام | How to Use:[/bold cyan]

[yellow]1. انتقل إلى مجلد المشروع | Navigate to project folder:[/yellow]
   cd aion_project

[yellow]2. تشغيل النظام التفاعلي | Run interactive system:[/yellow]
   python main.py start

[yellow]3. الأوامر السريعة | Quick commands:[/yellow]
   python main.py ai       # مساعد AI مباشرة
   python main.py version  # معلومات الإصدار
   python main.py --help   # المساعدة
    """
    
    usage_panel = Panel(
        usage_text.strip(),
        title="[bold blue]📖 دليل الاستخدام | Usage Guide[/bold blue]",
        border_style="blue"
    )
    
    console.print(usage_panel)

if __name__ == "__main__":
    main()
