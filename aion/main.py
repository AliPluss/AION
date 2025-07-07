#!/usr/bin/env python3
"""
🤖 AION - AI Operating Node
Terminal-based AI Assistant with Multilingual Support

Author: AION Development Team
Version: 2.0.0
"""

import typer
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

# Add project root to Python path for development
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    # Try relative imports first (package mode)
    from .utils.translator import Translator
    from .interfaces.cli import CLI
    from .interfaces.tui import TUI
    from .interfaces.web import WebInterface
    from .core.security import SecurityManager
except ImportError:
    # Fallback to absolute imports (development mode)
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

def show_animated_loading():
    """
    Display animated loading screen with AION branding
    Shows professional startup sequence with progress indicators
    """

    # AION ASCII Art Banner
    banner = """
    ╔═══════════════════════════════════════╗
    ║              🤖 AION                  ║
    ║        AI Operating Node              ║
    ║     Professional Terminal AI          ║
    ║                                       ║
    ║    Developer: project.django.rst@gmail.com    ║
    ║    GitHub: https://github.com/AliPluss/aion-ai ║
    ╚═══════════════════════════════════════╝
    """

    console.print(Panel(
        Align.center(Text(banner, style="bold cyan")),
        title="[bold green]AION Loading[/bold green]",
        border_style="bright_blue"
    ))

    # Animated loading sequence
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        steps = [
            "🔧 Initializing AION systems...",
            "🔐 Loading security modules...",
            "🤖 Connecting AI providers...",
            "🌐 Setting up multilingual support...",
            "⚡ Preparing code execution engine...",
            "📁 Loading file management system...",
            "🎤 Initializing voice control...",
            "📤 Setting up export capabilities...",
            "✅ AION ready!"
        ]

        task = progress.add_task("Loading...", total=len(steps))

        for step in steps:
            progress.update(task, description=step)
            time.sleep(0.6)  # Smooth animation timing
            progress.advance(task)

        time.sleep(1)  # Final pause before continuing

def display_welcome():
    """
    Display welcome screen with language selection
    Shows AION branding and available interface options

    This function presents the main entry point for users, displaying:
    - AION ASCII art logo
    - Available interface modes (CLI, TUI, Web)
    - Language selection options
    - System status information
    """
    
    # AION ASCII Art
    logo = """
    ╔═══════════════════════════════════════╗
    ║              🤖 AION                  ║
    ║        AI Operating Node              ║
    ║                                       ║
    ║    Professional AI Assistant          ║
    ║    with Multilingual Support          ║
    ╚═══════════════════════════════════════╝
    """
    
    console.print(Panel(
        Align.center(Text(logo, style="bold cyan")),
        title="[bold green]Welcome to AION[/bold green]",
        border_style="bright_blue"
    ))
    
    # Language selection
    lang_code = select_language()
    translator.set_language(lang_code)
    
    return lang_code

def select_language():
    """Language selection interface with command-driven selection - English as default"""
    languages = {
        "en": ("en", "English 🇬🇧"),
        "no": ("no", "Norsk 🇳🇴"),
        "de": ("de", "Deutsch 🇩🇪"),
        "fr": ("fr", "Français 🇫🇷"),
        "zh": ("zh", "中文 🇨🇳"),
        "es": ("es", "Español 🇪🇸"),
        "ar": ("ar", "العربية 🇸🇦")
    }

    console.print("\n🌐 [bold cyan]Language Selection[/bold cyan]")
    console.print("🇬🇧 [bold green]Default: English[/bold green] (press Enter to continue)")
    console.print("\nOther available languages:")
    for code, (_, name) in list(languages.items())[1:]:  # Skip English as it's shown as default
        console.print(f"   • [bold green]{code}[/bold green] - {name}")

    console.print("\n💡 Type language code or press Enter for English:")

    while True:
        choice = input("🌐 Language> ").strip().lower()

        if choice == "":
            # Default to English
            lang_code, lang_name = languages["en"]
            translator.set_language(lang_code)
            console.print(f"✅ Language set to: {lang_name}")
            return lang_code
        elif choice in languages:
            lang_code, lang_name = languages[choice]
            translator.set_language(lang_code)
            console.print(f"✅ Language set to: {lang_name}")
            return lang_code
        else:
            console.print(f"❌ Invalid language code: '{choice}'")
            console.print("💡 Available codes: " + ", ".join(languages.keys()))

def show_main_menu():
    """
    Display main menu with command-driven interface (no numeric options)

    Shows available interface options and system information:
    - CLI mode for command-line interaction
    - TUI mode for terminal user interface
    - Web mode for browser-based interface
    - System status and configuration options
    """
    console.print("\n" + "="*60)
    console.print("🚀 AION Main Menu - Command Interface")
    console.print("="*60)
    console.print("💬 [bold cyan]cli[/bold cyan] - Command Line Interface")
    console.print("🖥️  [bold cyan]tui[/bold cyan] - Terminal User Interface")
    console.print("🌐 [bold cyan]web[/bold cyan] - Browser Interface")
    console.print("⚙️  [bold cyan]settings[/bold cyan] - Configuration")
    console.print("🌍 [bold cyan]language[/bold cyan] - Change Language")
    console.print("❓ [bold cyan]help[/bold cyan] - Show Help")
    console.print("🚪 [bold cyan]exit[/bold cyan] - Exit AION")
    console.print("="*60)
    console.print("💡 Type a command and press Enter (e.g., 'cli' or 'tui')")

@app.command()
def start(
    interface: str = typer.Option("cli", help="Interface type: cli, tui, or web"),
    language: str = typer.Option("en", help="Language code (en, ar, fr, de, es, zh, no) - Default: English"),
    dev_mode: bool = typer.Option(False, help="Enable development mode")
):
    """
    Start AION with specified interface and language
    
    This is the main entry point for AION, providing:
    - Interface selection (CLI, TUI, Web)
    - Language configuration
    - Development mode for testing
    - Security initialization
    - System health checks
    """
    try:
        # Show animated loading screen first
        if not dev_mode:
            show_animated_loading()

        # Display welcome screen
        if not dev_mode:
            selected_lang = display_welcome()
            if selected_lang:
                language = selected_lang
        
        # Initialize security manager
        security = SecurityManager()
        
        # Set language
        translator.set_language(language)
        
        # Start selected interface
        if interface.lower() == "cli":
            cli = CLI(translator, security)
            cli.start()
        elif interface.lower() == "tui":
            tui = TUI(translator, security)
            tui.start()
        elif interface.lower() == "web":
            web = WebInterface(translator, security)
            web.start()
        else:
            console.print(f"❌ Unknown interface: {interface}")
            console.print("Available interfaces: cli, tui, web")
            
    except KeyboardInterrupt:
        console.print("\n👋 Goodbye! Thanks for using AION!")
    except Exception as e:
        console.print(f"❌ Error starting AION: {e}")
        if dev_mode:
            raise

@app.command()
def version():
    """Show AION version information"""
    console.print("🤖 AION - AI Operating Node")
    console.print("Version: 2.0.0")
    console.print("Author: AION Development Team")
    console.print("License: MIT")

@app.command()
def config():
    """Show configuration information"""
    console.print("⚙️ AION Configuration")
    console.print(f"Current Language: {translator.current_language}")
    console.print(f"Supported Languages: {list(translator.supported_languages.keys())}")

if __name__ == "__main__":
    app()
