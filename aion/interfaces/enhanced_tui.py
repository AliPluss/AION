#!/usr/bin/env python3
"""
🎨 AION Enhanced Terminal User Interface
Next-generation TUI with fully animated and dynamic icon system

This module provides:
- Fully animated icon system for all UI elements
- Dynamic arrow key navigation with real-time feedback
- Live icon reactions and highlighting effects
- Cross-platform emoji support with ASCII fallback
- Performance-optimized animations for terminal environments
- Comprehensive keyboard shortcuts and accessibility
"""

import asyncio
import sys
import time
import uuid
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path

# Import new modules
try:
    from ..core.stats_monitor import stats_monitor
    from ..core.plugin_installer import plugin_installer, install_plugin_command
    from ..security.otp_manager import otp_manager, setup_two_factor_auth, verify_otp_command
    ENHANCED_FEATURES_AVAILABLE = True
except ImportError:
    ENHANCED_FEATURES_AVAILABLE = False
    print("⚠️ Enhanced features not available - some modules missing")

try:
    from textual.app import App, ComposeResult
    from textual.screen import Screen
    from textual.widget import Widget
    from textual.widgets import Header, Footer, Static, Button, Input, Log, TextArea
    from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
    from textual.reactive import reactive
    from textual.binding import Binding
    from textual import events, on
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text

# Import our animated components
from .animated_components import (
    AnimatedMenuManager, AnimatedSelector, SelectionItem, AnimatedIcon,
    AI_PROVIDER_ICONS, LANGUAGE_ICONS, SYSTEM_ICONS, AnimationType
)

class AnimatedButton(Widget):
    """Custom animated button with icon effects"""
    
    def __init__(self, label: str, icon: AnimatedIcon, callback: Optional[Callable] = None, **kwargs):
        super().__init__(**kwargs)
        self.label = label
        self.icon = icon
        self.callback = callback
        self.is_focused = False
        self.is_hovered = False
        self.frame_counter = 0
        self.animation_engine = None
        
    def on_mount(self):
        """Initialize animation engine when mounted"""
        from .animated_components import AnimationEngine
        self.animation_engine = AnimationEngine()
        self.set_interval(0.1, self._update_animation)
    
    def _update_animation(self):
        """Update animation frame"""
        self.frame_counter += 1
        self.refresh()
    
    def render(self) -> Text:
        """Render animated button with integrated icon and text"""
        if not self.animation_engine:
            # Fallback: single integrated line
            return Text(f"{self.icon.fallback} {self.label}")

        # Get animation style
        animation_style = self.animation_engine.get_animation_frame(
            self.icon.animation, self.frame_counter, self.icon.intensity
        )

        # Choose icon based on emoji support
        icon_display = self.icon.icon if self._supports_emoji() else self.icon.fallback

        # Apply focus/hover effects and create single integrated line
        if self.is_focused or self.is_hovered:
            # Selected state: integrate icon + text in single line with animation
            integrated_text = f"► {icon_display} {self.label}"
            style = f"[bold {self.icon.color}]{animation_style}"
        else:
            # Normal state: integrate icon + text in single line
            integrated_text = f"  {icon_display} {self.label}"
            style = f"[{self.icon.color}]"

        # Return single integrated Text object
        return Text(integrated_text, style=style)
    
    def on_focus(self):
        """Handle focus event"""
        self.is_focused = True
        self.refresh()
    
    def on_blur(self):
        """Handle blur event"""
        self.is_focused = False
        self.refresh()
    
    def on_enter(self):
        """Handle mouse enter"""
        self.is_hovered = True
        self.refresh()
    
    def on_leave(self):
        """Handle mouse leave"""
        self.is_hovered = False
        self.refresh()
    
    def on_click(self):
        """Handle click event"""
        if self.callback:
            self.callback()
    
    def _supports_emoji(self) -> bool:
        """Check if terminal supports emoji"""
        try:
            "🧠".encode('utf-8')
            return True
        except:
            return False

