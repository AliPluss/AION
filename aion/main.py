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
    """Pure arrow-key language selection interface - English as default"""
    try:
        # Try pure arrow navigation first
        from aion.interfaces.arrow_navigation import select_language_arrows
        lang_code = select_language_arrows()
        translator.set_language(lang_code)
        return lang_code
    except ImportError:
        # Fallback to numbered selection if arrow navigation fails
        from rich.prompt import IntPrompt

        languages = [
            ("en", "English 🇬🇧", "🧠 Pulse"),
            ("ar", "العربية 🇮🇶", "🇮🇶 Bounce RTL"),
            ("no", "Norsk 🇳🇴", "✨ Glow"),
            ("de", "Deutsch 🇩🇪", "🌊 Wave"),
            ("fr", "Français 🇫🇷", "💫 Sparkle"),
            ("zh", "中文 🇨🇳", "🎭 Fade"),
            ("es", "Español 🇪🇸", "⚡ Flash")
        ]

        console.print("\n🌐 [bold cyan]Language Selection[/bold cyan]")
        console.print("🎮 [bold yellow]Select 1-7, or press Enter for English default[/bold yellow]\n")

        for i, (code, name, animation) in enumerate(languages, 1):
            status = "🔥 Default" if code == "en" else "✅ Available"
            console.print(f"  {i}. {name} [dim]{animation}[/dim] {status}")

        try:
            choice = IntPrompt.ask(
                "🌐 Language",
                default=1,
                choices=[str(i) for i in range(1, len(languages) + 1)],
                show_default=True
            )

            lang_code, lang_name, animation = languages[choice - 1]
            translator.set_language(lang_code)
            console.print(f"\n✅ Selected: [bold green]{lang_name}[/bold green] ({animation})")
            return lang_code

        except (KeyboardInterrupt, EOFError):
            # Default to English
            translator.set_language("en")
            console.print("\n🇬🇧 ✅ Defaulting to English")
            return "en"

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
    console.print(f"Available Interfaces: CLI, TUI, Web")
    console.print(f"Security Level: Enhanced")

@app.command()
def install_plugin(
    source: str = typer.Argument(..., help="Plugin source (GitHub repo, PyPI package, or local path)"),
    source_type: str = typer.Option("auto", help="Source type: github, pypi, local, or auto")
):
    """Install a plugin from various sources"""
    try:
        from .core.plugin_installer import install_plugin_command
        console.print(f"🧩 Installing plugin from: {source}")
        success = install_plugin_command(source, source_type)
        if success:
            console.print("✅ Plugin installed successfully!")
        else:
            console.print("❌ Plugin installation failed")
    except ImportError:
        console.print("❌ Plugin installer not available")

@app.command()
def remove_plugin(
    plugin_name: str = typer.Argument(..., help="Name of the plugin to remove")
):
    """Remove an installed plugin"""
    try:
        from .core.plugin_installer import plugin_installer
        console.print(f"🗑️ Removing plugin: {plugin_name}")
        success = plugin_installer.uninstall_plugin(plugin_name)
        if success:
            console.print("✅ Plugin removed successfully!")
        else:
            console.print("❌ Plugin removal failed")
    except ImportError:
        console.print("❌ Plugin installer not available")

@app.command()
def list_plugins():
    """List all installed plugins"""
    try:
        from .core.plugin_installer import plugin_installer
        plugins = plugin_installer.list_installed_plugins()
        if plugins:
            console.print("🧩 Installed Plugins:")
            for plugin in plugins:
                console.print(f"  • {plugin.name} v{plugin.version} - {plugin.description}")
        else:
            console.print("📦 No plugins installed")
    except ImportError:
        console.print("❌ Plugin installer not available")

@app.command()
def update_plugin(
    plugin_name: str = typer.Argument(..., help="Name of the plugin to update")
):
    """Update an installed plugin"""
    try:
        from .core.plugin_installer import plugin_installer
        console.print(f"🔄 Updating plugin: {plugin_name}")
        success = plugin_installer.update_plugin(plugin_name)
        if success:
            console.print("✅ Plugin updated successfully!")
        else:
            console.print("❌ Plugin update failed")
    except ImportError:
        console.print("❌ Plugin installer not available")

@app.command()
def stats():
    """Show real-time system statistics"""
    try:
        from .core.stats_monitor import stats_monitor, format_bytes, format_duration
        console.print("📊 AION System Statistics")
        console.print("=" * 40)

        # Start monitoring if not already started
        stats_monitor.start_monitoring()

        # Get current stats
        current_stats = stats_monitor.get_current_system_stats()
        session_stats = stats_monitor.get_session_summary()

        if current_stats:
            console.print(f"🔥 CPU Usage: {current_stats.cpu_percent:.1f}%")
            console.print(f"🧠 Memory: {current_stats.memory_percent:.1f}% ({format_bytes(current_stats.memory_used)}/{format_bytes(current_stats.memory_total)})")
            console.print(f"💾 Disk: {current_stats.disk_percent:.1f}% ({format_bytes(current_stats.disk_used)}/{format_bytes(current_stats.disk_total)})")
            console.print(f"🌐 Network: ↑{format_bytes(current_stats.network_sent)} ↓{format_bytes(current_stats.network_recv)}")

        console.print("\n📈 Session Statistics:")
        console.print(f"⏱️ Uptime: {format_duration(session_stats.uptime.total_seconds())}")
        console.print(f"⌨️ Commands: {session_stats.commands_executed}")
        console.print(f"📝 Files Edited: {session_stats.files_edited}")
        console.print(f"🧩 Plugins Used: {session_stats.plugins_used}")
        console.print(f"🤖 AI Interactions: {session_stats.ai_interactions}")
        console.print(f"❌ Errors: {session_stats.errors_encountered}")

        # Performance recommendations
        recommendations = stats_monitor.get_performance_recommendations()
        if recommendations:
            console.print("\n💡 Recommendations:")
            for rec in recommendations:
                console.print(f"  {rec}")

    except ImportError:
        console.print("❌ Statistics monitoring not available")

@app.command()
def setup_2fa(
    account_name: str = typer.Option("user@aion", help="Account name for 2FA setup")
):
    """Setup two-factor authentication"""
    try:
        from .security.otp_manager import setup_two_factor_auth
        success = setup_two_factor_auth(account_name)
        if success:
            console.print("✅ Two-factor authentication setup completed!")
        else:
            console.print("❌ 2FA setup failed")
    except ImportError:
        console.print("❌ 2FA setup not available")

@app.command()
def verify_2fa(
    otp_code: str = typer.Argument(..., help="OTP code from authenticator app or backup code")
):
    """Verify two-factor authentication code"""
    try:
        from .security.otp_manager import verify_otp_command
        success = verify_otp_command(otp_code)
        if success:
            console.print("✅ 2FA verification successful!")
        else:
            console.print("❌ Invalid 2FA code")
    except ImportError:
        console.print("❌ 2FA verification not available")

@app.command()
def toggle_theme():
    """Toggle between light and dark themes"""
    try:
        from .interfaces.animated_components import ThemeManager
        theme_manager = ThemeManager()
        theme_manager.toggle_theme()
        console.print(f"🎨 Theme switched to: {theme_manager.current_theme.value}")
    except ImportError:
        console.print("❌ Theme switching not available")

def main():
    """Main entry point for AION application"""
    app()

if __name__ == "__main__":
    main()
