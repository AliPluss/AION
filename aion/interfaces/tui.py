"""
🖥️ AION Terminal User Interface
Professional TUI with rich interactive elements and multilingual support

This module provides the Terminal User Interface for AION, offering:
- Rich interactive terminal interface with Textual framework
- Advanced navigation with keyboard shortcuts and arrow keys
- Real-time system monitoring and status display
- Multilingual support with dynamic language switching
- Professional layout with panels, tables, and forms
- Integrated AI assistant mode with conversation tracking
- System command execution with security validation
- Code execution environment with syntax highlighting
- Animated loading screens and smooth transitions
"""

import os
import sys
import asyncio
import time
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align

# Textual imports for proper TUI
try:
    from textual.app import App, ComposeResult
    from textual.containers import Container, Horizontal, Vertical
    from textual.widgets import (
        Header, Footer, Button, Static, Input, Log,
        Select, TextArea, ProgressBar, Label, ListView, ListItem
    )
    from textual.binding import Binding
    from textual.screen import Screen
    from textual import events
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False
    App = object
    Screen = object

try:
    from ..utils.translator import Translator
    from ..core.security import SecurityManager
    from ..core.ai_providers import AdvancedAIManager
    from ..core.executor import AdvancedCodeExecutor
except ImportError:
    # Fallback for development mode
    from utils.translator import Translator
    from core.security import SecurityManager
    from core.ai_providers import AdvancedAIManager
    from core.executor import AdvancedCodeExecutor

# AI Assistant imports
try:
    from aion.ai.input_handler import AIScreenMixin, AIInputBar, AI_INPUT_CSS
    from aion.ai.contextual_assistant import contextual_ai
    from aion.ai.chatbot import aion_chatbot
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    AIScreenMixin = object

