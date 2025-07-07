#!/usr/bin/env python3
"""
🎨 AION Animated Components
Dynamic and animated UI components for enhanced terminal experience

This module provides:
- Animated icon system with pulse, glow, shake, frame, slide effects
- Dynamic selection menus with arrow key navigation
- Real-time highlighting and visual feedback
- Cross-platform emoji and ASCII fallback support
- Performance-optimized animations for terminal environments
"""

import asyncio
import time
import math
from typing import Dict, List, Tuple, Optional, Callable, Any
from enum import Enum
from dataclasses import dataclass

try:
    from textual.app import ComposeResult
    from textual.widget import Widget
    from textual.widgets import Static, Button, Select, OptionList
    from textual.containers import Container, Horizontal, Vertical
    from textual.reactive import reactive
    from textual.message import Message
    from textual.binding import Binding
    from textual import events
    from rich.text import Text
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False
    # Fallback imports
    from rich.console import Console
    from rich.text import Text
    from rich.panel import Panel

class AnimationType(Enum):
    """Animation types for icons and elements"""
    PULSE = "pulse"
    GLOW = "glow"
    SHAKE = "shake"
    FRAME = "frame"
    SLIDE = "slide"
    BOUNCE = "bounce"
    ROTATE = "rotate"
    ZOOM = "zoom"
    WAVE = "wave"
    ORBIT = "orbit"
    RIPPLE = "ripple"
    WIGGLE = "wiggle"
    FADE = "fade"
    SCALE = "scale"

@dataclass
class AnimatedIcon:
    """Animated icon configuration"""
    icon: str
    fallback: str
    animation: AnimationType
    color: str = "white"
    duration: float = 1.0
    intensity: float = 1.0
    description: str = ""

@dataclass
class SelectionItem:
    """Selection item with animated icon"""
    key: str
    label: str
    icon: AnimatedIcon
    callback: Optional[Callable] = None
    enabled: bool = True

