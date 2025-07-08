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
    # FORCE English as default - no user selection needed
    console.print("\n🌐 [bold green]Language: English (Default)[/bold green]")
    console.print("💡 [dim]Use 'change-language' command to switch languages later[/dim]")
    translator.set_language("en")
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

@app.command("change-language")
def change_language():
    """Change interface language using arrow key navigation"""
    try:
        from aion.interfaces.arrow_navigation import select_language_arrows
        console.print("\n🌐 [bold yellow]Language Selection[/bold yellow]")
        lang_code = select_language_arrows()
        if lang_code:
            translator.set_language(lang_code)
            console.print(f"\n✅ [bold green]Language changed to: {translator.get_language_name(lang_code)}[/bold green]")
        else:
            console.print("\n❌ [bold red]Language change cancelled[/bold red]")
    except Exception as e:
        console.print(f"\n⚠️ [bold red]Error changing language: {e}[/bold red]")
        console.print("🔄 [bold yellow]Keeping current language[/bold yellow]")

@app.command("send-email")
def send_email():
    """Send files or content via email"""
    try:
        from aion.integrations.email_system import email_system
        console.print("\n📧 [bold yellow]AION Email Sharing[/bold yellow]")
        success = email_system.send_email_interactive()
        if success:
            console.print("✅ [green]Email sent successfully![/green]")
        else:
            console.print("❌ [red]Email sending failed[/red]")
    except Exception as e:
        console.print(f"\n⚠️ [bold red]Email error: {e}[/bold red]")
        console.print("💡 [cyan]Make sure email is configured in .env file[/cyan]")

@app.command("github-tools")
def github_tools():
    """GitHub integration tools for repository management"""
    try:
        from aion.integrations.github_tools import github_tools
        console.print("\n🐙 [bold yellow]AION GitHub Tools[/bold yellow]")
        success = github_tools.github_tools_interactive()
        if success:
            console.print("✅ [green]GitHub operation completed![/green]")
        else:
            console.print("❌ [red]GitHub operation failed[/red]")
    except Exception as e:
        console.print(f"\n⚠️ [bold red]GitHub error: {e}[/bold red]")
        console.print("💡 [cyan]Make sure AION_GITHUB_TOKEN is set in .env file[/cyan]")

@app.command("chat")
def chat():
    """Launch full-screen AI chat mode"""
    try:
        from aion.ai.chatbot import aion_chatbot
        console.print("\n💬 [bold yellow]AION AI Chat Mode[/bold yellow]")
        console.print("🚀 [cyan]Starting interactive chat session...[/cyan]")

        # Start chat session
        session_id = aion_chatbot.start_chat_session()
        console.print(f"📋 [green]Session ID: {session_id}[/green]")
        console.print("💡 [yellow]Type 'exit' or 'quit' to end session[/yellow]")
        console.print("🧠 [cyan]I'll remember our entire conversation![/cyan]")
        console.print("---")

        # Interactive chat loop
        while True:
            try:
                user_input = input("\n👤 You: ").strip()

                if user_input.lower() in ['exit', 'quit', 'bye']:
                    console.print("👋 [yellow]Ending chat session...[/yellow]")
                    aion_chatbot.end_chat_session("User ended session")
                    break

                if not user_input:
                    continue

                console.print("🤖 AI: Thinking...")

                # Get AI response
                import asyncio
                response = asyncio.run(aion_chatbot.send_message(user_input))
                console.print(f"🤖 AI: {response}")

            except KeyboardInterrupt:
                console.print("\n👋 [yellow]Chat interrupted by user[/yellow]")
                aion_chatbot.end_chat_session("Interrupted by user")
                break
            except Exception as e:
                console.print(f"❌ [red]Chat error: {e}[/red]")

        console.print("✅ [green]Chat session ended![/green]")

    except Exception as e:
        console.print(f"\n⚠️ [bold red]Chat error: {e}[/bold red]")
        console.print("💡 [cyan]Make sure AI system is configured[/cyan]")

@app.command("search")
def search_command(
    topic: str = typer.Argument(..., help="Topic to search for"),
    sources: str = typer.Option("stackoverflow,github,python_docs", help="Comma-separated list of sources"),
    max_results: int = typer.Option(10, help="Maximum number of results")
):
    """Smart search across developer resources (Stack Overflow, GitHub, Python Docs)"""
    try:
        from aion.ai.smart_search import smart_search
        import asyncio

        console.print(f"\n🔍 [bold yellow]Smart Search: {topic}[/bold yellow]")

        # Parse sources
        source_list = [s.strip() for s in sources.split(",")]

        console.print(f"📡 [cyan]Searching {', '.join(source_list)}...[/cyan]")

        # Perform search
        search_results = asyncio.run(smart_search.search(topic, source_list, max_results))

        # Format and display results
        formatted_output = smart_search.format_search_results(search_results)
        console.print(formatted_output)

        console.print(f"\n✅ [green]Search completed in {search_results.search_time:.2f}s![/green]")
        console.print(f"📝 [cyan]Results logged to: search_logs/query_*.log[/cyan]")

    except Exception as e:
        console.print(f"\n⚠️ [bold red]Search error: {e}[/bold red]")
        console.print("💡 [cyan]Try: aion search [topic][/cyan]")