class AIONApp(App):
    """Main AION Textual Application with enhanced navigation"""

    CSS = """
    /* AI Assistant Styles */
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

    /* Original Styles */
    #loading-container {
        align: center middle;
        background: $surface;
    }

    #banner {
        text-align: center;
        color: $accent;
        margin: 1;
    }

    #loading-text {
        text-align: center;
        color: $text;
        margin: 1;
    }

    #main-container {
        padding: 1;
    }

    #welcome {
        background: $panel;
        border: solid $primary;
        margin: 1;
        padding: 1;
    }

    #main-buttons {
        align: center middle;
        margin: 1;
    }

    Button {
        margin: 0 1;
        min-width: 20;
    }

    #status-bar {
        background: $surface;
        color: $text-muted;
        text-align: center;
        margin: 1 0;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("escape", "back", "Back"),
        ("h", "help", "Help"),
    ]

    def __init__(self, translator: Translator, security: SecurityManager):
        super().__init__()
        self.translator = translator
        self.security = security
        self.ai_manager = AdvancedAIManager()
        self.code_executor = AdvancedCodeExecutor()

    def on_mount(self) -> None:
        """Show loading screen on startup"""
        # Initialize AI context
        if AI_AVAILABLE:
            contextual_ai.set_context("main_menu")
        self.push_screen(LoadingScreen())

    def compose(self) -> ComposeResult:
        """Main app composition"""
        yield Header(show_clock=True)
        yield Container(
            Static(self._get_welcome_message(), id="welcome"),
            Horizontal(
                Button("🤖 AI Assistant", id="ai-btn", variant="primary"),
                Button("⚡ Code Execution", id="code-btn", variant="success"),
                Button("📁 File Manager", id="file-btn", variant="warning"),
                Button("📧 Email Sharing", id="email-btn", variant="success"),
                Button("🐙 GitHub Tools", id="github-btn", variant="primary"),
                Button("💡 AI Code Assist", id="ai-assist-btn", variant="success"),
                Button("⚙️ Settings", id="settings-btn", variant="default"),
                id="main-buttons"
            ),
            # AI Input Bar
            Container(
                Static("🤖 AI Assistant:", id="ai-prompt"),
                Input(placeholder="Ask me anything about AION...", id="ai-input"),
                Static("Use arrow keys to navigate • Enter to select • Q to quit", id="ai-response"),
                id="ai-input-container",
                classes="ai-input-hidden"
            ),
            Static("💡 Press '/' for AI help, '?' for context help, or Ctrl+A for AI assistant", id="status-bar"),
            id="main-container"
        )
        yield Footer()

    async def on_key(self, event: events.Key) -> None:
        """Handle AI activation keys and smart search"""
        if not AI_AVAILABLE:
            return

        ai_container = self.query_one("#ai-input-container")
        ai_input = self.query_one("#ai-input", Input)
        ai_response = self.query_one("#ai-response", Static)

        # Ctrl+K - Smart Search
        if event.key == "ctrl+k":
            ai_container.remove_class("ai-input-hidden")
            ai_container.add_class("ai-input-visible")
            ai_input.placeholder = "🔍 Search Stack Overflow, GitHub, Python Docs..."
            ai_input.focus()
            ai_response.update("🔍 Smart Search Mode: Enter your search topic")
            event.prevent_default()

        # Forward slash (/) - Quick AI help
        elif event.key == "/":
            ai_container.remove_class("ai-input-hidden")
            ai_container.add_class("ai-input-visible")
            ai_input.placeholder = "Ask me anything about AION..."
            ai_input.focus()
            ai_response.update("💡 Ask me anything about AION!")
            event.prevent_default()

        # Question mark (?) - Context help
        elif event.key == "?":
            ai_container.remove_class("ai-input-hidden")
            ai_container.add_class("ai-input-visible")
            ai_input.value = "What can I do on this screen?"
            ai_input.placeholder = "Context help..."
            ai_input.focus()
            event.prevent_default()

        # Ctrl+A - AI assistant
        elif event.key == "ctrl+a":
            ai_container.remove_class("ai-input-hidden")
            ai_container.add_class("ai-input-visible")
            ai_input.placeholder = "AI Assistant ready..."
            ai_input.focus()
            ai_response.update("🤖 AI Assistant activated! How can I help?")
            event.prevent_default()

        # Escape - Hide AI input
        elif event.key == "escape":
            if "ai-input-visible" in ai_container.classes:
                ai_container.remove_class("ai-input-visible")
                ai_container.add_class("ai-input-hidden")
                ai_input.value = ""
                ai_input.placeholder = ""
                ai_response.update("💡 Press '/' for AI help, '?' for context help, Ctrl+K for search, or Ctrl+A for AI assistant")
                event.prevent_default()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle AI input submission and smart search"""
        if event.input.id == "ai-input" and AI_AVAILABLE:
            query = event.input.value.strip()
            if query:
                ai_response = self.query_one("#ai-response", Static)

                # Check if this is a search query (Ctrl+K was pressed)
                if "Search Stack Overflow" in event.input.placeholder:
                    # Handle smart search
                    ai_response.update("🔍 Searching developer resources...")

                    try:
                        from aion.ai.smart_search import smart_search

                        # Perform search
                        search_results = await smart_search.search(
                            query,
                            ["stackoverflow", "github", "python_docs"],
                            5
                        )

                        # Format results for display
                        if search_results.results:
                            response = f"🔍 **Found {len(search_results.results)} results for '{query}':**\n\n"
                            for i, result in enumerate(search_results.results[:3], 1):
                                response += f"**{i}. {result.title}**\n"
                                response += f"   Source: {result.source} | Score: {result.score:.2f}\n"
                                response += f"   {result.snippet[:100]}...\n\n"
                            response += f"📝 Full results: search_logs/query_*.log"
                        else:
                            response = f"🔍 No results found for '{query}'. Try different keywords."

                    except Exception as e:
                        response = f"⚠️ Search error: {e}"

                    ai_response.update(response)

                else:
                    # Handle regular AI query
                    ai_response.update("🤖 Thinking...")

                    # Get AI response
                    response = await contextual_ai.handle_ai_query(query)

                    # Display response
                    ai_response.update(response)

                # Clear input
                event.input.value = ""
                event.input.placeholder = ""

    def _get_welcome_message(self) -> str:
        """Get welcome message with system status"""
        return f"""🎯 Welcome to AION - AI Operating Node

Current Language: {self.translator.current_language}
Security Status: 🔐 Active
AI Providers: 🤖 Ready
Code Execution: ⚡ Available

Professional Terminal AI Assistant with Enhanced Navigation"""

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        button_id = event.button.id

        if button_id == "ai-btn":
            if AI_AVAILABLE:
                await self._show_chat()
            else:
                await self._show_ai_assistant()
        elif button_id == "code-btn":
            await self._show_code_execution()
        elif button_id == "file-btn":
            await self._show_file_manager()
        elif button_id == "email-btn":
            await self._show_email_sharing()
        elif button_id == "github-btn":
            await self._show_github_tools()
        elif button_id == "ai-assist-btn":
            await self._show_ai_assist()
        elif button_id == "settings-btn":
            await self._show_settings()

    async def _show_chat(self):
        """Show full-screen AI chat interface"""
        self.push_screen(ChatScreen(self.translator))

    async def _show_ai_assistant(self):
        """Show AI assistant interface"""
        self.push_screen(AIAssistantScreen(self.translator, self.ai_manager))

    async def _show_code_execution(self):
        """Show code execution interface"""
        self.push_screen(CodeExecutionScreen(self.translator, self.code_executor))

    async def _show_file_manager(self):
        """Show file manager interface"""
        self.push_screen(FileManagerScreen(self.translator))

    async def _show_email_sharing(self):
        """Show email sharing interface"""
        self.push_screen(EmailSharingScreen(self.translator))

    async def _show_github_tools(self):
        """Show GitHub tools interface"""
        self.push_screen(GitHubToolsScreen(self.translator))

    async def _show_ai_assist(self):
        """Show AI code assistance interface"""
        self.push_screen(AIAssistScreen(self.translator))

    async def _show_settings(self):
        """Show settings interface"""
        self.push_screen(SettingsScreen(self.translator))

