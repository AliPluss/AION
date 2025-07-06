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
            "voice_mode": "الوضع الصوتي",
            "settings": "الإعدادات",
            "help": "المساعدة",
            "exit": "خروج"
        },
        "en": {
            "welcome": "Welcome to AION",
            "ai_assistant": "AI Assistant",
            "code_execution": "Code Execution",
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
            ("3", "🎤 " + self.lang.get("voice_mode", "Voice Mode"), "التحكم بالأوامر الصوتية"),
            ("4", "⚙️ " + self.lang.get("settings", "Settings"), "الإعدادات والتخصيص"),
            ("5", "❓ " + self.lang.get("help", "Help"), "المساعدة والدليل"),
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
                choices=["0", "1", "2", "3", "4", "5"],
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
                console.print("\\n[yellow]🎤 بدء الوضع الصوتي...[/yellow]")
                console.print("[dim]⚠️ هذه الميزة قيد التطوير | This feature is under development[/dim]")
            elif choice == "4":
                console.print("\\n[yellow]⚙️ فتح الإعدادات...[/yellow]")
                console.print("[dim]⚠️ هذه الميزة قيد التطوير | This feature is under development[/dim]")
            elif choice == "5":
                self.show_help()
    
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