class AnimationEngine:
    """Core animation engine for terminal effects"""
    
    def __init__(self):
        self.console = Console()
        self.animation_cache = {}
        self.current_frame = 0
        self.fps = 10  # Terminal-friendly frame rate
        self.frame_time = 1.0 / self.fps
        
    def get_animation_frame(self, animation: AnimationType, frame: int, intensity: float = 1.0) -> str:
        """Get current animation frame for given animation type"""
        cache_key = f"{animation.value}_{frame}_{intensity}"
        
        if cache_key in self.animation_cache:
            return self.animation_cache[cache_key]
        
        result = self._calculate_animation_frame(animation, frame, intensity)
        self.animation_cache[cache_key] = result
        return result
    
    def _calculate_animation_frame(self, animation: AnimationType, frame: int, intensity: float) -> str:
        """Calculate animation frame based on type"""
        cycle = frame % 20  # 2-second cycle at 10fps
        progress = cycle / 20.0
        
        if animation == AnimationType.PULSE:
            # Pulse effect with brightness variation
            brightness = 0.5 + 0.5 * math.sin(progress * 2 * math.pi)
            return f"[bright_white]" if brightness > 0.7 else f"[white]"
            
        elif animation == AnimationType.GLOW:
            # Glow effect with color cycling
            glow_intensity = 0.3 + 0.7 * (math.sin(progress * 2 * math.pi) + 1) / 2
            if glow_intensity > 0.8:
                return f"[bold bright_yellow]"
            elif glow_intensity > 0.6:
                return f"[bright_yellow]"
            else:
                return f"[yellow]"
                
        elif animation == AnimationType.SHAKE:
            # Shake effect with position variation
            shake_positions = ["", " ", "  ", " ", ""]
            return shake_positions[cycle % len(shake_positions)]
            
        elif animation == AnimationType.BOUNCE:
            # Bounce effect with vertical movement simulation
            bounce_height = abs(math.sin(progress * 2 * math.pi))
            if bounce_height > 0.7:
                return "[bold]"
            else:
                return ""
                
        elif animation == AnimationType.ROTATE:
            # Rotation effect with character cycling
            rotate_chars = ["◐", "◓", "◑", "◒"]
            return rotate_chars[cycle % len(rotate_chars)]
            
        elif animation == AnimationType.ZOOM:
            # Zoom effect with size variation
            zoom_level = 0.5 + 0.5 * math.sin(progress * 2 * math.pi)
            return "[bold]" if zoom_level > 0.6 else ""
            
        elif animation == AnimationType.WAVE:
            # Wave effect with flowing motion
            wave_phase = math.sin(progress * 4 * math.pi)
            return "[italic]" if wave_phase > 0 else ""
            
        elif animation == AnimationType.ORBIT:
            # Orbit effect with circular motion simulation
            orbit_chars = ["○", "◔", "◑", "◕", "●", "◕", "◑", "◔"]
            return orbit_chars[cycle % len(orbit_chars)]
            
        elif animation == AnimationType.RIPPLE:
            # Ripple effect with expanding circles
            ripple_chars = ["·", "○", "◯", "⭕", "◯", "○", "·", " "]
            return ripple_chars[cycle % len(ripple_chars)]
            
        elif animation == AnimationType.WIGGLE:
            # Wiggle effect with subtle movement
            wiggle_positions = ["", "~", "", "~"]
            return wiggle_positions[cycle % len(wiggle_positions)]
            
        elif animation == AnimationType.FADE:
            # Fade effect with opacity variation
            fade_level = math.sin(progress * 2 * math.pi)
            if fade_level > 0.5:
                return "[bright_white]"
            elif fade_level > 0:
                return "[white]"
            else:
                return "[dim]"
                
        elif animation == AnimationType.SCALE:
            # Scale effect with size pulsing
            scale_level = 0.7 + 0.3 * math.sin(progress * 2 * math.pi)
            return "[bold]" if scale_level > 0.8 else ""
            
        else:
            return ""

class AnimatedSelector:
    """Animated selection component with arrow key navigation"""
    
    def __init__(self, items: List[SelectionItem], title: str = "Select Option"):
        self.items = items
        self.title = title
        self.selected_index = 0
        self.animation_engine = AnimationEngine()
        self.console = Console()
        self.is_active = False
        self.frame_counter = 0
        
    def render_item(self, item: SelectionItem, is_selected: bool, frame: int) -> str:
        """Render a single selection item with animation"""
        # Get animation frame
        animation_style = self.animation_engine.get_animation_frame(
            item.icon.animation, frame, item.icon.intensity
        )
        
        # Build the display string
        icon_display = item.icon.icon if self._supports_emoji() else item.icon.fallback
        
        # Apply selection highlighting
        if is_selected:
            prefix = "► "
            style_start = f"[bold {item.icon.color}]{animation_style}"
            style_end = "[/]"
            background = "[on blue]"
        else:
            prefix = "  "
            style_start = f"[{item.icon.color}]"
            style_end = "[/]"
            background = ""
        
        # Combine all elements
        display_text = f"{background}{prefix}{style_start}{icon_display}{style_end} {item.label}{background and '[/]' or ''}"
        
        return display_text
    
    def render_full_menu(self) -> str:
        """Render the complete animated menu"""
        lines = []
        lines.append(f"[bold cyan]{self.title}[/bold cyan]")
        lines.append("")
        
        for i, item in enumerate(self.items):
            if not item.enabled:
                continue
                
            is_selected = (i == self.selected_index)
            rendered_item = self.render_item(item, is_selected, self.frame_counter)
            lines.append(rendered_item)
        
        lines.append("")
        lines.append("[dim]Use ↑↓ arrows to navigate, Enter to select, Esc to cancel[/dim]")
        
        return "\n".join(lines)
    
    def move_selection(self, direction: int):
        """Move selection up (-1) or down (1)"""
        enabled_items = [i for i, item in enumerate(self.items) if item.enabled]
        if not enabled_items:
            return
            
        current_pos = enabled_items.index(self.selected_index) if self.selected_index in enabled_items else 0
        new_pos = (current_pos + direction) % len(enabled_items)
        self.selected_index = enabled_items[new_pos]
    
    def get_selected_item(self) -> Optional[SelectionItem]:
        """Get currently selected item"""
        if 0 <= self.selected_index < len(self.items):
            return self.items[self.selected_index]
        return None
    
    def _supports_emoji(self) -> bool:
        """Check if terminal supports emoji"""
        try:
            # Simple test - try to encode emoji
            "🧠".encode('utf-8')
            return True
        except:
            return False