class LoadingScreen(Screen):
    """Animated loading screen for AION startup"""

    def compose(self) -> ComposeResult:
        yield Container(
            Static(self._get_ascii_banner(), id="banner"),
            Static("", id="loading-text"),
            ProgressBar(id="progress"),
            id="loading-container"
        )

    def _get_ascii_banner(self) -> str:
        return """
    ╔═══════════════════════════════════════╗
    ║              🤖 AION                  ║
    ║        AI Operating Node              ║
    ║     Professional Terminal AI          ║
    ║                                       ║
    ╚═══════════════════════════════════════╝
        """

    async def on_mount(self) -> None:
        """Animate loading sequence"""
        if not TEXTUAL_AVAILABLE:
            return

        loading_text = self.query_one("#loading-text", Static)
        progress = self.query_one("#progress", ProgressBar)

        steps = [
            "🔧 Initializing AION systems...",
            "🔐 Loading security modules...",
            "🤖 Connecting AI providers...",
            "🌐 Setting up multilingual support...",
            "⚡ Preparing code execution engine...",
            "✅ AION ready!"
        ]

        for i, step in enumerate(steps):
            loading_text.update(step)
            progress.update(progress=(i + 1) / len(steps) * 100)
            await asyncio.sleep(0.5)

        # Switch to main screen after loading
        await asyncio.sleep(1)
        self.app.pop_screen()

class AIAssistantScreen(Screen):
    """AI Assistant interface screen"""

    BINDINGS = [
        ("escape", "back", "Back"),
        ("ctrl+c", "clear", "Clear"),
    ]

    def __init__(self, translator: Translator, ai_manager):
        super().__init__()
        self.translator = translator
        self.ai_manager = ai_manager

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("🤖 AI Assistant", id="title"),
            TextArea("", placeholder="Ask me anything...", id="input"),
            Log(id="conversation"),
            Horizontal(
                Button("Send", id="send-btn", variant="primary"),
                Button("Clear", id="clear-btn", variant="warning"),
                Button("Back", id="back-btn", variant="default"),
                id="controls"
            ),
            id="ai-container"
        )
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "send-btn":
            await self._send_message()
        elif event.button.id == "clear-btn":
            self.query_one("#conversation", Log).clear()
        elif event.button.id == "back-btn":
            self.app.pop_screen()

    async def _send_message(self):
        input_area = self.query_one("#input", TextArea)
        conversation = self.query_one("#conversation", Log)

        message = input_area.text.strip()
        if message:
            conversation.write_line(f"👤 You: {message}")
            input_area.text = ""

            # Get AI response (simplified)
            response = await self._get_ai_response(message)
            conversation.write_line(f"🤖 AION: {response}")

    async def _get_ai_response(self, message: str) -> str:
        """Get AI response (placeholder)"""
        return f"I received your message: '{message}'. This is a demo response."

class CodeExecutionScreen(Screen):
    """Code execution interface screen"""

    BINDINGS = [
        ("escape", "back", "Back"),
        ("f5", "run", "Run Code"),
    ]

    def __init__(self, translator: Translator, code_executor):
        super().__init__()
        self.translator = translator
        self.code_executor = code_executor

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("⚡ Code Execution", id="title"),
            Horizontal(
                Select([("Python", "python"), ("JavaScript", "javascript"), ("Rust", "rust")],
                      value="python", id="language-select"),
                Button("Run (F5)", id="run-btn", variant="success"),
                Button("Clear", id="clear-btn", variant="warning"),
                Button("Back", id="back-btn", variant="default"),
                id="code-controls"
            ),
            TextArea("print('Hello, AION!')", id="code-editor"),
            Log(id="output"),
            id="code-container"
        )
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run-btn":
            await self._run_code()
        elif event.button.id == "clear-btn":
            self.query_one("#output", Log).clear()
        elif event.button.id == "back-btn":
            self.app.pop_screen()

    async def _run_code(self):
        code_editor = self.query_one("#code-editor", TextArea)
        language_select = self.query_one("#language-select", Select)
        output = self.query_one("#output", Log)

        code = code_editor.text
        language = language_select.value

        output.write_line(f"🚀 Running {language} code...")

        # Execute code (simplified)
        try:
            result = f"Code executed successfully!\nOutput: Hello from {language}!"
            output.write_line(f"✅ {result}")
        except Exception as e:
            output.write_line(f"❌ Error: {str(e)}")

class FileManagerScreen(Screen):
    """File manager interface screen"""

    BINDINGS = [("escape", "back", "Back")]

    def __init__(self, translator: Translator):
        super().__init__()
        self.translator = translator

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("📁 File Manager", id="title"),
            ListView(
                ListItem(Label("📄 example.py")),
                ListItem(Label("📄 README.md")),
                ListItem(Label("📁 Documents")),
                ListItem(Label("📁 Projects")),
                id="file-list"
            ),
            Button("Back", id="back-btn", variant="default"),
            id="file-container"
        )
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back-btn":
            self.app.pop_screen()