class EnhancedAIONApp(App):
    """Enhanced AION App with animated components"""
    
    CSS = """
    #main-container {
        padding: 1;
        background: $surface;
    }
    
    #welcome-panel {
        background: $panel;
        border: solid $primary;
        margin: 1;
        padding: 1;
    }
    
    #menu-container {
        align: center middle;
        margin: 1;
    }
    
    #status-bar {
        background: $surface;
        color: $text-muted;
        text-align: center;
        margin: 1 0;
    }
    
    AnimatedButton {
        margin: 0 1;
        min-width: 25;
        height: 3;
    }
    
    .focused {
        background: $accent 20%;
        border: solid $accent;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("escape", "back", "Back"),
        ("h", "help", "Help"),
        ("ctrl+c", "quit", "Quit"),
        ("up", "move_up", "Move Up"),
        ("down", "move_down", "Move Down"),
        ("left", "move_left", "Move Left"),
        ("right", "move_right", "Move Right"),
        ("enter", "select", "Select"),
        ("ctrl+t", "toggle_theme", "Toggle Theme"),
        ("ctrl+s", "show_stats", "Show Stats"),
        ("ctrl+i", "install_plugin", "Install Plugin"),
        ("ctrl+2", "setup_2fa", "Setup 2FA"),
        ("f1", "help", "Help"),
        ("f2", "toggle_theme", "Theme"),
        ("f3", "show_stats", "Stats"),
        ("f4", "install_plugin", "Plugin"),
        ("f5", "setup_2fa", "2FA"),
    ]
    
    def __init__(self, translator=None, ai_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.translator = translator
        self.ai_manager = ai_manager
        self.menu_manager = AnimatedMenuManager()
        self.current_selection = 0
        self.menu_items = []
        
    def compose(self) -> ComposeResult:
        """Compose the enhanced UI"""
        yield Header(show_clock=True)
        yield Container(
            Static(self._get_welcome_message(), id="welcome-panel"),
            Container(
                self._create_main_menu(),
                id="menu-container"
            ),
            Static("🎮 Use ↑↓←→ arrows to navigate • Enter to select • Q to quit", id="status-bar"),
            id="main-container"
        )
        yield Footer()
    
    def _get_welcome_message(self) -> str:
        """Get animated welcome message"""
        return """🎯 Welcome to AION - AI Operating Node
        
🚀 Next-Generation Terminal AI Assistant
🎨 Enhanced with Dynamic Animated Interface
🔥 Professional-Grade Performance & Security

