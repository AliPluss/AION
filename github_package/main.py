#!/usr/bin/env python3
"""
🤖 AION - AI Operating Node
Terminal-based AI Assistant with Multilingual Support

Author: AION Development Team
Version: 1.0.0
"""

import typer
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.translator import Translator
from interfaces.cli import CLI
from interfaces.tui import TUI
from interfaces.web import WebInterface
from core.security import SecurityManager

# Initialize console and translator
console = Console()
translator = Translator()

app = typer.Typer(
    name="aion",
    help="🤖 AION - AI Operating Node Terminal Assistant",
    rich_markup_mode="rich"
)

def display_welcome():
    """Display welcome screen with language selection"""
    
    # ASCII Art for AION
    aion_art = """
    ╔═══════════════════════════════════════╗
    ║     █████╗ ██╗ ██████╗ ███╗   ██╗    ║
    ║    ██╔══██╗██║██╔═══██╗████╗  ██║    ║
    ║    ███████║██║██║   ██║██╔██╗ ██║    ║
    ║    ██╔══██║██║██║   ██║██║╚██╗██║    ║
    ║    ██║  ██║██║╚██████╔╝██║ ╚████║    ║
    ║    ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝    ║
    ║                                       ║
    ║    AI Operating Node - Terminal       ║
    ╚═══════════════════════════════════════╝
    """
    
    console.print(Panel(
        Align.center(Text(aion_art, style="bold cyan")),
        title="🤖 Welcome to AION",
        border_style="bright_blue"
    ))

def select_language():
    """Language selection interface"""
    languages = {
        "1": ("en", "English 🇬🇧"),
        "2": ("ar", "العربية 🇸🇦"),
        "3": ("no", "Norsk 🇳🇴"),
        "4": ("de", "Deutsch 🇩🇪"),
        "5": ("fr", "Français 🇫🇷"),
        "6": ("zh", "中文 🇨🇳"),
        "7": ("es", "Español 🇪🇸")
    }
    
    console.print("\n🌐 Choose your language / اختر لغتك:")
    for key, (code, name) in languages.items():
        console.print(f"[{key}] {name}")
    
    while True:
        choice = typer.prompt("\nEnter your choice (1-7)")
        if choice in languages:
            lang_code, lang_name = languages[choice]
            translator.set_language(lang_code)
            console.print(f"✅ Language set to: {lang_name}")
            return lang_code
        else:
            console.print("❌ Invalid choice. Please select 1-7.")

def show_main_menu():
    """Display main menu with current language"""
    menu_items = [
        ("1", "🧠", translator.get("menu_ai_assistant")),
        ("2", "💻", translator.get("menu_system_commands")),
        ("3", "📜", translator.get("menu_execute_code")),
        ("4", "🧩", translator.get("menu_plugins")),
        ("5", "🌐", translator.get("menu_web_interface")),
        ("6", "⚙️", translator.get("menu_settings")),
        ("7", "🌍", translator.get("menu_change_language")),
        ("8", "❓", translator.get("menu_help")),
        ("9", "🚪", translator.get("menu_exit"))
    ]
    
    console.print(f"\n{translator.get('main_menu_title')}")
    console.print("=" * 50)
    
    for num, emoji, text in menu_items:
        console.print(f"[{num}] {emoji} {text}")

@app.command()
def start():
    """🚀 Start AION Terminal Assistant"""
    try:
        # Initialize security
        security = SecurityManager()
        
        # Display welcome screen
        display_welcome()
        
        # Check if language is already set
        if not translator.current_language:
            select_language()
        
        # Initialize CLI interface
        cli = CLI(translator, security)
        
        # Main application loop
        while True:
            show_main_menu()
            
            choice = typer.prompt(f"\n{translator.get('enter_choice')}")
            
            if choice == "1":
                # AI Assistant
                cli.ai_assistant_mode()
            elif choice == "2":
                # System Commands
                cli.system_commands_mode()
            elif choice == "3":
                # Execute Code
                cli.execute_code_mode()
            elif choice == "4":
                # Plugins
                cli.plugins_mode()
            elif choice == "5":
                # Web Interface
                web = WebInterface(translator)
                web.start()
            elif choice == "6":
                # Settings
                cli.settings_mode()
            elif choice == "7":
                # Change Language
                select_language()
            elif choice == "8":
                # Help
                cli.show_help()
            elif choice == "9":
                # Exit
                console.print(f"👋 {translator.get('goodbye_message')}")
                break
            else:
                console.print(f"❌ {translator.get('invalid_choice')}")
                
    except KeyboardInterrupt:
        console.print(f"\n👋 {translator.get('goodbye_message')}")
    except Exception as e:
        console.print(f"❌ Error: {str(e)}")

@app.command()
def tui():
    """🎨 Start AION in Text User Interface mode"""
    try:
        tui_interface = TUI(translator)
        tui_interface.run()
    except Exception as e:
        console.print(f"❌ TUI Error: {str(e)}")

@app.command()
def web(
    host: str = typer.Option("127.0.0.1", help="Host to bind to"),
    port: int = typer.Option(8000, help="Port to bind to")
):
    """🌐 Start AION Web Interface"""
    try:
        web_interface = WebInterface(translator)
        web_interface.start(host=host, port=port)
    except Exception as e:
        console.print(f"❌ Web Interface Error: {str(e)}")

@app.command()
def version():
    """📋 Show AION version information"""
    version_info = """
    🤖 AION - AI Operating Node
    Version: 1.0.0
    Python: 3.10+
    
    Supported Languages:
    • العربية (Arabic) 🇸🇦
    • English 🇬🇧  
    • Norsk (Norwegian) 🇳🇴
    • Deutsch (German) 🇩🇪
    • Français (French) 🇫🇷
    • 中文 (Chinese) 🇨🇳
    • Español (Spanish) 🇪🇸
    """
    console.print(Panel(version_info, title="Version Info", border_style="green"))

if __name__ == "__main__":
    app()