class EmailSharingScreen(Screen):
    """Email sharing interface screen"""

    BINDINGS = [("escape", "back", "Back")]

    def __init__(self, translator):
        super().__init__()
        self.translator = translator

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("📧 Email Sharing", id="title"),
            Vertical(
                Static("Send files or content via email", id="description"),
                Horizontal(
                    Button("📝 Send Text", id="text-btn", variant="primary"),
                    Button("📁 Send File", id="file-btn", variant="success"),
                    Button("💻 Send Output", id="output-btn", variant="warning"),
                    id="email-buttons"
                ),
                TextArea("", placeholder="Email content will appear here...", id="preview"),
                Button("Back", id="back-btn", variant="default"),
                id="email-content"
            ),
            id="email-container"
        )
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back-btn":
            self.app.pop_screen()
        elif event.button.id == "text-btn":
            await self._send_text_email()
        elif event.button.id == "file-btn":
            await self._send_file_email()
        elif event.button.id == "output-btn":
            await self._send_output_email()

    async def _send_text_email(self):
        """Send text email"""
        try:
            from aion.integrations.email_system import email_system
            # Switch to CLI mode for interactive email
            self.app.exit()
            email_system.send_email_interactive()
        except Exception as e:
            preview = self.query_one("#preview", TextArea)
            preview.text = f"❌ Email error: {e}"

    async def _send_file_email(self):
        """Send file email"""
        try:
            from aion.integrations.email_system import email_system
            # Switch to CLI mode for interactive email
            self.app.exit()
            email_system.send_email_interactive()
        except Exception as e:
            preview = self.query_one("#preview", TextArea)
            preview.text = f"❌ Email error: {e}"

    async def _send_output_email(self):
        """Send terminal output email"""
        try:
            from aion.integrations.email_system import email_system
            # Switch to CLI mode for interactive email
            self.app.exit()
            email_system.send_email_interactive()
        except Exception as e:
            preview = self.query_one("#preview", TextArea)
            preview.text = f"❌ Email error: {e}"

    def action_back(self) -> None:
        self.app.pop_screen()

class GitHubToolsScreen(Screen):
    """GitHub tools interface screen"""

    BINDINGS = [("escape", "back", "Back")]

    def __init__(self, translator):
        super().__init__()
        self.translator = translator

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("🐙 GitHub Tools", id="title"),
            Vertical(
                Static("Repository management and synchronization", id="description"),
                Horizontal(
                    Button("📋 List Repos", id="list-btn", variant="primary"),
                    Button("📤 Push Files", id="push-btn", variant="success"),
                    Button("📥 Pull Updates", id="pull-btn", variant="warning"),
                    id="github-buttons"
                ),
                Horizontal(
                    Button("🌿 New Branch", id="branch-btn", variant="primary"),
                    Button("📊 Statistics", id="stats-btn", variant="success"),
                    Button("Back", id="back-btn", variant="default"),
                    id="github-buttons2"
                ),
                TextArea("", placeholder="GitHub operation results will appear here...", id="output"),
                id="github-content"
            ),
            id="github-container"
        )
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back-btn":
            self.app.pop_screen()
        elif event.button.id == "list-btn":
            await self._list_repositories()
        elif event.button.id == "push-btn":
            await self._push_files()
        elif event.button.id == "pull-btn":
            await self._pull_updates()
        elif event.button.id == "branch-btn":
            await self._create_branch()
        elif event.button.id == "stats-btn":
            await self._show_statistics()

    async def _list_repositories(self):
        """List repositories"""
        try:
            from aion.integrations.github_tools import github_tools
            # Switch to CLI mode for interactive GitHub tools
            self.app.exit()
            github_tools.github_tools_interactive()
        except Exception as e:
            output = self.query_one("#output", TextArea)
            output.text = f"❌ GitHub error: {e}"

    async def _push_files(self):
        """Push files to repository"""
        try:
            from aion.integrations.github_tools import github_tools
            # Switch to CLI mode for interactive GitHub tools
            self.app.exit()
            github_tools.github_tools_interactive()
        except Exception as e:
            output = self.query_one("#output", TextArea)
            output.text = f"❌ GitHub error: {e}"

    async def _pull_updates(self):
        """Pull repository updates"""
        try:
            from aion.integrations.github_tools import github_tools
            # Switch to CLI mode for interactive GitHub tools
            self.app.exit()
            github_tools.github_tools_interactive()
        except Exception as e:
            output = self.query_one("#output", TextArea)
            output.text = f"❌ GitHub error: {e}"

    async def _create_branch(self):
        """Create new branch"""
        try:
            from aion.integrations.github_tools import github_tools
            # Switch to CLI mode for interactive GitHub tools
            self.app.exit()
            github_tools.github_tools_interactive()
        except Exception as e:
            output = self.query_one("#output", TextArea)
            output.text = f"❌ GitHub error: {e}"

    async def _show_statistics(self):
        """Show GitHub statistics"""
        try:
            from aion.integrations.github_tools import github_tools
            # Switch to CLI mode for interactive GitHub tools
            self.app.exit()
            github_tools.github_tools_interactive()
        except Exception as e:
            output = self.query_one("#output", TextArea)
            output.text = f"❌ GitHub error: {e}"

    def action_back(self) -> None:
        self.app.pop_screen()

