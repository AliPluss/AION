#!/usr/bin/env python3
"""
Pure Arrow-Key Navigation System for AION
Provides keyboard-only navigation without manual input
"""

import sys
import platform
from typing import List, Tuple, Optional, Callable
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
# IntPrompt removed - using pure arrow navigation only

# Windows-compatible imports
if platform.system() == "Windows":
    try:
        import msvcrt
        WINDOWS_KEYS = True
    except ImportError:
        WINDOWS_KEYS = False
else:
    try:
        import termios
        import tty
        UNIX_KEYS = True
    except ImportError:
        UNIX_KEYS = False

console = Console()

class ArrowNavigator:
    """Pure arrow-key navigation system"""
    
    def __init__(self, items: List[Tuple[str, str, str]], title: str = "Selection"):
        """
        Initialize arrow navigator
        
        Args:
            items: List of (value, display_name, animation) tuples
            title: Title for the selection panel
        """
        self.items = items
        self.title = title
        self.selected_index = 0
        self.running = True
        
    def render_menu(self) -> Panel:
        """Render the navigation menu with current selection"""
        lines = []
        lines.append(f"[bold cyan]{self.title}[/bold cyan]")
        lines.append("[dim]Use ↑↓ arrows to navigate, Enter to select, Esc to cancel[/dim]")
        lines.append("")
        
        for i, (value, display_name, animation) in enumerate(self.items):
            if i == self.selected_index:
                # Selected item with animation and highlight
                prefix = "► "
                style = "[bold bright_white on blue]"
                suffix = f" {animation}[/bold bright_white on blue]"
            else:
                # Normal item
                prefix = "  "
                style = "[white]"
                suffix = f" [dim]{animation}[/dim]"
            
            lines.append(f"{style}{prefix}{display_name}{suffix}")
        
        lines.append("")
        lines.append("[dim]Press Enter to confirm selection[/dim]")
        
        return Panel("\n".join(lines), border_style="bright_blue", title="🎮 Arrow Navigation")
    
    def get_key(self) -> str:
        """Get single keypress without Enter - Windows compatible"""
        if platform.system() == "Windows" and WINDOWS_KEYS:
            try:
                import msvcrt
                key = msvcrt.getch()
                if key == b'\xe0':  # Arrow key prefix on Windows
                    key = msvcrt.getch()
                    if key == b'H':
                        return 'up'
                    elif key == b'P':
                        return 'down'
                elif key == b'\r':
                    return 'enter'
                elif key == b'\x1b':
                    return 'esc'
                return key.decode('utf-8', errors='ignore')
            except:
                return 'fallback'
        elif platform.system() != "Windows" and 'UNIX_KEYS' in globals() and UNIX_KEYS:
            try:
                # Unix/Linux/macOS
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    key = sys.stdin.read(1)
                    if key == '\x1b':  # ESC sequence
                        key += sys.stdin.read(2)
                        if key == '\x1b[A':
                            return 'up'
                        elif key == '\x1b[B':
                            return 'down'
                        else:
                            return 'esc'
                    elif key == '\r' or key == '\n':
                        return 'enter'
                    elif key == '\x1b':
                        return 'esc'
                    return key
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except:
                return 'fallback'
        else:
            # Fallback for unsupported systems
            return 'fallback'
    
    def navigate(self) -> Optional[str]:
        """
        Start arrow navigation and return selected value

        Returns:
            Selected value or None if cancelled
        """
        # Try arrow navigation first
        try:
            console.print(f"\n🎮 [bold yellow]Arrow Navigation Active[/bold yellow]")
            console.print("[dim]Use ↑↓ arrows to navigate, Enter to select, Esc to cancel[/dim]")

            with Live(self.render_menu(), refresh_per_second=10) as live:
                while self.running:
                    try:
                        key = self.get_key()

                        if key == 'fallback':
                            # Switch to numbered fallback
                            break
                        elif key == 'up':
                            self.selected_index = (self.selected_index - 1) % len(self.items)
                            live.update(self.render_menu())
                        elif key == 'down':
                            self.selected_index = (self.selected_index + 1) % len(self.items)
                            live.update(self.render_menu())
                        elif key == 'enter':
                            selected_value = self.items[self.selected_index][0]
                            selected_name = self.items[self.selected_index][1]
                            selected_animation = self.items[self.selected_index][2]

                            # Show confirmation
                            console.print(f"\n✅ Selected: [bold green]{selected_name}[/bold green] ({selected_animation})")
                            return selected_value
                        elif key == 'esc':
                            console.print("\n❌ Selection cancelled")
                            return None

                    except KeyboardInterrupt:
                        console.print("\n❌ Selection cancelled")
                        return None
                    except Exception:
                        # Switch to fallback on any error
                        break

        except Exception:
            pass  # Fall through to numbered fallback

        # If arrow navigation fails, return default selection
        console.print("\n⚠️ [bold red]Arrow navigation not available[/bold red]")
        selected_value = self.items[self.selected_index][0]
        selected_name = self.items[self.selected_index][1]
        console.print(f"🔄 [bold yellow]Using default: {selected_name}[/bold yellow]")
        return selected_value