Ready for intelligent terminal operations..."""
    
    def _create_main_menu(self) -> Container:
        """Create animated main menu"""
        self.menu_items = [
            ("ai", "AI Assistant", AI_PROVIDER_ICONS["openai"]),
            ("code", "Code Execution", SYSTEM_ICONS["terminal"]),
            ("files", "File Manager", SYSTEM_ICONS["file_explorer"]),
            ("plugins", "Plugin Manager", SYSTEM_ICONS["plugin_manager"]),
            ("settings", "Settings", SYSTEM_ICONS["settings"]),
        ]
        
        buttons = []
        for i, (key, label, icon) in enumerate(self.menu_items):
            button = AnimatedButton(
                label=label,
                icon=icon,
                callback=lambda k=key: self._handle_menu_selection(k),
                id=f"btn-{key}"
            )
            buttons.append(button)
        
        return Vertical(*buttons)
    
    def _handle_menu_selection(self, selection: str):
        """Handle menu selection"""
        if selection == "ai":
            self.push_screen(EnhancedAIScreen(self.translator, self.ai_manager))
        elif selection == "code":
            self.push_screen(EnhancedCodeScreen(self.translator))
        elif selection == "files":
            self.push_screen(EnhancedFileScreen(self.translator))
        elif selection == "plugins":
            self.push_screen(EnhancedPluginScreen(self.translator))
        elif selection == "settings":
            self.push_screen(EnhancedSettingsScreen(self.translator))
    
    def action_move_up(self):
        """Move selection up"""
        self.current_selection = max(0, self.current_selection - 1)
        self._update_focus()
    
    def action_move_down(self):
        """Move selection down"""
        self.current_selection = min(len(self.menu_items) - 1, self.current_selection + 1)
        self._update_focus()
    
    def action_select(self):
        """Select current item"""
        if 0 <= self.current_selection < len(self.menu_items):
            key, _, _ = self.menu_items[self.current_selection]
            self._handle_menu_selection(key)
    
    def _update_focus(self):
        """Update focus based on current selection"""
        for i, (key, _, _) in enumerate(self.menu_items):
            button = self.query_one(f"#btn-{key}")
            if i == self.current_selection:
                button.focus()
            else:
                button.blur()

class EnhancedAIScreen(Screen):
    """Enhanced AI Assistant screen with animated provider selection"""
    
    BINDINGS = [("escape", "back", "Back")]
    
    def __init__(self, translator, ai_manager):
        super().__init__()
        self.translator = translator
        self.ai_manager = ai_manager
        self.menu_manager = AnimatedMenuManager()
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("🤖 AI Assistant - Enhanced Interface", id="title"),
            Container(
                self._create_provider_selection(),
                id="provider-container"
            ),
            TextArea("Enter your AI prompt here...", id="prompt-input"),
            Log(id="ai-output"),
            id="ai-container"
        )
        yield Footer()
    
    def _create_provider_selection(self) -> Container:
        """Create animated AI provider selection with integrated icons"""
        providers = ["openai", "deepseek", "google", "openrouter"]
        buttons = []

        for provider in providers:
            if provider in AI_PROVIDER_ICONS:
                icon = AI_PROVIDER_ICONS[provider]
                button = AnimatedButton(
                    label=icon.description,
                    icon=icon,
                    callback=lambda p=provider: self._select_provider(p),
                    id=f"provider-{provider}"
                )
                buttons.append(button)

        # Use Vertical layout for better arrow key navigation and integrated display
        return Vertical(*buttons)
    
    def _select_provider(self, provider: str):
        """Select AI provider"""
        if self.ai_manager:
            self.ai_manager.set_current_provider(provider)
        
        # Update UI to show selection
        output = self.query_one("#ai-output")
        output.write_line(f"✅ Selected AI Provider: {provider}")
    
    def action_back(self):
        """Go back to main menu"""
        self.app.pop_screen()

class EnhancedSettingsScreen(Screen):
    """Enhanced settings screen with animated options"""
    
    BINDINGS = [("escape", "back", "Back")]
    
    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.menu_manager = AnimatedMenuManager()
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("⚙️ Settings - Enhanced Configuration", id="title"),
            Container(
                self._create_language_selection(),
                self._create_security_selection(),
                id="settings-container"
            ),
            id="main-settings"
        )
        yield Footer()
    
    def _create_language_selection(self) -> Container:
        """Create animated language selection with integrated icons"""
        languages = ["en", "ar", "no", "de", "fr", "es", "zh"]
        buttons = []

        for lang in languages:
            if lang in LANGUAGE_ICONS:
                icon = LANGUAGE_ICONS[lang]
                button = AnimatedButton(
                    label=icon.description,
                    icon=icon,
                    callback=lambda l=lang: self._select_language(l),
                    id=f"lang-{lang}"
                )
                buttons.append(button)

        return Container(
            Static("🌐 Language Selection", id="lang-title"),
            Vertical(*buttons),  # Changed to Vertical for better navigation
            id="language-section"
        )
    
    def _create_security_selection(self) -> Container:
        """Create animated security level selection with integrated icons"""
        security_levels = [
            ("high", SYSTEM_ICONS["security_high"]),
            ("medium", SYSTEM_ICONS["security_medium"]),
            ("low", SYSTEM_ICONS["security_low"]),
        ]

        buttons = []
        for level, icon in security_levels:
            button = AnimatedButton(
                label=icon.description,
                icon=icon,
                callback=lambda l=level: self._select_security(l),
                id=f"security-{level}"
            )
            buttons.append(button)

        return Container(
            Static("🔐 Security Level", id="security-title"),
            Vertical(*buttons),  # Changed to Vertical for better navigation
            id="security-section"
        )
    
    def _select_language(self, language: str):
        """Select language"""
        if self.translator:
            self.translator.set_language(language)
        # Update UI feedback here
    
    def _select_security(self, level: str):
        """Select security level"""
        # Update security level here
        pass
    
    def action_back(self):
        """Go back to main menu"""
        self.app.pop_screen()

    def action_toggle_theme(self):
        """Toggle between light and dark themes"""
        if ENHANCED_FEATURES_AVAILABLE:
            from .animated_components import ThemeManager
            theme_manager = ThemeManager()
            theme_manager.toggle_theme()
            self.notify(f"🎨 Theme switched to {theme_manager.current_theme.value}")
        else:
            self.notify("⚠️ Theme switching not available")

    def action_show_stats(self):
        """Show real-time statistics"""
        if ENHANCED_FEATURES_AVAILABLE:
            stats_monitor.start_monitoring()
            current_stats = stats_monitor.get_current_system_stats()
            if current_stats:
                self.notify(f"📊 CPU: {current_stats.cpu_percent:.1f}% | Memory: {current_stats.memory_percent:.1f}%")
            else:
                self.notify("📊 Statistics monitoring started")
        else:
            self.notify("⚠️ Statistics monitoring not available")

    def action_install_plugin(self):
        """Show plugin installation dialog"""
        if ENHANCED_FEATURES_AVAILABLE:
            self.notify("🧩 Plugin installation - Use: install-plugin <source>")
        else:
            self.notify("⚠️ Plugin installation not available")

    def action_setup_2fa(self):
        """Setup two-factor authentication"""
        if ENHANCED_FEATURES_AVAILABLE:
            if otp_manager.is_otp_enabled():
                self.notify("🔐 2FA already enabled")
            else:
                self.notify("🔐 Setting up 2FA - Check terminal for QR code")
                # Run setup in background
                import threading
                threading.Thread(target=setup_two_factor_auth, daemon=True).start()
        else:
            self.notify("⚠️ 2FA setup not available")

# Placeholder screens for other menu items
class EnhancedCodeScreen(Screen):
    BINDINGS = [("escape", "back", "Back")]
    def __init__(self, translator): 
        super().__init__()
        self.translator = translator
    def action_back(self): self.app.pop_screen()

class EnhancedFileScreen(Screen):
    BINDINGS = [("escape", "back", "Back")]
    def __init__(self, translator): 
        super().__init__()
        self.translator = translator
    def action_back(self): self.app.pop_screen()

class EnhancedPluginScreen(Screen):
    """Enhanced plugin management screen"""
    BINDINGS = [("escape", "back", "Back"), ("i", "install_plugin", "Install")]

    def __init__(self, translator):
        super().__init__()
        self.translator = translator

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("🧩 Plugin Manager", id="title"),
            Static("Available Commands:", classes="section-title"),
            Static("• install-plugin <source> - Install from GitHub/PyPI/Local"),
            Static("• remove-plugin <name> - Uninstall plugin"),
            Static("• list-plugins - Show installed plugins"),
            Static("• update-plugin <name> - Update plugin"),
            Static(""),
            Static("Examples:", classes="section-title"),
            Static("• install-plugin user/repo - From GitHub"),
            Static("• install-plugin package-name - From PyPI"),
            Static("• install-plugin ./local/path - From local directory"),
            id="main-container"
        )
        yield Footer()

    def action_back(self):
        self.app.pop_screen()

    def action_install_plugin(self):
        """Show plugin installation prompt"""
        self.notify("🧩 Use command: install-plugin <source>")

class EnhancedStatsScreen(Screen):
    """Real-time statistics monitoring screen"""
    BINDINGS = [("escape", "back", "Back"), ("r", "refresh", "Refresh")]

    def __init__(self, translator):
        super().__init__()
        self.translator = translator
        self.stats_container = None

    def compose(self) -> ComposeResult:
        yield Header()
        self.stats_container = Container(
            Static("📊 Real-Time Statistics", id="title"),
            Static("Loading statistics...", id="stats-content"),
            id="main-container"
        )
        yield self.stats_container
        yield Footer()

    def on_mount(self):
        """Start monitoring when screen mounts"""
        if ENHANCED_FEATURES_AVAILABLE:
            stats_monitor.start_monitoring()
            self.set_interval(2.0, self.update_stats)

    def update_stats(self):
        """Update statistics display"""
        if not ENHANCED_FEATURES_AVAILABLE:
            return

        try:
            current_stats = stats_monitor.get_current_system_stats()
            session_stats = stats_monitor.get_session_summary()

            if current_stats:
                stats_text = f"""
