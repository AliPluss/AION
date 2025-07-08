#!/usr/bin/env python3
"""
Pure Arrow-Key Navigation System for AION
Provides keyboard-only navigation without manual input
"""

import sys
import platform
import time
import math
import re
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
        """Render the navigation menu with current selection and live animations"""
        lines = []
        lines.append(f"[bold cyan]{self.title}[/bold cyan]")
        lines.append("[dim]Use ↑↓ arrows to navigate, Enter to select, Esc to cancel[/dim]")
        lines.append("")

        # Get current time for animation effects
        current_time = time.time()

        for i, (value, display_name, animation) in enumerate(self.items):
            if i == self.selected_index:
                # Selected item with live animation and highlight
                prefix = "► "
                style = "[bold bright_white on blue]"

                # Apply live animation effects based on animation type
                animated_icon = self._get_animated_icon(animation, current_time, selected=True)
                display_text = f"{animated_icon} {display_name}"
                suffix = "[/bold bright_white on blue]"
            else:
                # Normal item with subtle animation
                prefix = "  "
                style = "[white]"

                # Subtle animation for non-selected items
                animated_icon = self._get_animated_icon(animation, current_time, selected=False)
                display_text = f"{animated_icon} {display_name}"
                suffix = ""

            lines.append(f"{style}{prefix}{display_text}{suffix}")

        lines.append("")
        lines.append("[dim]Press Enter to confirm selection[/dim]")

        return Panel("\n".join(lines), border_style="bright_blue", title="🎮 Arrow Navigation")

    def _get_animated_icon(self, animation_text: str, current_time: float, selected: bool = False) -> str:
        """Generate animated icon based on animation type and time"""
        # Extract icon and animation type from animation_text
        if "🧠" in animation_text and "Pulse" in animation_text:
            return self._pulse_animation("🧠", current_time, selected)
        elif "🇮🇶" in animation_text and "Bounce" in animation_text:
            return self._bounce_animation("🇮🇶", current_time, selected)
        elif "🛰️" in animation_text and "Orbit" in animation_text:
            return self._orbit_animation("🛰️", current_time, selected)
        elif "🌐" in animation_text and "Ripple" in animation_text:
            return self._ripple_animation("🌐", current_time, selected)
        elif "🛤️" in animation_text and "Slide" in animation_text:
            return self._slide_animation("🛤️", current_time, selected)
        elif "✨" in animation_text:
            return self._sparkle_animation("✨", current_time, selected)
        elif "🧩" in animation_text:
            return self._wiggle_animation("🧩", current_time, selected)
        elif "📋" in animation_text:
            return self._list_animation("📋", current_time, selected)
        elif "⬇️" in animation_text:
            return self._download_animation("⬇️", current_time, selected)
        elif "🗑️" in animation_text:
            return self._delete_animation("🗑️", current_time, selected)
        elif "✅" in animation_text:
            return self._check_animation("✅", current_time, selected)
        elif "❌" in animation_text:
            return self._x_animation("❌", current_time, selected)
        elif "🔙" in animation_text:
            return self._back_animation("🔙", current_time, selected)
        else:
            # Extract first emoji from animation_text or use default
            emoji_match = re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002600-\U000026FF\U00002700-\U000027BF]', animation_text)
            if emoji_match:
                return emoji_match.group(0)
            return "•"

    def _pulse_animation(self, icon: str, current_time: float, selected: bool) -> str:
        """Pulse animation for brain/AI icons"""
        if selected:
            # Fast pulse when selected
            pulse_cycle = (math.sin(current_time * 8) + 1) / 2
            if pulse_cycle > 0.7:
                return f"[bold bright_cyan]{icon}[/bold bright_cyan]"
            elif pulse_cycle > 0.4:
                return f"[cyan]{icon}[/cyan]"
            else:
                return icon
        else:
            # Slow pulse when not selected
            pulse_cycle = (math.sin(current_time * 2) + 1) / 2
            if pulse_cycle > 0.8:
                return f"[dim cyan]{icon}[/dim cyan]"
            else:
                return f"[dim]{icon}[/dim]"

    def _bounce_animation(self, icon: str, current_time: float, selected: bool) -> str:
        """Bounce animation for Arabic/RTL icons"""
        if selected:
            # RTL bounce effect
            bounce_cycle = abs(math.sin(current_time * 6))
            if bounce_cycle > 0.8:
                return f"[bold bright_yellow]{icon}[/bold bright_yellow]"
            elif bounce_cycle > 0.5:
                return f"[yellow]{icon}[/yellow]"
            else:
                return icon
        else:
            return f"[dim]{icon}[/dim]"

    def _orbit_animation(self, icon: str, current_time: float, selected: bool) -> str:
        """Orbit animation for satellite/DeepSeek icons"""
        if selected:
            # Orbital rotation effect
            orbit_cycle = (current_time * 4) % (2 * math.pi)
            if orbit_cycle < math.pi / 2:
                return f"[bold bright_blue]{icon}[/bold bright_blue]"
            elif orbit_cycle < math.pi:
                return f"[blue]{icon}[/blue]"
            elif orbit_cycle < 3 * math.pi / 2:
                return f"[dim blue]{icon}[/dim blue]"
            else:
                return icon
        else:
            return f"[dim]{icon}[/dim]"

    def _ripple_animation(self, icon: str, current_time: float, selected: bool) -> str:
        """Ripple animation for globe/Google icons"""
        if selected:
            ripple_cycle = (math.sin(current_time * 5) + 1) / 2
            if ripple_cycle > 0.6:
                return f"[bold bright_green]{icon}[/bold bright_green]"
            else:
                return f"[green]{icon}[/green]"
        else:
            return f"[dim]{icon}[/dim]"

    def _slide_animation(self, icon: str, current_time: float, selected: bool) -> str:
        """Slide animation for track/OpenRouter icons"""
        if selected:
            slide_cycle = (current_time * 3) % 1
            if slide_cycle < 0.5:
                return f"[bold bright_magenta]{icon}[/bold bright_magenta]"
            else:
                return f"[magenta]{icon}[/magenta]"
        else:
            return f"[dim]{icon}[/dim]"

    def _sparkle_animation(self, icon: str, current_time: float, selected: bool) -> str:
        """Sparkle animation for generic items"""
        if selected:
            sparkle_cycle = (math.sin(current_time * 7) + 1) / 2
            if sparkle_cycle > 0.7:
                return f"[bold bright_white]{icon}[/bold bright_white]"
            else:
                return f"[white]{icon}[/white]"
        else:
            return f"[dim]{icon}[/dim]"

    def _wiggle_animation(self, icon: str, current_time: float, selected: bool) -> str:
        """Wiggle animation for plugin icons"""
        if selected:
            wiggle_cycle = math.sin(current_time * 10) * 0.5
            if abs(wiggle_cycle) > 0.3:
                return f"[bold bright_red]{icon}[/bold bright_red]"
            else:
                return f"[red]{icon}[/red]"
        else:
            return f"[dim]{icon}[/dim]"

    def _list_animation(self, icon: str, current_time: float, selected: bool) -> str:
        """List animation for file/list icons"""
        if selected:
            return f"[bold bright_blue]{icon}[/bold bright_blue]"
        else:
            return f"[dim]{icon}[/dim]"

    def _download_animation(self, icon: str, current_time: float, selected: bool) -> str:
        """Download animation for install icons"""
        if selected:
            download_cycle = (current_time * 4) % 1
            if download_cycle < 0.3:
                return f"[bold bright_green]{icon}[/bold bright_green]"
            else:
                return f"[green]{icon}[/green]"
        else:
            return f"[dim]{icon}[/dim]"

    def _delete_animation(self, icon: str, current_time: float, selected: bool) -> str:
        """Delete animation for remove icons"""
        if selected:
            delete_cycle = (math.sin(current_time * 6) + 1) / 2
            if delete_cycle > 0.5:
                return f"[bold bright_red]{icon}[/bold bright_red]"
            else:
                return f"[red]{icon}[/red]"
        else:
            return f"[dim]{icon}[/dim]"

    def _check_animation(self, icon: str, current_time: float, selected: bool) -> str:
        """Check animation for enable icons"""
        if selected:
            return f"[bold bright_green]{icon}[/bold bright_green]"
        else:
            return f"[dim]{icon}[/dim]"

    def _x_animation(self, icon: str, current_time: float, selected: bool) -> str:
        """X animation for disable icons"""
        if selected:
            return f"[bold bright_red]{icon}[/bold bright_red]"
        else:
            return f"[dim]{icon}[/dim]"

    def _back_animation(self, icon: str, current_time: float, selected: bool) -> str:
        """Back animation for return icons"""
        if selected:
            back_cycle = (current_time * 3) % 1
            if back_cycle < 0.5:
                return f"[bold bright_yellow]{icon}[/bold bright_yellow]"
            else:
                return f"[yellow]{icon}[/yellow]"
        else:
            return f"[dim]{icon}[/dim]"

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
            import os

            # Clear screen properly for Windows
            if platform.system() == "Windows":
                os.system('cls')
            else:
                os.system('clear')

            console.print(f"\n🎮 [bold yellow]Arrow Navigation Active[/bold yellow]")
            console.print("[dim]Use ↑↓ arrows to navigate, Enter to select, Esc to cancel[/dim]")
            console.print(self.render_menu())

            while self.running:
                try:
                    key = self.get_key()

                    if key == 'fallback':
                        # Switch to numbered fallback
                        break
                    elif key in ['up', 'down']:
                        # Update selection
                        if key == 'up':
                            self.selected_index = (self.selected_index - 1) % len(self.items)
                        else:
                            self.selected_index = (self.selected_index + 1) % len(self.items)

                        # Clear screen properly for Windows
                        if platform.system() == "Windows":
                            os.system('cls')
                        else:
                            os.system('clear')

                        # Redraw interface
                        console.print(f"\n🎮 [bold yellow]Arrow Navigation Active[/bold yellow]")
                        console.print("[dim]Use ↑↓ arrows to navigate, Enter to select, Esc to cancel[/dim]")
                        console.print(self.render_menu())

                    elif key == 'enter':
                        selected_value = self.items[self.selected_index][0]
                        selected_name = self.items[self.selected_index][1]
                        selected_animation = self.items[self.selected_index][2]

                        # Clear and show confirmation
                        if platform.system() == "Windows":
                            os.system('cls')
                        else:
                            os.system('clear')
                        console.print(f"\n✅ Selected: [bold green]{selected_name}[/bold green] ({selected_animation})")
                        return selected_value

                    elif key == 'esc':
                        if platform.system() == "Windows":
                            os.system('cls')
                        else:
                            os.system('clear')
                        console.print("\n❌ Selection cancelled")
                        return None

                except KeyboardInterrupt:
                    if platform.system() == "Windows":
                        os.system('cls')
                    else:
                        os.system('clear')
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