# Predefined animated icons for common AION elements
AI_PROVIDER_ICONS = {
    "openai": AnimatedIcon("🧠", "[AI]", AnimationType.PULSE, "bright_blue", 1.5, 1.0, "OpenAI GPT Models"),
    "deepseek": AnimatedIcon("🛰️", "[DS]", AnimationType.ORBIT, "bright_cyan", 2.0, 0.8, "DeepSeek AI Models"),
    "google": AnimatedIcon("🌐", "[GG]", AnimationType.RIPPLE, "bright_green", 1.8, 0.9, "Google Gemini"),
    "openrouter": AnimatedIcon("🛤️", "[OR]", AnimationType.SLIDE, "bright_magenta", 1.2, 1.0, "OpenRouter Gateway"),
    "anthropic": AnimatedIcon("🤖", "[AN]", AnimationType.GLOW, "bright_yellow", 1.6, 0.7, "Anthropic Claude"),
}

LANGUAGE_ICONS = {
    "en": AnimatedIcon("🇬🇧", "[EN]", AnimationType.SCALE, "bright_white", 1.0, 1.0, "English"),
    "ar": AnimatedIcon("🇮🇶", "[AR]", AnimationType.BOUNCE, "bright_yellow", 1.4, 0.8, "Arabic (Iraq)"),
    "no": AnimatedIcon("🇳🇴", "[NO]", AnimationType.WIGGLE, "bright_blue", 1.2, 0.9, "Norwegian"),
    "de": AnimatedIcon("🇩🇪", "[DE]", AnimationType.FADE, "bright_red", 1.3, 0.7, "German"),
    "fr": AnimatedIcon("🇫🇷", "[FR]", AnimationType.WAVE, "bright_blue", 1.5, 0.8, "French"),
    "es": AnimatedIcon("🇪🇸", "[ES]", AnimationType.ROTATE, "bright_red", 1.1, 0.9, "Spanish"),
    "zh": AnimatedIcon("🇨🇳", "[ZH]", AnimationType.ZOOM, "bright_red", 1.7, 1.0, "Chinese"),
}

SYSTEM_ICONS = {
    "security_high": AnimatedIcon("🔒", "[SEC]", AnimationType.PULSE, "bright_green", 1.0, 1.0, "High Security"),
    "security_medium": AnimatedIcon("🔓", "[MED]", AnimationType.GLOW, "bright_yellow", 1.2, 0.8, "Medium Security"),
    "security_low": AnimatedIcon("⚠️", "[LOW]", AnimationType.SHAKE, "bright_red", 0.8, 1.0, "Low Security"),
    "plugin_manager": AnimatedIcon("🧩", "[PLG]", AnimationType.BOUNCE, "bright_magenta", 1.3, 0.9, "Plugin Manager"),
    "file_explorer": AnimatedIcon("📁", "[FILE]", AnimationType.SLIDE, "bright_cyan", 1.1, 0.8, "File Explorer"),
    "settings": AnimatedIcon("⚙️", "[SET]", AnimationType.ROTATE, "bright_white", 1.4, 0.7, "Settings"),
    "terminal": AnimatedIcon("💻", "[TERM]", AnimationType.RIPPLE, "bright_green", 1.2, 0.9, "Terminal"),
}