📊 System Resources:
  🔥 CPU Usage: {current_stats.cpu_percent:.1f}%
  🧠 Memory: {current_stats.memory_percent:.1f}% ({self._format_bytes(current_stats.memory_used)}/{self._format_bytes(current_stats.memory_total)})
  💾 Disk: {current_stats.disk_percent:.1f}% ({self._format_bytes(current_stats.disk_used)}/{self._format_bytes(current_stats.disk_total)})
  🌐 Network: ↑{self._format_bytes(current_stats.network_sent)} ↓{self._format_bytes(current_stats.network_recv)}

📈 Session Statistics:
  ⏱️ Uptime: {self._format_duration(session_stats.uptime.total_seconds())}
  ⌨️ Commands: {session_stats.commands_executed}
  📝 Files Edited: {session_stats.files_edited}
  🧩 Plugins Used: {session_stats.plugins_used}
  🤖 AI Interactions: {session_stats.ai_interactions}
  ❌ Errors: {session_stats.errors_encountered}

🎯 Performance:
  📊 Monitoring: Active
  🔄 Update Rate: 2 seconds
  ⚡ Status: {"🟢 Good" if current_stats.cpu_percent < 70 else "🟡 High" if current_stats.cpu_percent < 90 else "🔴 Critical"}
"""
            else:
                stats_text = "📊 Statistics not available - monitoring starting..."

            # Update the stats content
            stats_widget = self.query_one("#stats-content")
            stats_widget.update(stats_text)

        except Exception as e:
            self.notify(f"❌ Error updating stats: {e}")

    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"

    def _format_duration(self, seconds: float) -> str:
        """Format duration to human readable format"""
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            return f"{seconds/60:.0f}m {seconds%60:.0f}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours:.0f}h {minutes:.0f}m"

    def action_back(self):
        self.app.pop_screen()

    def action_refresh(self):
        """Manually refresh statistics"""
        self.update_stats()
        self.notify("📊 Statistics refreshed")
