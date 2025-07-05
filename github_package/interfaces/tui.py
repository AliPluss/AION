"""
🎨 AION Text User Interface
Rich terminal interface using Textual
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Button, Static, Input, TextArea, Select, Log
from textual.binding import Binding
from textual.screen import Screen
from textual import events
from rich.text import Text

from utils.translator import Translator

class MainScreen(Screen):
    """Main screen for AION TUI"""
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("1", "ai_mode", "AI Assistant"),
        Binding("2", "system_mode", "System Commands"),
        Binding("3", "code_mode", "Execute Code"),
        Binding("4", "plugins_mode", "Plugins"),
        Binding("5", "settings_mode", "Settings"),
        Binding("l", "change_language", "Language"),
    ]
    
    def __init__(self, translator: Translator):
        super().__init__()
        self.translator = translator
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the main screen"""
        yield Header()
        
        with Container(id="main-container"):
            yield Static(self._get_welcome_text(), id="welcome")
            
            with Vertical(id="menu-container"):
                yield Button(f"🧠 {self.translator.get('menu_ai_assistant')}", id="ai-btn", variant="primary")
                yield Button(f"💻 {self.translator.get('menu_system_commands')}", id="system-btn", variant="default")
                yield Button(f"📜 {self.translator.get('menu_execute_code')}", id="code-btn", variant="default")
                yield Button(f"🧩 {self.translator.get('menu_plugins')}", id="plugins-btn", variant="default")
                yield Button(f"⚙️ {self.translator.get('menu_settings')}", id="settings-btn", variant="default")
                yield Button(f"🌍 {self.translator.get('menu_change_language')}", id="language-btn", variant="success")
        
        yield Footer()
    
    def _get_welcome_text(self) -> str:
        """Get welcome text in current language"""
        return f"""
╔═══════════════════════════════════════╗
║     █████╗ ██╗ ██████╗ ███╗   ██╗    ║
║    ██╔══██╗██║██╔═══██╗████╗  ██║    ║
║    ███████║██║██║   ██║██╔██╗ ██║    ║
║    ██╔══██║██║██║   ██║██║╚██╗██║    ║
║    ██║  ██║██║╚██████╔╝██║ ╚████║    ║
║    ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝    ║
║                                       ║
║    {self.translator.get('welcome_message')}    ║
╚═══════════════════════════════════════╝

{self.translator.get('tui_instructions', 'Use buttons or keyboard shortcuts to navigate')}
        """
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events"""
        if event.button.id == "ai-btn":
            self.action_ai_mode()
        elif event.button.id == "system-btn":
            self.action_system_mode()
        elif event.button.id == "code-btn":
            self.action_code_mode()
        elif event.button.id == "plugins-btn":
            self.action_plugins_mode()
        elif event.button.id == "settings-btn":
            self.action_settings_mode()
        elif event.button.id == "language-btn":
            self.action_change_language()
    
    def action_ai_mode(self) -> None:
        """Switch to AI Assistant mode"""
        self.app.push_screen(AIScreen(self.translator))
    
    def action_system_mode(self) -> None:
        """Switch to System Commands mode"""
        self.app.push_screen(SystemScreen(self.translator))
    
    def action_code_mode(self) -> None:
        """Switch to Code Execution mode"""
        self.app.push_screen(CodeScreen(self.translator))
    
    def action_plugins_mode(self) -> None:
        """Switch to Plugins mode"""
        self.app.push_screen(PluginsScreen(self.translator))
    
    def action_settings_mode(self) -> None:
        """Switch to Settings mode"""
        self.app.push_screen(SettingsScreen(self.translator))
    
    def action_change_language(self) -> None:
        """Change language"""
        self.app.push_screen(LanguageScreen(self.translator))

class AIScreen(Screen):
    """AI Assistant screen"""
    
    BINDINGS = [
        Binding("escape", "back", "Back"),
        Binding("enter", "send_message", "Send"),
    ]
    
    def __init__(self, translator: Translator):
        super().__init__()
        self.translator = translator
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container():
            yield Static(f"🧠 {self.translator.get('ai_mode_title')}", id="title")
            yield Log(id="chat-log")
            
            with Horizontal():
                yield Input(placeholder=self.translator.get('enter_message', 'Enter your message...'), id="message-input")
                yield Button("Send", id="send-btn", variant="primary")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "send-btn":
            self.action_send_message()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "message-input":
            self.action_send_message()
    
    def action_send_message(self) -> None:
        """Send message to AI"""
        message_input = self.query_one("#message-input", Input)
        chat_log = self.query_one("#chat-log", Log)
        
        message = message_input.value.strip()
        if message:
            chat_log.write_line(f"👤 You: {message}")
            chat_log.write_line(f"🤖 AI: {self.translator.get('ai_placeholder', 'AI response coming soon!')}")
            message_input.value = ""
    
    def action_back(self) -> None:
        """Go back to main screen"""
        self.app.pop_screen()

class SystemScreen(Screen):
    """System Commands screen"""
    
    BINDINGS = [
        Binding("escape", "back", "Back"),
        Binding("enter", "execute_command", "Execute"),
    ]
    
    def __init__(self, translator: Translator):
        super().__init__()
        self.translator = translator
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container():
            yield Static(f"💻 {self.translator.get('system_mode_title')}", id="title")
            yield Log(id="command-log")
            
            with Horizontal():
                yield Input(placeholder=self.translator.get('enter_command'), id="command-input")
                yield Button("Execute", id="execute-btn", variant="primary")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "execute-btn":
            self.action_execute_command()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "command-input":
            self.action_execute_command()
    
    def action_execute_command(self) -> None:
        """Execute system command"""
        command_input = self.query_one("#command-input", Input)
        command_log = self.query_one("#command-log", Log)
        
        command = command_input.value.strip()
        if command:
            command_log.write_line(f"$ {command}")
            command_log.write_line(f"Output: {self.translator.get('command_placeholder', 'Command execution coming soon!')}")
            command_input.value = ""
    
    def action_back(self) -> None:
        """Go back to main screen"""
        self.app.pop_screen()

class CodeScreen(Screen):
    """Code Execution screen"""
    
    BINDINGS = [
        Binding("escape", "back", "Back"),
        Binding("ctrl+r", "run_code", "Run Code"),
    ]
    
    def __init__(self, translator: Translator):
        super().__init__()
        self.translator = translator
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container():
            yield Static(f"📜 {self.translator.get('code_mode_title')}", id="title")
            
            with Horizontal():
                yield Select([
                    ("Python", "python"),
                    ("JavaScript", "javascript"),
                    ("Rust", "rust"),
                    ("C++", "cpp")
                ], id="language-select")
                yield Button("Run Code", id="run-btn", variant="primary")
            
            yield TextArea("# Enter your code here\nprint('Hello, AION!')", id="code-editor")
            yield Log(id="output-log")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run-btn":
            self.action_run_code()
    
    def action_run_code(self) -> None:
        """Run the code"""
        code_editor = self.query_one("#code-editor", TextArea)
        output_log = self.query_one("#output-log", Log)
        language_select = self.query_one("#language-select", Select)
        
        code = code_editor.text
        language = language_select.value
        
        output_log.write_line(f"🔄 Running {language} code...")
        output_log.write_line(f"Output: {self.translator.get('code_placeholder', 'Code execution coming soon!')}")
    
    def action_back(self) -> None:
        """Go back to main screen"""
        self.app.pop_screen()

class PluginsScreen(Screen):
    """Plugins screen"""
    
    BINDINGS = [
        Binding("escape", "back", "Back"),
    ]
    
    def __init__(self, translator: Translator):
        super().__init__()
        self.translator = translator
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container():
            yield Static(f"🧩 {self.translator.get('plugins_mode_title')}", id="title")
            yield Static(f"{self.translator.get('coming_soon', 'Plugin system coming soon!')} 🚧")
        
        yield Footer()
    
    def action_back(self) -> None:
        """Go back to main screen"""
        self.app.pop_screen()

class SettingsScreen(Screen):
    """Settings screen"""
    
    BINDINGS = [
        Binding("escape", "back", "Back"),
    ]
    
    def __init__(self, translator: Translator):
        super().__init__()
        self.translator = translator
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container():
            yield Static(f"⚙️ {self.translator.get('settings_mode_title')}", id="title")
            yield Button(f"🌍 {self.translator.get('menu_change_language')}", id="lang-btn")
            yield Button(f"🔐 {self.translator.get('security_settings', 'Security Settings')}", id="security-btn")
            yield Button(f"🤖 {self.translator.get('ai_settings', 'AI Settings')}", id="ai-settings-btn")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "lang-btn":
            self.app.push_screen(LanguageScreen(self.translator))
    
    def action_back(self) -> None:
        """Go back to main screen"""
        self.app.pop_screen()

class LanguageScreen(Screen):
    """Language selection screen"""
    
    BINDINGS = [
        Binding("escape", "back", "Back"),
    ]
    
    def __init__(self, translator: Translator):
        super().__init__()
        self.translator = translator
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        with Container():
            yield Static(f"🌍 {self.translator.get('choose_language')}", id="title")
            
            languages = self.translator.get_supported_languages()
            for code, name in languages.items():
                current = "✅ " if code == self.translator.current_language else ""
                yield Button(f"{current}{name}", id=f"lang-{code}")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id and event.button.id.startswith("lang-"):
            lang_code = event.button.id.replace("lang-", "")
            self.translator.set_language(lang_code)
            self.app.pop_screen()
    
    def action_back(self) -> None:
        """Go back to previous screen"""
        self.app.pop_screen()

class TUI(App):
    """Main TUI Application"""
    
    CSS = """
    #main-container {
        align: center middle;
        width: 80%;
        height: 80%;
    }
    
    #welcome {
        text-align: center;
        margin: 1;
        padding: 1;
    }
    
    #menu-container {
        align: center middle;
        width: 50%;
    }
    
    Button {
        margin: 1;
        width: 100%;
    }
    
    #title {
        text-align: center;
        margin: 1;
        text-style: bold;
    }
    
    #chat-log, #command-log, #output-log {
        height: 60%;
        border: solid $primary;
        margin: 1;
    }
    
    #code-editor {
        height: 40%;
        border: solid $primary;
        margin: 1;
    }
    """
    
    def __init__(self, translator: Translator):
        super().__init__()
        self.translator = translator
        self.title = "AION - AI Operating Node"
        self.sub_title = translator.get('welcome_message')
    
    def on_mount(self) -> None:
        """Called when app starts"""
        self.push_screen(MainScreen(self.translator))

# Alias for backward compatibility
TUIInterface = TUI