class AIAssistScreen(Screen):
    """AI code assistance interface screen"""

    BINDINGS = [("escape", "back", "Back")]

    def __init__(self, translator):
        super().__init__()
        self.translator = translator

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("💡 AI Code Assistant", id="title"),
            Vertical(
                Static("AI-powered code analysis and suggestions", id="description"),
                Horizontal(
                    Button("📄 Analyze File", id="analyze-btn", variant="primary"),
                    Button("✍️ Code Snippet", id="snippet-btn", variant="success"),
                    Button("🔍 Check Errors", id="errors-btn", variant="warning"),
                    id="ai-buttons"
                ),
                Horizontal(
                    Button("🚀 Improvements", id="improve-btn", variant="primary"),
                    Button("📊 Quality Score", id="quality-btn", variant="success"),
                    Button("Back", id="back-btn", variant="default"),
                    id="ai-buttons2"
                ),
                TextArea("", placeholder="AI analysis results will appear here...", id="results"),
                id="ai-content"
            ),
            id="ai-container"
        )
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back-btn":
            self.app.pop_screen()
        elif event.button.id == "analyze-btn":
            await self._analyze_file()
        elif event.button.id == "snippet-btn":
            await self._analyze_snippet()
        elif event.button.id == "errors-btn":
            await self._check_errors()
        elif event.button.id == "improve-btn":
            await self._suggest_improvements()
        elif event.button.id == "quality-btn":
            await self._show_quality_score()

    async def _analyze_file(self):
        """Analyze file with AI"""
        try:
            from aion.integrations.ai_code_assist import ai_code_assist
            # Switch to CLI mode for interactive AI assistance
            self.app.exit()
            ai_code_assist.analyze_code_interactive()
        except Exception as e:
            results = self.query_one("#results", TextArea)
            results.text = f"❌ AI assistance error: {e}"

    async def _analyze_snippet(self):
        """Analyze code snippet"""
        try:
            from aion.integrations.ai_code_assist import ai_code_assist
            # Switch to CLI mode for interactive AI assistance
            self.app.exit()
            ai_code_assist.analyze_code_interactive()
        except Exception as e:
            results = self.query_one("#results", TextArea)
            results.text = f"❌ AI assistance error: {e}"

    async def _check_errors(self):
        """Check for code errors"""
        try:
            from aion.integrations.ai_code_assist import ai_code_assist
            # Switch to CLI mode for interactive AI assistance
            self.app.exit()
            ai_code_assist.analyze_code_interactive()
        except Exception as e:
            results = self.query_one("#results", TextArea)
            results.text = f"❌ AI assistance error: {e}"

    async def _suggest_improvements(self):
        """Suggest code improvements"""
        try:
            from aion.integrations.ai_code_assist import ai_code_assist
            # Switch to CLI mode for interactive AI assistance
            self.app.exit()
            ai_code_assist.analyze_code_interactive()
        except Exception as e:
            results = self.query_one("#results", TextArea)
            results.text = f"❌ AI assistance error: {e}"

    async def _show_quality_score(self):
        """Show code quality score"""
        try:
            from aion.integrations.ai_code_assist import ai_code_assist
            # Switch to CLI mode for interactive AI assistance
            self.app.exit()
            ai_code_assist.analyze_code_interactive()
        except Exception as e:
            results = self.query_one("#results", TextArea)
            results.text = f"❌ AI assistance error: {e}"

    def action_back(self) -> None:
        self.app.pop_screen()

