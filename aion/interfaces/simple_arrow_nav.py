"""
Simple Arrow Navigation System
Enhanced and stable arrow-key navigation for AION
"""

import os
import sys
import time
import platform
from typing import List, Tuple, Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Try to import keyboard handling
try:
    if platform.system() == "Windows":
        import msvcrt
        WINDOWS_KEYS = True
    else:
        import termios
        import tty
        UNIX_KEYS = True
except ImportError:
    WINDOWS_KEYS = False
    UNIX_KEYS = False

console = Console()

class SimpleArrowNavigator:
    """Simple and stable arrow navigation system"""
    
    def __init__(self, items: List[Tuple[str, str]], title: str = "Selection"):
        """
        Initialize simple navigator
        
        Args:
            items: List of (value, display_name) tuples
            title: Title for the selection
        """
        self.items = items
        self.title = title
        self.selected_index = 0
        self.running = True
        
    def get_key(self) -> str:
        """Get a single keypress - cross-platform"""
        if platform.system() == "Windows" and WINDOWS_KEYS:
            return self._get_key_windows()
        elif UNIX_KEYS:
            return self._get_key_unix()
        else:
            # Fallback to input
            return input("Enter choice (up/down/enter/esc): ").lower()
    
    def _get_key_windows(self) -> str:
        """Windows key handling"""
        try:
            key = msvcrt.getch()
            if key == b'\xe0':  # Special key prefix
                key = msvcrt.getch()
                if key == b'H':  # Up arrow
                    return 'up'
                elif key == b'P':  # Down arrow
                    return 'down'
            elif key == b'\r':  # Enter
                return 'enter'
            elif key == b'\x1b':  # Escape
                return 'escape'
            elif key.lower() == b'q':
                return 'escape'
        except:
            pass
        return 'unknown'
    
    def _get_key_unix(self) -> str:
        """Unix/Linux key handling"""
        try:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.setraw(sys.stdin.fileno())
            
            key = sys.stdin.read(1)
            
            if key == '\x1b':  # Escape sequence
                key += sys.stdin.read(2)
                if key == '\x1b[A':  # Up arrow
                    return 'up'
                elif key == '\x1b[B':  # Down arrow
                    return 'down'
                else:
                    return 'escape'
            elif key == '\r' or key == '\n':  # Enter
                return 'enter'
            elif key.lower() == 'q':
                return 'escape'
            
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except:
            pass
        return 'unknown'
    
    def render_menu(self) -> None:
        """Render the menu with current selection"""
        # Clear screen
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')
        
        # Create menu content
        lines = []
        lines.append(f"🎯 {self.title}")
        lines.append("─" * 40)
        lines.append("Use ↑↓ arrows to navigate, Enter to select, Esc/Q to cancel")
        lines.append("")
        
        for i, (value, display_name) in enumerate(self.items):
            if i == self.selected_index:
                # Selected item
                lines.append(f"► [SELECTED] {display_name}")
            else:
                # Unselected item
                lines.append(f"  {display_name}")
        
        lines.append("")
        lines.append("─" * 40)
        lines.append(f"Selection: {self.selected_index + 1}/{len(self.items)}")
        
        # Print menu
        for line in lines:
            print(line)
    
    def navigate(self) -> Optional[str]:
        """Start navigation and return selected value"""
        try:
            while self.running:
                self.render_menu()
                
                key = self.get_key()
                
                if key == 'up':
                    self.selected_index = (self.selected_index - 1) % len(self.items)
                elif key == 'down':
                    self.selected_index = (self.selected_index + 1) % len(self.items)
                elif key == 'enter':
                    selected_value = self.items[self.selected_index][0]
                    selected_name = self.items[self.selected_index][1]
                    
                    # Clear screen and show selection
                    if platform.system() == "Windows":
                        os.system('cls')
                    else:
                        os.system('clear')
                    
                    print(f"✅ Selected: {selected_name}")
                    time.sleep(1)
                    return selected_value
                elif key == 'escape':
                    # Clear screen
                    if platform.system() == "Windows":
                        os.system('cls')
                    else:
                        os.system('clear')
                    
                    print("❌ Selection cancelled")
                    time.sleep(1)
                    return None
                elif key in ['up', 'down', 'enter', 'esc']:
                    # Handle fallback input
                    if key == 'up' and self.selected_index > 0:
                        self.selected_index -= 1
                    elif key == 'down' and self.selected_index < len(self.items) - 1:
                        self.selected_index += 1
                    elif key == 'enter':
                        return self.items[self.selected_index][0]
                    elif key == 'esc':
                        return None
                
        except KeyboardInterrupt:
            print("\n❌ Navigation interrupted")
            return None
        except Exception as e:
            print(f"❌ Navigation error: {e}")
            return None

def select_language_simple() -> str:
    """Simple language selection with arrow navigation"""
    languages = [
        ("en", "🇬🇧 English"),
        ("ar", "🇮🇶 العربية (Arabic)"),
        ("no", "🇳🇴 Norsk (Norwegian)"),
        ("de", "🇩🇪 Deutsch (German)"),
        ("fr", "🇫🇷 Français (French)"),
        ("zh", "🇨🇳 中文 (Chinese)"),
        ("es", "🇪🇸 Español (Spanish)")
    ]
    
    navigator = SimpleArrowNavigator(languages, "🌐 Language Selection")
    result = navigator.navigate()
    
    # Always return a valid language code
    return result if result else "en"

def select_ai_provider_simple() -> str:
    """Simple AI provider selection with arrow navigation"""
    providers = [
        ("openai", "🧠 OpenAI (GPT-4)"),
        ("deepseek", "🛰️ DeepSeek"),
        ("anthropic", "🤖 Anthropic (Claude)"),
        ("google", "🌐 Google (Gemini)"),
        ("openrouter", "🛤️ OpenRouter")
    ]
    
    navigator = SimpleArrowNavigator(providers, "🤖 AI Provider Selection")
    result = navigator.navigate()
    
    # Always return a valid provider
    return result if result else "openai"

def select_theme_simple() -> str:
    """Simple theme selection with arrow navigation"""
    themes = [
        ("dark", "🌙 Dark Theme"),
        ("light", "☀️ Light Theme"),
        ("auto", "🔄 Auto (System)"),
        ("blue", "🔵 Blue Theme"),
        ("green", "🟢 Green Theme")
    ]
    
    navigator = SimpleArrowNavigator(themes, "🎨 Theme Selection")
    result = navigator.navigate()
    
    return result if result else "dark"