@app.command("explain")
def explain_command(command: str = typer.Argument(..., help="Command to explain")):
    """Explain terminal commands with AI-powered analysis"""
    try:
        from aion.ai.command_explainer import command_explainer
        import asyncio

        console.print(f"\n📘 [bold yellow]Explaining Command: {command}[/bold yellow]")
        console.print("🔍 [cyan]Analyzing command with AI...[/cyan]")

        # Get command explanation
        explanation = asyncio.run(command_explainer.explain_command(command))

        # Format and display explanation
        formatted_output = command_explainer.format_explanation_display(explanation)
        console.print(formatted_output)

        console.print(f"\n✅ [green]Command explanation completed![/green]")
        console.print(f"📝 [cyan]Logged to: test_logs/system_command_explanation.log[/cyan]")

    except Exception as e:
        console.print(f"\n⚠️ [bold red]Command explanation error: {e}[/bold red]")
        console.print("💡 [cyan]Try: aion explain [command][/cyan]")

@app.command("ai-assist")
def ai_assist():
    """AI-powered code analysis and suggestions"""
    try:
        from aion.integrations.ai_code_assist import ai_code_assist
        console.print("\n💡 [bold yellow]AION AI Code Assistant[/bold yellow]")
        success = ai_code_assist.analyze_code_interactive()
        if success:
            console.print("✅ [green]Code analysis completed![/green]")
        else:
            console.print("❌ [red]Code analysis failed[/red]")
    except Exception as e:
        console.print(f"\n⚠️ [bold red]AI assistance error: {e}[/bold red]")
        console.print("💡 [cyan]Make sure AI provider is configured[/cyan]")

@app.command("ai-use")
def ai_use(provider: str):
    """Switch AI provider (openai, deepseek, anthropic, google, openrouter)"""
    try:
        from aion.ai_engine.provider_router import provider_router
        console.print(f"\n🔀 [bold yellow]Switching to AI Provider: {provider}[/bold yellow]")

        success = provider_router.switch_provider(provider)
        if success:
            console.print(f"✅ [green]Successfully switched to {provider}[/green]")
            console.print(f"🧠 [cyan]Current provider: {provider_router.get_current_provider()}[/cyan]")
        else:
            console.print(f"❌ [red]Failed to switch to {provider}[/red]")
            console.print("💡 [yellow]Available providers: openai, deepseek, anthropic, google, openrouter[/yellow]")
    except Exception as e:
        console.print(f"\n⚠️ [bold red]Provider switching error: {e}[/bold red]")
        console.print("💡 [cyan]Make sure AI engine is properly configured[/cyan]")

@app.command("ai-status")
def ai_status():
    """Show current AI provider status and configuration"""
    try:
        from aion.ai_engine.provider_router import provider_router
        console.print("\n🧠 [bold yellow]AI Provider Status[/bold yellow]")

        current = provider_router.get_current_provider()
        console.print(f"📍 [green]Current Provider: {current}[/green]")

        # Show available providers
        providers = provider_router.get_available_providers()
        console.print("\n📋 [cyan]Available Providers:[/cyan]")
        for provider in providers:
            status = "✅ Ready" if provider_router.is_provider_ready(provider) else "❌ Not configured"
            console.print(f"  • {provider}: {status}")

    except Exception as e:
        console.print(f"\n⚠️ [bold red]AI status error: {e}[/bold red]")
        console.print("💡 [cyan]Make sure AI engine is properly configured[/cyan]")

@app.command("voice")
def voice():
    """Launch voice assistant mode"""
    try:
        from aion.ai_engine.ai_interface import ai_interface
        console.print("\n🔊 [bold yellow]AION Voice Assistant[/bold yellow]")
        console.print("🎤 [cyan]Voice mode is not yet fully implemented[/cyan]")
        console.print("💡 [yellow]This feature will be available in a future update[/yellow]")
        console.print("🔄 [green]For now, use text-based chat: aion chat[/green]")
    except Exception as e:
        console.print(f"\n⚠️ [bold red]Voice assistant error: {e}[/bold red]")
        console.print("💡 [cyan]Feature under development[/cyan]")

def main():
    """Main entry point for AION application"""
    app()

if __name__ == "__main__":
    main()