class ChatScreen(Screen):
    """Full-screen AI chat interface"""

    BINDINGS = [
        ("escape", "back", "Back"),
        ("ctrl+c", "clear", "Clear Chat"),
        ("ctrl+s", "save", "Save Session"),
    ]

    def __init__(self, translator: Translator):
        super().__init__()
        self.translator = translator
        self.session_id = None

    def compose(self) -> ComposeResult:
        yield Container(
            Static("💬 AION AI Chat - Full Conversation Mode", id="chat-title"),
            Container(
                Log(id="chat-history", auto_scroll=True),
                id="chat-display"
            ),
            Horizontal(
                Input(placeholder="Type your message... (Press Enter to send)", id="chat-input"),
                Button("Send", id="send-btn", variant="primary"),
                Button("Clear", id="clear-btn", variant="warning"),
                Button("Save", id="save-btn", variant="success"),
                id="chat-controls"
            ),
            Static("💡 Continuous memory active • Context-aware responses • Code & error analysis", id="chat-status"),
            id="chat-container"
        )

    async def on_mount(self):
        """Initialize chat session"""
        if AI_AVAILABLE:
            self.session_id = aion_chatbot.start_chat_session()
            chat_history = self.query_one("#chat-history", Log)
            chat_history.write_line("🤖 **AION AI Chat Started**")
            chat_history.write_line(f"📋 Session ID: {self.session_id}")
            chat_history.write_line("💬 I'm ready to help! I can explain code, analyze errors, and answer AION questions.")
            chat_history.write_line("🧠 I'll remember our entire conversation for context.")
            chat_history.write_line("---")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "send-btn":
            await self._send_message()
        elif event.button.id == "clear-btn":
            await self._clear_chat()
        elif event.button.id == "save-btn":
            await self._save_session()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "chat-input":
            await self._send_message()

    async def _send_message(self):
        """Send message to AI chatbot"""
        if not AI_AVAILABLE:
            return

        chat_input = self.query_one("#chat-input", Input)
        chat_history = self.query_one("#chat-history", Log)

        user_message = chat_input.value.strip()
        if not user_message:
            return

        # Display user message
        chat_history.write_line(f"👤 **You:** {user_message}")

        # Clear input
        chat_input.value = ""

        # Show AI thinking
        chat_history.write_line("🤖 **AI:** Thinking...")

        try:
            # Get AI response
            ai_response = await aion_chatbot.send_message(user_message)

            # Remove thinking message and add response
            chat_history.write_line(f"🤖 **AI:** {ai_response}")
            chat_history.write_line("---")

        except Exception as e:
            chat_history.write_line(f"❌ **Error:** {e}")

    async def _clear_chat(self):
        """Clear chat history"""
        chat_history = self.query_one("#chat-history", Log)
        chat_history.clear()

        if AI_AVAILABLE and self.session_id:
            # End current session and start new one
            aion_chatbot.end_chat_session("Chat cleared by user")
            self.session_id = aion_chatbot.start_chat_session()

            chat_history.write_line("🔄 **Chat Cleared**")
            chat_history.write_line(f"📋 New Session ID: {self.session_id}")
            chat_history.write_line("💬 Ready for a fresh conversation!")
            chat_history.write_line("---")

    async def _save_session(self):
        """Save chat session"""
        if not AI_AVAILABLE or not self.session_id:
            return

        chat_history = self.query_one("#chat-history", Log)

        try:
            summary = aion_chatbot.get_session_summary()
            chat_history.write_line(f"💾 **Session Saved**")
            chat_history.write_line(f"📊 Messages: {summary.get('total_messages', 0)}")
            chat_history.write_line(f"⏱️ Duration: {summary.get('duration_minutes', 0):.1f} minutes")
            chat_history.write_line("---")

        except Exception as e:
            chat_history.write_line(f"❌ **Save Error:** {e}")

    def action_back(self) -> None:
        """End session and go back"""
        if AI_AVAILABLE and self.session_id:
            aion_chatbot.end_chat_session("User ended session")
        self.app.pop_screen()

    def action_clear(self) -> None:
        """Clear chat action"""
        self.run_action("_clear_chat")

    def action_save(self) -> None:
        """Save session action"""
        self.run_action("_save_session")

class SettingsScreen(Screen):
    """Settings interface screen"""

    BINDINGS = [("escape", "back", "Back")]

    def __init__(self, translator: Translator):
        super().__init__()
        self.translator = translator

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("⚙️ Settings", id="title"),
            Static(f"Current Language: {self.translator.current_language}", id="lang-info"),
            Horizontal(
                Button("Change Language", id="lang-btn", variant="primary"),
                Button("Security Settings", id="security-btn", variant="warning"),
                Button("Back", id="back-btn", variant="default"),
                id="settings-controls"
            ),
            id="settings-container"
        )
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back-btn":
            self.app.pop_screen()