def select_with_arrows(items: List[Tuple[str, str, str]], title: str = "Selection", default_index: int = 0) -> str:
    """
    Convenience function for arrow-key selection - guaranteed to return a value

    Args:
        items: List of (value, display_name, animation) tuples
        title: Selection title
        default_index: Default selected index

    Returns:
        Selected value (never None)
    """
    try:
        navigator = ArrowNavigator(items, title)
        navigator.selected_index = default_index

        result = navigator.navigate()
        # Always return a valid result
        if result is not None:
            return result
        else:
            # If navigation was cancelled, return default
            console.print(f"\n🔄 [bold yellow]Using default: {items[default_index][1]}[/bold yellow]")
            return items[default_index][0]
    except Exception as e:
        # If any error occurs, return default
        console.print(f"\n⚠️ [bold red]Selection error: {e}[/bold red]")
        console.print(f"🔄 [bold yellow]Using default: {items[default_index][1]}[/bold yellow]")
        return items[default_index][0]

# Language selection with pure arrow navigation
def select_language_arrows() -> str:
    """Pure arrow-key language selection - guaranteed to return a language code"""
    languages = [
        ("en", "English 🇬🇧", "🧠 Pulse"),
        ("ar", "العربية 🇮🇶", "🇮🇶 Bounce RTL"),
        ("no", "Norsk 🇳🇴", "✨ Glow"),
        ("de", "Deutsch 🇩🇪", "🌊 Wave"),
        ("fr", "Français 🇫🇷", "💫 Sparkle"),
        ("zh", "中文 🇨🇳", "🎭 Fade"),
        ("es", "Español 🇪🇸", "⚡ Flash")
    ]

    console.print("\n🎮 [bold yellow]Pure Arrow-Key Navigation Active[/bold yellow]")
    console.print("[dim]Use ↑↓ arrows to navigate, Enter to select, Esc for English default[/dim]\n")

    try:
        result = select_with_arrows(languages, "🌐 Language Selection", default_index=0)
        # Always return a valid language code, default to English if None
        return result if result else "en"
    except Exception as e:
        console.print(f"\n⚠️ [bold red]Navigation error: {e}[/bold red]")
        console.print("🔄 [bold yellow]Defaulting to English[/bold yellow]")
        return "en"

# AI Provider selection with arrows
def select_ai_provider_arrows() -> str:
    """Pure arrow-key AI provider selection"""
    providers = [
        ("openai", "OpenAI GPT 🧠", "🧠 Pulse"),
        ("deepseek", "DeepSeek 🛰️", "🛰️ Orbit"),
        ("google", "Google Gemini 🌐", "🌐 Ripple"),
        ("openrouter", "OpenRouter 🛤️", "🛤️ Slide")
    ]
    
    console.print("\n🤖 [bold yellow]AI Provider Selection[/bold yellow]")
    console.print("[dim]Navigate with arrows, Enter to select[/dim]\n")
    
    return select_with_arrows(providers, "🤖 AI Provider Selection", default_index=0)

# Plugin selection with arrows
def select_plugin_arrows(plugins: List[str]) -> Optional[str]:
    """Pure arrow-key plugin selection"""
    if not plugins:
        console.print("❌ No plugins available")
        return None
        
    plugin_items = [
        (plugin, f"🧩 {plugin}", "🧩 Wiggle") 
        for plugin in plugins
    ]
    
    console.print("\n🧩 [bold yellow]Plugin Selection[/bold yellow]")
    console.print("[dim]Choose plugin to execute[/dim]\n")
    
    return select_with_arrows(plugin_items, "🧩 Plugin Selection", default_index=0)
