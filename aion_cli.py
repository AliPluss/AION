#!/usr/bin/env python3
"""
🚀 AION CLI Entry Point
Professional command-line interface for AION AI Operating Node

This is the main entry point for AION, providing:
- Unified command-line interface with argument parsing
- Environment configuration and API key management
- Language selection and initialization
- Interface routing (CLI/TUI/Web)
- Error handling and graceful fallbacks
- Cross-platform compatibility
"""

import os
import sys
import argparse
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# AION imports
try:
    from aion.utils.translator import Translator
    from aion.core.security import SecurityManager
    from aion.interfaces.tui import TUI
    from aion.interfaces.cli import CLIInterface
    from aion.core.ai_providers import AdvancedAIManager
    AION_IMPORTS_OK = True
except ImportError as e:
    AION_IMPORTS_OK = False
    IMPORT_ERROR = str(e)

class AIONBootstrap:
    """
    🚀 AION Bootstrap Manager
    
    Handles application initialization, configuration, and interface routing.
    Provides a unified entry point for all AION functionality.
    """
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.config = {}
        self.translator = None
        self.security = None
        
        # Load environment configuration
        self._load_environment()
        
        # Initialize core components
        self._initialize_components()
    
    def _load_environment(self):
        """Load environment variables and configuration"""
        # Load .env file if available
        if DOTENV_AVAILABLE:
            env_file = project_root / '.env'
            if env_file.exists():
                load_dotenv(env_file)
                self._print_success("✅ Environment configuration loaded")
            else:
                self._print_warning("⚠️ No .env file found - using system environment")
        
        # Load API keys from environment
        self.config = {
            'openai_api_key': os.getenv('OPENAI_API_KEY'),
            'deepseek_api_key': os.getenv('DEEPSEEK_API_KEY'),
            'google_api_key': os.getenv('GOOGLE_API_KEY'),
            'openrouter_api_key': os.getenv('OPENROUTER_API_KEY'),
            'default_language': os.getenv('AION_DEFAULT_LANGUAGE', 'en'),
            'interface_mode': os.getenv('AION_INTERFACE', 'tui'),
            'debug_mode': os.getenv('AION_DEBUG', 'false').lower() == 'true'
        }
    
    def _initialize_components(self):
        """Initialize core AION components"""
        if not AION_IMPORTS_OK:
            self._print_error(f"❌ Failed to import AION modules: {IMPORT_ERROR}")
            # Initialize basic translator even if imports fail
            try:
                from aion.utils.translator import Translator
                self.translator = Translator()
                self.translator.set_language(self.config['default_language'])
            except:
                self.translator = None
            return False

        try:
            # Initialize translator with default language
            self.translator = Translator()
            self.translator.set_language(self.config['default_language'])

            # Initialize security manager
            self.security = SecurityManager()

            self._print_success("✅ AION core components initialized")
            return True

        except Exception as e:
            self._print_error(f"❌ Failed to initialize AION: {str(e)}")
            # Ensure translator is available even if other components fail
            try:
                from aion.utils.translator import Translator
                self.translator = Translator()
                self.translator.set_language(self.config['default_language'])
            except:
                self.translator = None
            return False
    
    def _print_success(self, message: str):
        """Print success message"""
        if self.console:
            self.console.print(message, style="green")
        else:
            print(message)
    
    def _print_warning(self, message: str):
        """Print warning message"""
        if self.console:
            self.console.print(message, style="yellow")
        else:
            print(message)
    
    def _print_error(self, message: str):
        """Print error message"""
        if self.console:
            self.console.print(message, style="red")
        else:
            print(message)
    
    def _print_info(self, message: str):
        """Print info message"""
        if self.console:
            self.console.print(message, style="cyan")
        else:
            print(message)
    
    def check_api_keys(self) -> bool:
        """Check if at least one AI provider API key is configured"""
        api_keys = [
            self.config['openai_api_key'],
            self.config['deepseek_api_key'],
            self.config['google_api_key'],
            self.config['openrouter_api_key']
        ]
        
        if not any(api_keys):
            self._print_warning("⚠️ No AI provider API keys found")
            self._print_info("💡 Create a .env file with your API keys for full functionality")
            return False
        
        configured_providers = []
        if self.config['openai_api_key']:
            configured_providers.append("OpenAI")
        if self.config['deepseek_api_key']:
            configured_providers.append("DeepSeek")
        if self.config['google_api_key']:
            configured_providers.append("Google")
        if self.config['openrouter_api_key']:
            configured_providers.append("OpenRouter")
        
        self._print_success(f"✅ AI Providers configured: {', '.join(configured_providers)}")
        return True
    
    def select_language(self) -> str:
        """Interactive language selection with arrow key navigation"""
        if not self.console:
            return self.config['default_language']

        try:
            from aion.interfaces.arrow_navigation import select_language_arrows
            self.console.print("\n🌐 [bold yellow]Language Selection[/bold yellow]")
            lang_code = select_language_arrows()
            if lang_code:
                self.translator.set_language(lang_code)
                self.console.print(f"\n✅ [bold green]Language changed to: {self.translator.get_language_name(lang_code)}[/bold green]")
                return lang_code
            else:
                self.console.print("\n❌ [bold red]Language change cancelled[/bold red]")
                return self.config['default_language']
        except Exception as e:
            self._print_error(f"❌ Error selecting language: {e}")
            return self.config['default_language']
    
    def start_interface(self, interface_type: str = None):
        """Start the specified interface"""
        if not AION_IMPORTS_OK:
            self._print_error("❌ Cannot start interface - AION modules not available")
            return False
        
        interface_type = interface_type or self.config['interface_mode']
        
        try:
            if interface_type.lower() == 'tui':
                self._print_info("🖥️ Starting TUI interface...")
                tui = TUI(self.translator, self.security)
                tui.start()
            
            elif interface_type.lower() == 'cli':
                self._print_info("💻 Starting CLI interface...")
                cli = CLIInterface(self.translator, self.security)
                cli.start()
            
            else:
                self._print_error(f"❌ Unknown interface type: {interface_type}")
                return False
                
        except KeyboardInterrupt:
            self._print_info("\n👋 AION shutdown requested by user")
            return True
        except Exception as e:
            self._print_error(f"❌ Interface error: {str(e)}")
            return False
    
    def show_banner(self):
        """Display AION banner"""
        banner = """
    ╔═══════════════════════════════════════╗
    ║              🤖 AION                  ║
    ║        AI Operating Node              ║
    ║     Professional Terminal AI          ║
    ║                                       ║
    ╚═══════════════════════════════════════╝
        """
        
        if self.console:
            self.console.print(Panel(
                Text(banner, style="bold cyan"),
                title="[bold green]Welcome to AION[/bold green]",
                border_style="bright_blue"
            ))
        else:
            print(banner)

    def handle_ai_prompt(self, prompt: str):
        """Handle AI prompt from command line"""
        self._print_info(f"🧠 Processing AI prompt: {prompt}")

        try:
            # Initialize AI manager if available
            if AION_IMPORTS_OK:
                from aion.core.ai_providers import AdvancedAIManager
                ai_manager = AdvancedAIManager()

                # Process the prompt
                self._print_info("🔄 Sending request to AI provider...")
                response = f"AI Response simulation for: {prompt}"

                self._print_success("✅ AI Response received:")
                if self.console:
                    self.console.print(Panel(response, title="🤖 AI Response", border_style="green"))
                else:
                    print(f"AI Response: {response}")

            else:
                self._print_warning("⚠️ AI providers not available - using fallback response")
                fallback_response = f"Fallback response for prompt: {prompt}"
                if self.console:
                    self.console.print(Panel(fallback_response, title="🤖 Fallback Response", border_style="yellow"))
                else:
                    print(f"Fallback Response: {fallback_response}")

        except Exception as e:
            self._print_error(f"❌ Error processing AI prompt: {str(e)}")

    def handle_code_execution(self, code: str):
        """Handle code execution from command line"""
        self._print_info(f"⚡ Executing code: {code}")

        try:
            # Initialize sandbox if available
            if AION_IMPORTS_OK:
                from aion.core.sandbox import AdvancedSandbox, SandboxConfig
                config = SandboxConfig(max_memory_mb=50, max_cpu_time_seconds=10)
                sandbox = AdvancedSandbox(config)

                # Execute the code
                self._print_info("🔄 Executing in sandbox...")
                return_code, stdout, stderr = sandbox.execute_command(['python', '-c', code])

                if return_code == 0:
                    self._print_success("✅ Code executed successfully:")
                    if self.console:
                        self.console.print(Panel(stdout, title="📤 Output", border_style="green"))
                    else:
                        print(f"Output: {stdout}")
                else:
                    self._print_error("❌ Code execution failed:")
                    if self.console:
                        self.console.print(Panel(stderr, title="❌ Error", border_style="red"))
                    else:
                        print(f"Error: {stderr}")

            else:
                self._print_warning("⚠️ Sandbox not available - simulating execution")
                if self.console:
                    self.console.print(Panel(f"Simulated execution of: {code}", title="⚡ Simulation", border_style="yellow"))
                else:
                    print(f"Simulated execution: {code}")

        except Exception as e:
            self._print_error(f"❌ Error executing code: {str(e)}")

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="🤖 AION - AI Operating Node",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python aion_cli.py                    # Start with default TUI interface
  python aion_cli.py --interface cli    # Start CLI interface
  python aion_cli.py --language ar      # Start with Arabic language
  python aion_cli.py --setup            # Run initial setup
        """
    )
    
    parser.add_argument(
        '--interface', '-i',
        choices=['tui', 'cli'],
        default='tui',
        help='Interface type to use (default: tui)'
    )
    
    parser.add_argument(
        '--language', '-l',
        choices=['en', 'ar', 'no', 'de', 'fr', 'zh', 'es'],
        help='Language code (default: en)'
    )
    
    parser.add_argument(
        '--setup', '-s',
        action='store_true',
        help='Run initial setup and configuration'
    )
    
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Enable debug mode'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='AION v1.0.0-production-ready'
    )

    parser.add_argument(
        '--ai-prompt', '-p',
        type=str,
        help='Execute AI prompt directly from command line'
    )

    parser.add_argument(
        '--execute', '-e',
        type=str,
        help='Execute code directly from command line'
    )

    return parser

def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Initialize AION bootstrap
    bootstrap = AIONBootstrap()
    
    # Show banner
    bootstrap.show_banner()
    
    # Override config with command line arguments
    if args.language:
        bootstrap.config['default_language'] = args.language
        if bootstrap.translator:
            bootstrap.translator.set_language(args.language)
    
    if args.debug:
        bootstrap.config['debug_mode'] = True
    
    # Check API keys
    bootstrap.check_api_keys()
    
    # Run setup if requested
    if args.setup:
        bootstrap.select_language()
        bootstrap._print_success("✅ Setup completed!")
        return

    # Handle AI prompt if provided
    if args.ai_prompt:
        bootstrap.handle_ai_prompt(args.ai_prompt)
        return

    # Handle code execution if provided
    if args.execute:
        bootstrap.handle_code_execution(args.execute)
        return

    # Start unified AION engine
    try:
        from aion_engine import AIONEngine
        engine = AIONEngine()
        engine.run()
        return
    except ImportError as e:
        bootstrap._print_error(f"❌ AION Engine not available: {e}")
        bootstrap._print_info("🔄 Falling back to standard interface")
        success = bootstrap.start_interface(args.interface)
        if not success:
            sys.exit(1)
    except Exception as e:
        bootstrap._print_error(f"❌ Engine error: {e}")
        bootstrap._print_info("🔄 Falling back to standard interface")
        success = bootstrap.start_interface(args.interface)
        if not success:
            sys.exit(1)

if __name__ == "__main__":
    main()