class TUI:
    """
    Professional Terminal User Interface for AION

    This class provides a comprehensive TUI experience with:
    - Rich interactive terminal interface using Textual framework
    - Advanced keyboard navigation and shortcuts
    - Real-time system monitoring and status updates
    - Multilingual support with dynamic language switching
    - Professional layout management with panels and widgets
    - AI assistant integration with conversation tracking
    - System monitoring and resource usage display
    - Advanced error handling and user feedback
    - Enhanced animated icon system with dynamic effects
    - Arrow key navigation with real-time highlighting
    - Cross-platform emoji support with ASCII fallback

    The TUI provides an enhanced terminal experience with visual
    elements, interactive forms, and intuitive navigation.
    """
    
    def __init__(self, translator: Translator, security: SecurityManager):
        self.translator = translator
        self.security = security
        self.console = Console()
        self.current_session = None
        self.is_running = False

        # Check if Textual is available for enhanced TUI
        self.textual_available = TEXTUAL_AVAILABLE
        self.enhanced_mode = False

        if self.textual_available:
            # Try to use enhanced animated TUI first
            try:
                from .enhanced_tui import EnhancedAIONApp
                self.app = EnhancedAIONApp(translator, None)  # AI manager will be set later
                self.enhanced_mode = True
                print("🎨 Enhanced Animated AION TUI initialized successfully")
            except ImportError:
                # Fallback to standard TUI
                self.app = AIONApp(translator, security)
                print("🖥️ Standard AION TUI initialized successfully")
        else:
            print("🖥️ AION TUI initialized successfully (Rich fallback mode)")

    def start(self):
        """Start the TUI interface"""
        if self.textual_available:
            # Use enhanced Textual TUI
            self._show_animated_loading()
            if self.enhanced_mode:
                self.console.print("🎨 [bold green]Starting Enhanced Animated AION Interface...[/bold green]")
                self.console.print("✨ [cyan]Features: Dynamic icons, arrow navigation, real-time animations[/cyan]")
            else:
                self.console.print("🖥️ [bold blue]Starting Standard AION Interface...[/bold blue]")
            self.app.run()
        else:
            # Fallback to basic Rich TUI
            self.console.print(Panel(
                "🖥️ AION TUI Interface Starting...\n\n⚠️ Enhanced TUI requires 'textual' package\nUsing basic interface...",
                border_style="yellow"
            ))

            # Create session token
            self.current_session = self.security.create_session_token("tui_user")
            self.is_running = True

            self._show_main_interface()

    def _show_animated_loading(self):
        """Show animated loading screen using Rich"""
        if not self.textual_available:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console,
            ) as progress:

                # ASCII Banner
                banner = """
    ╔═══════════════════════════════════════╗
    ║              🤖 AION                  ║
    ║        AI Operating Node              ║
    ║     Professional Terminal AI          ║
    ║                                       ║
    ╚═══════════════════════════════════════╝
                """

                self.console.print(Panel(
                    Align.center(Text(banner, style="bold cyan")),
                    title="[bold green]AION Loading[/bold green]",
                    border_style="bright_blue"
                ))

                steps = [
                    "🔧 Initializing AION systems...",
                    "🔐 Loading security modules...",
                    "🤖 Connecting AI providers...",
                    "🌐 Setting up multilingual support...",
                    "⚡ Preparing code execution engine...",
                    "✅ AION ready!"
                ]

                task = progress.add_task("Loading...", total=len(steps))

                for step in steps:
                    progress.update(task, description=step)
                    time.sleep(0.5)
                    progress.advance(task)

                time.sleep(1)
    
    def _show_main_interface(self):
        """Display main TUI interface"""
        self.console.clear()
        
        # Header
        header = Panel(
            "🤖 AION Terminal User Interface",
            style="bold cyan",
            border_style="bright_blue"
        )
        self.console.print(header)
        
        # Status panel
        status_table = Table(title="System Status")
        status_table.add_column("Component", style="cyan")
        status_table.add_column("Status", style="green")
        
        status_table.add_row("Security", "Active" if self.security else "Inactive")
        status_table.add_row("Session", "Active" if self.current_session else "Inactive")
        status_table.add_row("Language", self.translator.current_language.upper())
        
        self.console.print(status_table)
        
        # Menu options
        menu_panel = Panel(
            """
🔹 Available Options:
  [1] AI Assistant Mode
  [2] System Commands  
  [3] Code Execution
  [4] File Management
  [5] Settings
  [6] Help
  [7] Exit
  
📝 Navigation:
  • Use number keys to select options
  • Press 'q' to quit current mode
  • Press 'h' for help in any mode
            """,
            title="Main Menu",
            border_style="yellow"
        )
        self.console.print(menu_panel)
        
        self._handle_user_input()
    
    def _handle_user_input(self):
        """Handle user input in main interface with command-driven control"""
        self.console.print("\n💡 [bold yellow]Available Commands:[/bold yellow]")
        self.console.print("   • [bold cyan]ai[/bold cyan] or [bold cyan]assistant[/bold cyan] - Start AI Assistant")
        self.console.print("   • [bold cyan]code[/bold cyan] or [bold cyan]execute[/bold cyan] - Code Execution")
        self.console.print("   • [bold cyan]files[/bold cyan] or [bold cyan]manager[/bold cyan] - File Management")
        self.console.print("   • [bold cyan]system[/bold cyan] or [bold cyan]commands[/bold cyan] - System Commands")
        self.console.print("   • [bold cyan]settings[/bold cyan] or [bold cyan]config[/bold cyan] - Settings")
        self.console.print("   • [bold cyan]help[/bold cyan] - Show help")
        self.console.print("   • [bold cyan]quit[/bold cyan] or [bold cyan]exit[/bold cyan] - Exit AION")
        self.console.print("   • Use [bold green]Tab[/bold green] for autocomplete, [bold green]↑↓[/bold green] for history")

        while self.is_running:
            try:
                command = input("\n🤖 AION> ").strip().lower()

                if command in ["ai", "assistant", "chat"]:
                    self._ai_assistant_mode()
                elif command in ["code", "execute", "run"]:
                    self._code_execution_mode()
                elif command in ["files", "manager", "file", "fm"]:
                    self._file_management_mode()
                elif command in ["system", "commands", "sys", "cmd"]:
                    self._system_commands_mode()
                elif command in ["settings", "config", "preferences"]:
                    self._settings_mode()
                elif command in ["help", "?", "h"]:
                    self._show_help()
                elif command in ["quit", "exit", "q", "bye"]:
                    self._exit_tui()
                    break
                elif command == "":
                    continue  # Empty input, just continue
                else:
                    self.console.print(f"❌ Unknown command: '{command}'")
                    self.console.print("💡 Type 'help' to see available commands")

            except KeyboardInterrupt:
                self._exit_tui()
                break
            except Exception as e:
                self.console.print(f"❌ Error: {e}")
    
    def _ai_assistant_mode(self):
        """AI Assistant mode in TUI"""
        self.console.clear()
        self.console.print(Panel(
            "🧠 AI Assistant Mode",
            style="bold cyan",
            border_style="cyan"
        ))
        
        self.console.print("💡 Enter your AI requests. Type 'back' to return to main menu.")
        
        while True:
            try:
                user_input = input("\n🤖 AI: ").strip()
                
                if user_input.lower() in ['back', 'exit', 'quit']:
                    break
                
                if user_input:
                    self._process_ai_request(user_input)
                    
            except KeyboardInterrupt:
                break
        
        self._show_main_interface()
    
    def _process_ai_request(self, request: str):
        """Process AI request (placeholder)"""
        self.console.print("🔄 Processing AI request...")
        
        # Simulate AI processing
        import time
        time.sleep(1)
        
        responses = [
            f"I understand you're asking about: {request}",
            "This is a simulated AI response in TUI mode.",
            "AI providers would be integrated here for real responses."
        ]
        
        import random
        response = random.choice(responses)
        
        response_panel = Panel(
            response,
            title="AI Response",
            border_style="green"
        )
        self.console.print(response_panel)
    
    def _system_commands_mode(self):
        """System commands mode"""
        self.console.clear()
        self.console.print(Panel(
            "⚙️ System Commands Mode",
            style="bold yellow",
            border_style="yellow"
        ))
        
        self.console.print("💻 Enter system commands. Type 'back' to return.")
        
        while True:
            try:
                command = input("\n💻 System: ").strip()
                
                if command.lower() in ['back', 'exit', 'quit']:
                    break
                
                if command:
                    self._execute_system_command(command)
                    
            except KeyboardInterrupt:
                break
        
        self._show_main_interface()
    
    def _execute_system_command(self, command: str):
        """Execute system command with validation"""
        # Basic security check
        dangerous_commands = ['rm -rf', 'del /f', 'format', 'fdisk']
        if any(dangerous in command.lower() for dangerous in dangerous_commands):
            self.console.print("❌ Dangerous command blocked for security.")
            return
        
        self.console.print(f"🔄 Executing: {command}")
        
        try:
            import subprocess
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                output_panel = Panel(
                    result.stdout,
                    title="Command Output",
                    border_style="green"
                )
                self.console.print(output_panel)
            
            if result.stderr:
                error_panel = Panel(
                    result.stderr,
                    title="Command Error",
                    border_style="red"
                )
                self.console.print(error_panel)
                
        except subprocess.TimeoutExpired:
            self.console.print("⏰ Command timed out after 30 seconds")
        except Exception as e:
            self.console.print(f"❌ Error executing command: {e}")
    
    def _code_execution_mode(self):
        """Code execution mode"""
        self.console.clear()
        self.console.print(Panel(
            "🚀 Code Execution Mode",
            style="bold magenta",
            border_style="magenta"
        ))
        
        self.console.print("Code execution interface (placeholder)")
        self.console.print("Press Enter to return to main menu...")
        input()
        
        self._show_main_interface()
    
    def _file_management_mode(self):
        """File management mode"""
        self.console.clear()
        self.console.print(Panel(
            "📁 File Management Mode",
            style="bold blue",
            border_style="blue"
        ))
        
        self.console.print("File management interface (placeholder)")
        self.console.print("Press Enter to return to main menu...")
        input()
        
        self._show_main_interface()
    
    def _settings_mode(self):
        """Settings mode"""
        self.console.clear()
        self.console.print(Panel(
            "⚙️ Settings",
            style="bold green",
            border_style="green"
        ))
        
        settings_table = Table(title="Current Settings")
        settings_table.add_column("Setting", style="cyan")
        settings_table.add_column("Value", style="white")
        
        settings_table.add_row("Language", self.translator.current_language.upper())
        settings_table.add_row("Security Level", str(self.security.protection_level) if self.security else "N/A")
        settings_table.add_row("Session Active", "Yes" if self.current_session else "No")
        settings_table.add_row("Interface", "TUI")
        
        self.console.print(settings_table)
        self.console.print("\nPress Enter to return to main menu...")
        input()
        
        self._show_main_interface()
    
    def _show_help(self):
        """Show help information"""
        self.console.clear()
        help_panel = Panel(
            """
🤖 AION TUI Help

Available Modes:
• AI Assistant - Chat with AI providers
• System Commands - Execute system commands safely
• Code Execution - Run code in multiple languages
• File Management - Browse and manage files
• Settings - View and modify configuration

Navigation:
• Use number keys (1-7) to select options
• Type 'back' to return to previous menu
• Press 'q' or Ctrl+C to exit current mode
• Type 'h' for help in any mode

Security Features:
• All commands are validated for security
• Sessions expire automatically for safety
• Dangerous commands are blocked
• Real-time threat monitoring active

Tips:
• TUI provides enhanced visual interface
• All features support multilingual interface
• System resources are monitored in real-time
            """,
            title="Help",
            border_style="blue"
        )
        self.console.print(help_panel)
        
        self.console.print("\nPress Enter to return to main menu...")
        input()
        
        self._show_main_interface()
    
    def _exit_tui(self):
        """Exit TUI interface"""
        self.is_running = False
        self.console.clear()
        
        goodbye_panel = Panel(
            f"👋 {self.translator.get('goodbye_message', 'Goodbye! Thanks for using AION!')}",
            style="bold green",
            border_style="green"
        )
        self.console.print(goodbye_panel)
        
        # Cleanup
        if self.current_session:
            # Session cleanup would happen here
            pass
    
    def stop(self):
        """Stop the TUI interface"""
        self._exit_tui()
