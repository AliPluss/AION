"""
💻 AION Command Line Interface
Interactive CLI with multilingual support
"""

import os
import sys
import subprocess
import platform
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax

from utils.translator import Translator
from core.security import SecurityManager

class CLI:
    """Command Line Interface for AION"""

    def __init__(self, translator: Translator, security: SecurityManager):
        self.translator = translator
        self.security = security
        self.console = Console()
        self.current_session = None
        self.command_history: List[str] = []
        self.system_info = self._get_system_info()
    
    def _get_system_info(self) -> Dict[str, str]:
        """Get system information"""
        return {
            'os': platform.system(),
            'platform': platform.platform(),
            'architecture': platform.architecture()[0],
            'python_version': platform.python_version(),
            'hostname': platform.node()
        }
    
    def ai_assistant_mode(self):
        """AI Assistant interactive mode"""
        self.console.print(Panel(
            f"🧠 {self.translator.get('ai_mode_title')}",
            border_style="cyan"
        ))
        
        self.console.print(f"💡 {self.translator.get('ai_mode_help', 'Enter your AI requests. Type \"back\" to return to main menu.')}")
        
        while True:
            try:
                user_input = Prompt.ask(f"\n🤖 AI")
                
                if user_input.lower() in ['back', 'exit', 'quit']:
                    break
                
                if user_input.strip():
                    self.command_history.append(f"AI: {user_input}")
                    # Here you would integrate with AI providers
                    self._simulate_ai_response(user_input)
                
            except KeyboardInterrupt:
                break
    
    def _simulate_ai_response(self, query: str):
        """Simulate AI response (placeholder for actual AI integration)"""
        self.console.print(f"🔄 {self.translator.get('processing')}")
        
        # This is a placeholder - in real implementation, you'd call AI providers
        responses = {
            'hello': f"👋 {self.translator.get('welcome_message')}",
            'help': f"❓ {self.translator.get('help_available', 'I can help you with code generation, system commands, and more!')}",
            'code': "💻 I can generate code in Python, Rust, C++, JavaScript and more!",
            'system': "🖥️ I can explain and help with system commands for Windows and Linux!"
        }
        
        # Simple keyword matching (replace with actual AI)
        response = "🤔 I'm still learning! This is a demo version."
        for keyword, reply in responses.items():
            if keyword.lower() in query.lower():
                response = reply
                break
        
        self.console.print(Panel(response, title="🤖 AI Response", border_style="green"))
    
    def system_commands_mode(self):
        """System commands interactive mode"""
        self.console.print(Panel(
            f"💻 {self.translator.get('system_mode_title')}",
            border_style="blue"
        ))
        
        # Show system info
        self._show_system_info()
        
        self.console.print(f"\n💡 {self.translator.get('system_mode_help', 'Enter system commands. Type \"help\" for available commands or \"back\" to return.')}")
        
        while True:
            try:
                command = Prompt.ask(f"\n{self.system_info['os']} $")
                
                if command.lower() in ['back', 'exit']:
                    break
                elif command.lower() == 'help':
                    self._show_system_help()
                elif command.strip():
                    self._execute_system_command(command)
                
            except KeyboardInterrupt:
                break
    
    def _show_system_info(self):
        """Display system information"""
        table = Table(title="System Information")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in self.system_info.items():
            table.add_row(key.replace('_', ' ').title(), value)
        
        self.console.print(table)
    
    def _show_system_help(self):
        """Show available system commands"""
        if self.system_info['os'] == 'Windows':
            commands = {
                'dir': 'List directory contents',
                'cd': 'Change directory',
                'mkdir': 'Create directory',
                'del': 'Delete files',
                'copy': 'Copy files',
                'move': 'Move files',
                'type': 'Display file contents',
                'systeminfo': 'Display system information',
                'tasklist': 'List running processes',
                'ipconfig': 'Display network configuration'
            }
        else:  # Linux/Unix
            commands = {
                'ls': 'List directory contents',
                'cd': 'Change directory',
                'mkdir': 'Create directory',
                'rm': 'Remove files',
                'cp': 'Copy files',
                'mv': 'Move files',
                'cat': 'Display file contents',
                'ps': 'List running processes',
                'top': 'Display running processes',
                'df': 'Display disk usage',
                'free': 'Display memory usage'
            }
        
        table = Table(title=f"{self.system_info['os']} Commands")
        table.add_column("Command", style="cyan")
        table.add_column("Description", style="white")
        
        for cmd, desc in commands.items():
            table.add_row(cmd, desc)
        
        self.console.print(table)
    
    def _execute_system_command(self, command: str):
        """Execute system command with security checks"""
        # Security check
        if not self.security.is_command_allowed(command):
            self.console.print(f"🚫 {self.translator.get('command_blocked', 'Command blocked for security reasons')}")
            return
        
        try:
            self.console.print(f"🔄 {self.translator.get('executing', 'Executing')}: {command}")
            
            # Execute command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Display output
            if result.stdout:
                self.console.print(Panel(
                    Syntax(result.stdout, "text", theme="monokai"),
                    title="Output",
                    border_style="green"
                ))
            
            if result.stderr:
                self.console.print(Panel(
                    result.stderr,
                    title="Error",
                    border_style="red"
                ))
            
            # Add to history
            self.command_history.append(f"CMD: {command}")
            
        except subprocess.TimeoutExpired:
            self.console.print(f"⏰ {self.translator.get('command_timeout', 'Command timed out')}")
        except Exception as e:
            self.console.print(f"❌ {self.translator.get('error_occurred')}: {str(e)}")
    
    def execute_code_mode(self):
        """Code execution mode"""
        self.console.print(Panel(
            f"📜 {self.translator.get('code_mode_title')}",
            border_style="magenta"
        ))
        
        languages = {
            '1': ('python', 'Python'),
            '2': ('javascript', 'JavaScript'),
            '3': ('rust', 'Rust'),
            '4': ('cpp', 'C++')
        }
        
        self.console.print("\nSupported Languages:")
        for key, (code, name) in languages.items():
            self.console.print(f"[{key}] {name}")
        
        choice = Prompt.ask("Select language (1-4)")
        
        if choice in languages:
            lang_code, lang_name = languages[choice]
            self._code_execution_session(lang_code, lang_name)
    
    def _code_execution_session(self, lang_code: str, lang_name: str):
        """Interactive code execution session"""
        self.console.print(f"\n🚀 {lang_name} Execution Mode")
        self.console.print("Enter your code (type 'run' to execute, 'back' to return):")
        
        code_lines = []
        
        while True:
            try:
                line = Prompt.ask(">>> " if not code_lines else "... ")
                
                if line.lower() == 'back':
                    break
                elif line.lower() == 'run':
                    if code_lines:
                        code = '\n'.join(code_lines)
                        self._execute_code(code, lang_code)
                        code_lines = []
                    else:
                        self.console.print("No code to execute!")
                elif line.lower() == 'clear':
                    code_lines = []
                    self.console.print("Code cleared!")
                else:
                    code_lines.append(line)
                    
            except KeyboardInterrupt:
                break
    
    def _execute_code(self, code: str, language: str):
        """Execute code in specified language"""
        try:
            self.console.print(f"🔄 {self.translator.get('executing')} {language} code...")
            
            # Create temporary file
            import tempfile
            
            if language == 'python':
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(code)
                    temp_file = f.name
                
                result = subprocess.run([sys.executable, temp_file], 
                                      capture_output=True, text=True, timeout=10)
            
            elif language == 'javascript':
                with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                    f.write(code)
                    temp_file = f.name
                
                result = subprocess.run(['node', temp_file], 
                                      capture_output=True, text=True, timeout=10)
            
            else:
                self.console.print(f"❌ {language} execution not implemented yet")
                return
            
            # Display results
            if result.stdout:
                self.console.print(Panel(
                    result.stdout,
                    title="Output",
                    border_style="green"
                ))
            
            if result.stderr:
                self.console.print(Panel(
                    result.stderr,
                    title="Error",
                    border_style="red"
                ))
            
            # Cleanup
            os.unlink(temp_file)
            
        except subprocess.TimeoutExpired:
            self.console.print("⏰ Code execution timed out")
        except Exception as e:
            self.console.print(f"❌ Execution error: {str(e)}")
    
    def plugins_mode(self):
        """Plugins management mode"""
        self.console.print(Panel(
            f"🧩 {self.translator.get('plugins_mode_title')}",
            border_style="yellow"
        ))
        
        self.console.print("Plugin system coming soon! 🚧")
    
    def settings_mode(self):
        """Settings management mode"""
        self.console.print(Panel(
            f"⚙️ {self.translator.get('settings_mode_title')}",
            border_style="bright_blue"
        ))
        
        settings_menu = [
            "1. Change Language",
            "2. Security Settings", 
            "3. AI Provider Settings",
            "4. Display Settings",
            "5. Back to Main Menu"
        ]
        
        for item in settings_menu:
            self.console.print(item)
        
        choice = Prompt.ask("Select option (1-5)")
        
        if choice == "1":
            self._language_settings()
        elif choice == "2":
            self._security_settings()
        else:
            self.console.print("Feature coming soon! 🚧")
    
    def _language_settings(self):
        """Language settings"""
        languages = self.translator.get_supported_languages()
        
        self.console.print("\nAvailable Languages:")
        for i, (code, name) in enumerate(languages.items(), 1):
            current = "✅" if code == self.translator.current_language else "  "
            self.console.print(f"{current} [{i}] {name}")
        
        try:
            choice = int(Prompt.ask(f"Select language (1-{len(languages)})"))
            lang_codes = list(languages.keys())
            if 1 <= choice <= len(lang_codes):
                new_lang = lang_codes[choice - 1]
                self.translator.set_language(new_lang)
                self.console.print(f"✅ {self.translator.get('language_changed')}")
        except ValueError:
            self.console.print("Invalid selection")
    
    def _security_settings(self):
        """Security settings display"""
        status = self.security.get_security_status()
        
        table = Table(title="Security Status")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in status.items():
            table.add_row(key.replace('_', ' ').title(), str(value))
        
        self.console.print(table)
    
    def show_help(self):
        """Display help information"""
        self.console.print(Panel(
            f"❓ {self.translator.get('help_title')}",
            border_style="bright_green"
        ))
        
        help_text = f"""
🤖 AION - AI Operating Node

{self.translator.get('help_description', 'AION is a multilingual terminal-based AI assistant that supports:')}

• 🧠 AI-powered code generation and assistance
• 💻 System command execution and explanation  
• 📜 Multi-language code execution (Python, JS, Rust, C++)
• 🧩 Plugin system for extensibility
• 🌐 Web interface for remote access
• 🔐 Dynamic security with session management
• 🌍 Multilingual interface support

{self.translator.get('help_commands', 'Available Commands:')}
• navigate - {self.translator.get('cmd_navigate', 'Navigate between sections')}
• generate - {self.translator.get('cmd_generate', 'Generate code with AI')}
• run - {self.translator.get('cmd_run', 'Execute code or commands')}
• plugins - {self.translator.get('cmd_plugins', 'Manage plugins')}
• help - {self.translator.get('cmd_help', 'Show this help')}
• exit - {self.translator.get('cmd_exit', 'Exit AION')}

{self.translator.get('help_support', 'For more help, visit the documentation or contact support.')}
        """
        
        self.console.print(help_text)

# Alias for backward compatibility
CLIInterface = CLI