class AnimatedMenuManager:
    """Manager for animated menus and selections"""

    def __init__(self):
        self.console = Console()
        self.animation_engine = AnimationEngine()
        self.active_selector = None
        self.animation_task = None

    async def show_ai_provider_selection(self, available_providers: List[str]) -> Optional[str]:
        """Show animated AI provider selection menu"""
        items = []
        for provider in available_providers:
            if provider in AI_PROVIDER_ICONS:
                icon = AI_PROVIDER_ICONS[provider]
                items.append(SelectionItem(provider, icon.description, icon))

        selector = AnimatedSelector(items, "🤖 Select AI Provider")
        return await self._run_selector(selector)

    async def show_language_selection(self, available_languages: List[str]) -> Optional[str]:
        """Show animated language selection menu"""
        items = []
        for lang in available_languages:
            if lang in LANGUAGE_ICONS:
                icon = LANGUAGE_ICONS[lang]
                items.append(SelectionItem(lang, icon.description, icon))

        selector = AnimatedSelector(items, "🌐 Select Language")
        return await self._run_selector(selector)

    async def show_security_level_selection(self) -> Optional[str]:
        """Show animated security level selection menu"""
        items = [
            SelectionItem("high", "High Security", SYSTEM_ICONS["security_high"]),
            SelectionItem("medium", "Medium Security", SYSTEM_ICONS["security_medium"]),
            SelectionItem("low", "Low Security", SYSTEM_ICONS["security_low"]),
        ]

        selector = AnimatedSelector(items, "🔐 Select Security Level")
        return await self._run_selector(selector)

    async def show_main_menu(self) -> Optional[str]:
        """Show animated main menu"""
        items = [
            SelectionItem("ai", "AI Assistant", AI_PROVIDER_ICONS["openai"]),
            SelectionItem("code", "Code Execution", SYSTEM_ICONS["terminal"]),
            SelectionItem("files", "File Manager", SYSTEM_ICONS["file_explorer"]),
            SelectionItem("plugins", "Plugin Manager", SYSTEM_ICONS["plugin_manager"]),
            SelectionItem("settings", "Settings", SYSTEM_ICONS["settings"]),
        ]

        selector = AnimatedSelector(items, "🎯 AION Main Menu")
        return await self._run_selector(selector)

    async def _run_selector(self, selector: AnimatedSelector) -> Optional[str]:
        """Run an animated selector with keyboard input"""
        selector.is_active = True

        # Start animation loop
        self.animation_task = asyncio.create_task(self._animation_loop(selector))

        try:
            # Handle keyboard input (simplified for demo)
            # In real implementation, this would use proper keyboard handling
            result = await self._handle_keyboard_input(selector)
            return result
        finally:
            selector.is_active = False
            if self.animation_task:
                self.animation_task.cancel()

    async def _animation_loop(self, selector: AnimatedSelector):
        """Animation loop for updating display"""
        while selector.is_active:
            try:
                # Clear screen and render menu
                self.console.clear()
                menu_display = selector.render_full_menu()
                self.console.print(Panel(menu_display, border_style="bright_blue"))

                # Update frame counter
                selector.frame_counter += 1

                # Wait for next frame
                await asyncio.sleep(selector.animation_engine.frame_time)
            except asyncio.CancelledError:
                break

    async def _handle_keyboard_input(self, selector: AnimatedSelector) -> Optional[str]:
        """Handle keyboard input for selector (simplified demo version)"""
        # This is a simplified version for demonstration
        # Real implementation would use proper keyboard event handling

        # For demo purposes, simulate some selections
        await asyncio.sleep(2)  # Show animation for 2 seconds

        # Return the first enabled item as demo
        for item in selector.items:
            if item.enabled:
                return item.key

        return None
