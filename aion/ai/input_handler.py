#!/usr/bin/env python3
"""
🎯 AION AI Input Handler

Universal AI input handler that can be embedded into any AION screen
for contextual AI assistance.

Features:
- Universal key bindings (/, ?, Alt+A)
- Context-aware AI responses
- Real-time input processing
- Seamless screen integration
"""

import asyncio
from typing import Optional, Callable, Any
from textual.widgets import Input, Static
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual import events
from rich.text import Text

from aion.ai.contextual_assistant import contextual_ai

class AIInputBar(Container):
    """AI input bar widget for contextual assistance"""
    
    show_input = reactive(False)
    
    def __init__(self, screen_type: str, **kwargs):
        super().__init__(**kwargs)
        self.screen_type = screen_type
        self.ai_input: Optional[Input] = None
        self.ai_response: Optional[Static] = None
        
    def compose(self):
        """Compose AI input bar"""
        with Container(id="ai-input-container", classes="ai-input-hidden"):
            yield Static("🤖 AI Assistant:", id="ai-prompt")
            yield Input(placeholder="Ask me anything about this screen...", id="ai-input")
            yield Static("", id="ai-response")
    
    def on_mount(self):
        """Initialize AI input bar"""
        self.ai_input = self.query_one("#ai-input", Input)
        self.ai_response = self.query_one("#ai-response", Static)
        
        # Set context for AI assistant
        contextual_ai.set_context(self.screen_type)
    
    async def show_ai_input(self, trigger_key: str = "/"):
        """Show AI input bar"""
        container = self.query_one("#ai-input-container")
        container.remove_class("ai-input-hidden")
        container.add_class("ai-input-visible")
        
        if self.ai_input:
            self.ai_input.focus()
            
        # Show context tip
        tip = await contextual_ai.provide_screen_tips(self.screen_type)
        if self.ai_response:
            self.ai_response.update(tip)
    
    async def hide_ai_input(self):
        """Hide AI input bar"""
        container = self.query_one("#ai-input-container")
        container.remove_class("ai-input-visible")
        container.add_class("ai-input-hidden")
        
        if self.ai_input:
            self.ai_input.value = ""
        if self.ai_response:
            self.ai_response.update("")
    
    async def on_input_submitted(self, event: Input.Submitted):
        """Handle AI input submission"""
        if event.input.id == "ai-input":
            query = event.input.value.strip()
            if query:
                # Show loading
                if self.ai_response:
                    self.ai_response.update("🤖 Thinking...")
                
                # Get AI response
                response = await contextual_ai.handle_ai_query(query)
                
                # Display response
                if self.ai_response:
                    self.ai_response.update(response)
                
                # Clear input
                event.input.value = ""

class AIKeyHandler:
    """Universal AI key handler for all screens"""
    
    def __init__(self, screen_instance, screen_type: str):
        self.screen = screen_instance
        self.screen_type = screen_type
        self.ai_input_bar: Optional[AIInputBar] = None
        
    def setup_ai_input(self) -> AIInputBar:
        """Setup AI input bar for screen"""
        self.ai_input_bar = AIInputBar(self.screen_type)
        return self.ai_input_bar
    
    async def handle_key_event(self, event: events.Key) -> bool:
        """Handle AI activation keys"""
        # Forward slash (/) - Quick AI help
        if event.key == "/":
            if self.ai_input_bar:
                await self.ai_input_bar.show_ai_input("/")
                return True
        
        # Question mark (?) - Context help
        elif event.key == "?":
            if self.ai_input_bar:
                await self.ai_input_bar.show_ai_input("?")
                # Pre-fill with context question
                if self.ai_input_bar.ai_input:
                    self.ai_input_bar.ai_input.value = "What can I do on this screen?"
                return True
        
        # Alt+A - AI assistant
        elif event.key == "ctrl+a":  # Using Ctrl+A as Alt+A alternative
            if self.ai_input_bar:
                await self.ai_input_bar.show_ai_input("Alt+A")
                return True
        
        # Escape - Hide AI input
        elif event.key == "escape":
            if self.ai_input_bar and self.ai_input_bar.show_input:
                await self.ai_input_bar.hide_ai_input()
                return True
        
        return False
    
    def update_context(self, file_path: Optional[str] = None, action: str = "", screen_data: dict = None):
        """Update AI context"""
        contextual_ai.set_context(
            self.screen_type, 
            file_path=file_path, 
            action=action, 
            screen_data=screen_data or {}
        )

class AIScreenMixin:
    """Mixin class to add AI capabilities to any screen"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ai_handler: Optional[AIKeyHandler] = None
        self.ai_input_bar: Optional[AIInputBar] = None
    
    def setup_ai_assistance(self, screen_type: str):
        """Setup AI assistance for screen"""
        self.ai_handler = AIKeyHandler(self, screen_type)
        self.ai_input_bar = self.ai_handler.setup_ai_input()
        return self.ai_input_bar
    
    async def on_key(self, event: events.Key) -> None:
        """Handle key events for AI assistance"""
        if self.ai_handler:
            handled = await self.ai_handler.handle_key_event(event)
            if handled:
                event.prevent_default()
                return
        
        # Call parent key handler if not handled by AI
        if hasattr(super(), 'on_key'):
            await super().on_key(event)
    
    def update_ai_context(self, file_path: Optional[str] = None, action: str = "", screen_data: dict = None):
        """Update AI context"""
        if self.ai_handler:
            self.ai_handler.update_context(file_path, action, screen_data)

# CSS for AI input bar styling
AI_INPUT_CSS = """
#ai-input-container {
    height: auto;
    background: $surface;
    border: solid $primary;
    margin: 1;
    padding: 1;
}

.ai-input-hidden {
    display: none;
}

.ai-input-visible {
    display: block;
}

#ai-prompt {
    color: $primary;
    text-style: bold;
}

#ai-input {
    margin: 1 0;
}

#ai-response {
    color: $text;
    background: $surface-lighten-1;
    padding: 1;
    margin: 1 0;
    border-radius: 1;
}
"""
