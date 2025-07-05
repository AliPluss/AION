#!/usr/bin/env python3
"""
🧠 AION - AI Operating Node Enhanced Setup
Multi-language terminal assistant with advanced AI capabilities
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path
import platform
import time

def print_banner():
    """Print AION banner with animation"""
    banner = """
╔═══════════════════════════════════════════════════════════════════════════╗
║     █████╗ ██╗ ██████╗ ███╗   ██╗    ███████╗███████╗████████╗██╗   ██╗   ║
║    ██╔══██╗██║██╔═══██╗████╗  ██║    ██╔════╝██╔════╝╚══██╔══╝██║   ██║   ║
║    ███████║██║██║   ██║██╔██╗ ██║    ███████╗█████╗     ██║   ██║   ██║   ║
║    ██╔══██║██║██║   ██║██║╚██╗██║    ╚════██║██╔══╝     ██║   ██║   ██║   ║
║    ██║  ██║██║╚██████╔╝██║ ╚████║    ███████║███████╗   ██║   ╚██████╔╝   ║
║    ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝    ╚══════╝╚══════╝   ╚═╝    ╚═════╝    ║
║                                                                           ║
║                    AI Operating Node - Enhanced Setup                     ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """
    for line in banner.split('\n'):
        print(line)
        time.sleep(0.05)
    print("\n🚀 Welcome to AION Enhanced Setup!\n")
    time.sleep(0.5)

def setup_environment():
    """Setup virtual environment and install dependencies"""
    print("🔧 Setting up AION environment...")
    
    # Create project directory
    home_dir = Path.home()
    aion_dir = home_dir / "aion-enhanced"
    aion_dir.mkdir(exist_ok=True)
    
    # Create virtual environment
    venv_dir = aion_dir / "venv"
    if not venv_dir.exists():
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)])
    
    # Determine pip path
    if os.name == 'nt':  # Windows
        pip_path = venv_dir / "Scripts" / "pip"
        python_path = venv_dir / "Scripts" / "python"
    else:  # Unix/Linux/Mac
        pip_path = venv_dir / "bin" / "pip"
        python_path = venv_dir / "bin" / "python"
    
    # Install dependencies
    print("📚 Installing dependencies (this may take a few minutes)...")
    dependencies = [
        "rich>=10.0.0", 
        "typer>=0.7.0", 
        "textual>=0.10.1", 
        "fastapi>=0.95.0", 
        "uvicorn>=0.21.1", 
        "pydantic>=1.10.7", 
        "openai>=1.0.0", 
        "google-generativeai>=0.3.0", 
        "python-dotenv>=1.0.0",
        "requests>=2.28.2", 
        "pyyaml>=6.0", 
        "colorama>=0.4.6", 
        "prompt_toolkit>=3.0.38", 
        "pygments>=2.15.0",
        "langchain>=0.0.200", 
        "transformers>=4.28.1", 
        "numpy>=1.24.2",
        "websockets>=11.0.2",
        "pyttsx3>=2.90",
        "SpeechRecognition>=3.10.0",
        "markdown>=3.4.3",
        "pdfkit>=1.0.0",
        "psutil>=5.9.5",
        "docker>=6.1.0",
        "schedule>=1.2.0"
    ]
    
    # Update pip first
    subprocess.run([str(pip_path), "install", "--upgrade", "pip"])
    
    # Install dependencies in batches to avoid memory issues
    batch_size = 5
    for i in range(0, len(dependencies), batch_size):
        batch = dependencies[i:i+batch_size]
        subprocess.run([str(pip_path), "install", "--upgrade"] + batch)
        print(f"✅ Installed batch {i//batch_size + 1}/{(len(dependencies)-1)//batch_size + 1}")
    
    # Try to install optional dependencies
    try:
        if platform.system() == "Windows":
            subprocess.run([str(pip_path), "install", "pywin32>=306"])
        
        # Try to install torch with CUDA support
        subprocess.run([str(pip_path), "install", "torch", "torchvision", "torchaudio"])
    except Exception as e:
        print(f"⚠️ Some optional dependencies couldn't be installed: {e}")
    
    # Create directories
    dirs = ["config", "logs", "plugins", "data", "sessions", "sandbox", "recipes"]
    for dir_name in dirs:
        (aion_dir / dir_name).mkdir(exist_ok=True)
    
    return aion_dir, venv_dir, python_path

def download_source_code(aion_dir):
    """Create AION source code structure"""
    print("📥 Creating AION source code structure...")
    
    # Create source directories
    src_dir = aion_dir / "src"
    src_dir.mkdir(exist_ok=True)
    
    # Create core modules
    modules = [
        "ai", "cli", "tui", "web", "security", "plugins", "utils", "core",
        "voice", "sandbox", "recipes", "scheduler", "analytics", "export"
    ]
    for module in modules:
        module_dir = src_dir / module
        module_dir.mkdir(exist_ok=True)
        init_file = module_dir / "__init__.py"
        init_file.touch()
    
    # Create main.py
    create_main_script(aion_dir)
    
    return src_dir

def create_config_files(aion_dir):
    """Create configuration files"""
    print("⚙️ Creating configuration files...")
    
    config_dir = aion_dir / "config"
    
    # Create AI provider config
    ai_config = {
        "openai": {
            "enabled": True,
            "api_key": "",
            "model": "gpt-3.5-turbo",
            "available_models": [
                "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini"
            ],
            "settings": {
                "max_tokens": 2000,
                "temperature": 0.7,
                "top_p": 1.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0
            }
        },
        "gemini": {
            "enabled": True,
            "api_key": "",
            "model": "gemini-pro",
            "available_models": ["gemini-pro", "gemini-pro-vision"],
            "settings": {
                "temperature": 0.7,
                "top_p": 1.0,
                "top_k": 40
            }
        },
        "anthropic": {
            "enabled": True,
            "api_key": "",
            "model": "claude-3-opus",
            "available_models": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
            "settings": {
                "max_tokens": 2000,
                "temperature": 0.7
            }
        },
        "deepseek": {
            "enabled": True,
            "api_key": "",
            "model": "deepseek-coder",
            "available_models": ["deepseek-coder", "deepseek-chat"],
            "settings": {
                "temperature": 0.7,
                "top_p": 1.0
            }
        },
        "default_provider": "openai",
        "global_settings": {
            "timeout": 30,
            "retry_attempts": 3,
            "retry_delay": 1.0,
            "enable_streaming": True,
            "enable_function_calling": True,
            "enable_code_execution": True,
            "max_conversation_history": 10
        },
        "logging": {
            "enable_request_logging": True,
            "enable_response_logging": False,
            "log_level": "INFO",
            "log_file": "~/.aion/logs/ai_requests.log"
        }
    }
    
    with open(config_dir / "ai_config.json", "w", encoding="utf-8") as f:
        json.dump(ai_config, f, indent=2)
    
    # Create user preferences
    user_prefs = {
        "interface": {
            "language": "en",
            "theme": "dark",
            "emoji_enabled": True,
            "rich_formatting": True,
            "auto_complete": True,
            "syntax_highlighting": True
        },
        "security": {
            "sandbox_execution": True,
            "code_analysis_before_execution": True,
            "api_key_encryption": True,
            "max_execution_time": 30,
            "allowed_network_access": False,
            "allowed_file_access": ["~/aion-enhanced/sandbox"]
        },
        "features": {
            "voice_interface": False,
            "session_logging": True,
            "auto_update": True,
            "scheduled_tasks": True,
            "plugin_auto_discovery": True,
            "code_quality_metrics": True
        },
        "advanced": {
            "developer_mode": False,
            "debug_logging": False,
            "experimental_features": False,
            "custom_prompt_templates": True,
            "system_integration": True
        }
    }
    
    with open(config_dir / "user_preferences.json", "w", encoding="utf-8") as f:
        json.dump(user_prefs, f, indent=2)
    
    # Create languages config
    languages = {
        "supported_languages": [
            {"code": "en", "name": "English", "flag": "🇬🇧", "rtl": False},
            {"code": "ar", "name": "العربية", "flag": "🇸🇦", "rtl": True},
            {"code": "no", "name": "Norsk", "flag": "🇳🇴", "rtl": False},
            {"code": "de", "name": "Deutsch", "flag": "🇩🇪", "rtl": False},
            {"code": "fr", "name": "Français", "flag": "🇫🇷", "rtl": False},
            {"code": "zh", "name": "中文", "flag": "🇨🇳", "rtl": False},
            {"code": "es", "name": "Español", "flag": "🇪🇸", "rtl": False}
        ],
        "translations": {
            "main_menu": {
                "en": "Main Menu",
                "ar": "القائمة الرئيسية",
                "no": "Hovedmeny",
                "de": "Hauptmenü",
                "fr": "Menu Principal",
                "zh": "主菜单",
                "es": "Menú Principal"
            },
            "ai_assistant": {
                "en": "AI Assistant",
                "ar": "مساعد الذكاء الاصطناعي",
                "no": "AI-assistent",
                "de": "KI-Assistent",
                "fr": "Assistant IA",
                "zh": "人工智能助手",
                "es": "Asistente de IA"
            },
            "execute_code": {
                "en": "Execute Code",
                "ar": "تنفيذ الكود",
                "no": "Kjør Kode",
                "de": "Code Ausführen",
                "fr": "Exécuter le Code",
                "zh": "执行代码",
                "es": "Ejecutar Código"
            }
        },
        "default": "en"
    }
    
    with open(config_dir / "languages.json", "w", encoding="utf-8") as f:
        json.dump(languages, f, indent=2)
    
    # Create sandbox config
    sandbox_config = {
        "enabled": True,
        "isolation_level": "process",  # process, container, or vm
        "resource_limits": {
            "max_cpu_percent": 50,
            "max_memory_mb": 500,
            "max_disk_mb": 100,
            "max_execution_time_seconds": 30
        },
        "allowed_modules": {
            "python": ["os.path", "sys", "math", "random", "datetime", "json", "re"],
            "javascript": ["fs.promises", "path", "crypto", "util", "os"],
            "rust": ["std::fs", "std::path", "std::io", "std::time", "std::env"]
        },
        "network_access": False,
        "file_access": {
            "allowed_paths": ["~/aion-enhanced/sandbox"],
            "read_only_paths": ["~/aion-enhanced/data/examples"]
        }
    }
    
    with open(config_dir / "sandbox_config.json", "w", encoding="utf-8") as f:
        json.dump(sandbox_config, f, indent=2)
    
    # Create plugins config
    plugins_config = {
        "enabled": True,
        "auto_discovery": True,
        "plugin_directories": ["~/aion-enhanced/plugins"],
        "trusted_sources": ["github.com/aion-ecosystem"],
        "allowed_capabilities": ["file_access", "network_access", "ui_integration"],
        "auto_update": False,
        "installed_plugins": []
    }
    
    with open(config_dir / "plugins_config.json", "w", encoding="utf-8") as f:
        json.dump(plugins_config, f, indent=2)

def create_main_script(aion_dir):
    """Create the main.py script"""
    main_script = """#!/usr/bin/env python3
"""\"
🧠 AION - AI Operating Node
Terminal-based AI Assistant with Multilingual Support

Enhanced Edition with advanced features:
- Multi-language code execution
- AI-powered assistance
- Plugin system
- Web interface
- Voice commands
- Sandbox execution
- Educational mode
- Recipe system
- Scheduled tasks
\"\"\"

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import os
import sys
from pathlib import Path
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Import AION modules
from src.cli import cli_app
from src.tui import tui_app
from src.web import web_app
from src.core import version
from src.utils.logger import setup_logger

# Setup logger
logger = setup_logger()

app = typer.Typer(help="🤖 AION - AI Operating Node Terminal Assistant")
console = Console()

@app.command()
def start():
    \"\"\"🚀 Start AION Terminal Assistant\"\"\"
    logger.info("Starting AION CLI")
    cli_app.start_cli()

@app.command()
def tui():
    \"\"\"🎨 Start AION in Text User Interface mode\"\"\"
    logger.info("Starting AION TUI")
    asyncio.run(tui_app.start_tui())

@app.command()
def web(host: str = "127.0.0.1", port: int = 8000):
    \"\"\"🌐 Start AION Web Interface\"\"\"
    logger.info(f"Starting AION Web Interface on {host}:{port}")
    web_app.start_web(host, port)

@app.command()
def voice():
    \"\"\"🎤 Start AION with voice interface\"\"\"
    logger.info("Starting AION Voice Interface")
    from src.voice import voice_app
    voice_app.start_voice()

@app.command()
def schedule(task_file: str = None):
    \"\"\"⏰ Run or manage scheduled tasks\"\"\"
    logger.info("Managing scheduled tasks")
    from src.scheduler import scheduler
    scheduler.manage_tasks(task_file)

@app.command()
def version():
    \"\"\"📋 Show AION version information\"\"\"
    logger.info("Displaying version information")
    console.print(Panel.fit(
        f"[bold blue]AION - AI Operating Node[/bold blue]\\n"
        f"[green]Version: {version.VERSION}[/green]\\n"
        f"[yellow]Enhanced Edition[/yellow]\\n"
        f"[cyan]Build Date: {version.BUILD_DATE}[/cyan]",
        title="📋 Version Info"
    ))

@app.command()
def setup():
    \"\"\"🔧 Configure AION settings\"\"\"
    logger.info("Running setup wizard")
    from src.utils.setup_wizard import run_wizard
    run_wizard()

@app.command()
def plugin(action: str = "list", name: str = None):
    \"\"\"🧩 Manage plugins (list, install, remove, info)\"\"\"
    logger.info(f"Plugin management: {action} {name or ''}")
    from src.plugins.manager import manage_plugins
    manage_plugins(action, name)

@app.command()
def export(session_id: str = None, format: str = "markdown"):
    \"\"\"📤 Export session to file (markdown, pdf, html)\"\"\"
    logger.info(f"Exporting session {session_id or 'latest'} to {format}")
    from src.export import exporter
    exporter.export_session(session_id, format)

if __name__ == "__main__":
    console.print(Panel.fit(
        "[bold blue]AION - AI Operating Node[/bold blue]\\n"
        "[green]Enhanced Terminal Assistant[/green]\\n"
        "[yellow]Type 'python main.py --help' for available commands[/yellow]",
        title="🤖 AION"
    ))
    app()
"""
    
    with open(aion_dir / "main.py", "w", encoding="utf-8") as f:
        f.write(main_script)

def create_launcher_scripts(aion_dir, venv_dir, python_path):
    """Create launcher scripts for different platforms"""
    print("🚀 Creating launcher scripts...")
    
    # Windows batch file
    if os.name == 'nt':
        batch_content = f"""@echo off
cd "{aion_dir}"
call "{venv_dir}\\Scripts\\activate.bat"
python main.py %*
"""
        with open(aion_dir / "aion.bat", "w") as f:
            f.write(batch_content)
        
        # Create shortcut
        try:
            import win32com.client
            shortcut_path = os.path.join(os.path.expanduser("~"), "Desktop", "AION Enhanced.lnk")
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = str(aion_dir / "aion.bat")
            shortcut.WorkingDirectory = str(aion_dir)
            shortcut.IconLocation = f"{sys.executable},0"
            shortcut.save()
            print(f"✅ Created desktop shortcut: {shortcut_path}")
        except:
            print("⚠️ Could not create desktop shortcut automatically")
    
    # Unix/Linux/Mac shell script
    else:
        shell_content = f"""#!/bin/bash
cd "{aion_dir}"
source "{venv_dir}/bin/activate"
python main.py "$@"
"""
        shell_script = aion_dir / "aion.sh"
        with open(shell_script, "w") as f:
            f.write(shell_content)
        # Make executable
        shell_script.chmod(0o755)
        
        # Create symlink in /usr/local/bin if possible
        try:
            bin_dir = Path("/usr/local/bin")
            if bin_dir.exists() and os.access(bin_dir, os.W_OK):
                symlink_path = bin_dir / "aion"
                if symlink_path.exists():
                    symlink_path.unlink()
                symlink_path.symlink_to(shell_script)
                print(f"✅ Created symlink: {symlink_path}")
        except:
            print("⚠️ Could not create symlink in /usr/local/bin (requires sudo)")

def create_core_modules(src_dir):
    """Create core AION modules"""
    print("🧠 Creating enhanced AION core modules...")
    
    # Create version.py
    version_file = src_dir / "core" / "version.py"
    with open(version_file, "w", encoding="utf-8") as f:
        f.write('"""AION version information"""\n\nimport datetime\n\nVERSION = "1.0.0-enhanced"\nBUILD_DATE = datetime.datetime.now().strftime("%Y-%m-%d")\n')
    
    # Create logger.py
    logger_file = src_dir / "utils" / "logger.py"
    with open(logger_file, "w", encoding="utf-8") as f:
        f.write("""\"\"\"Logging utilities for AION\"\"\"
import logging
import os
from pathlib import Path
from datetime import datetime

def setup_logger(name="aion", level=logging.INFO):
    \"\"\"Setup and configure logger\"\"\"
    # Create logs directory
    log_dir = Path.home() / "aion-enhanced" / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Create log file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = log_dir / f"aion_{timestamp}.log"
    
    # Configure logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)  # Only warnings and errors to console
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
""")

    # Create AI manager module
    ai_manager = src_dir / "ai" / "manager.py"
    with open(ai_manager, "w", encoding="utf-8") as f:
        f.write("""\"\"\"AI Provider Manager for AION\"\"\"
import json
import os
import logging
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Setup logger
logger = logging.getLogger("aion.ai")

class AIManager:
    \"\"\"Manages AI providers and interactions\"\"\"
    
    def __init__(self):
        self.config = self._load_config()
        self.providers = {}
        self.setup_providers()
        self.conversation_history = []
        self.max_history = self.config.get("global_settings", {}).get("max_conversation_history", 10)
    
    def _load_config(self) -> Dict:
        \"\"\"Load AI configuration\"\"\"
        config_path = Path.home() / "aion-enhanced" / "config" / "ai_config.json"
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading AI config: {e}")
                return {}
        return {}
    
    def setup_providers(self) -> None:
        \"\"\"Setup AI providers based on configuration\"\"\"
        # Setup OpenAI
        if self.config.get("openai", {}).get("enabled", False):
            api_key = self.config["openai"].get("api_key")
            if api_key:
                try:
                    import openai
                    openai.api_key = api_key
                    self.providers["openai"] = {
                        "name": "OpenAI",
                        "client": openai,
                        "models": self.config["openai"].get("available_models", []),
                        "default_model": self.config["openai"].get("model", "gpt-3.5-turbo"),
                        "settings": self.config["openai"].get("settings", {})
                    }
                    logger.info("OpenAI provider configured successfully")
                except ImportError:
                    logger.warning("OpenAI package not installed")
                except Exception as e:
                    logger.error(f"Error setting up OpenAI: {e}")
        
        # Setup Gemini
        if self.config.get("gemini", {}).get("enabled", False):
            api_key = self.config["gemini"].get("api_key")
            if api_key:
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=api_key)
                    self.providers["gemini"] = {
                        "name": "Google Gemini",
                        "client": genai,
                        "models": self.config["gemini"].get("available_models", []),
                        "default_model": self.config["gemini"].get("model", "gemini-pro"),
                        "settings": self.config["gemini"].get("settings", {})
                    }
                    logger.info("Gemini provider configured successfully")
                except ImportError:
                    logger.warning("Google Generative AI package not installed")
                except Exception as e:
                    logger.error(f"Error setting up Gemini: {e}")
        
        # Setup Anthropic
        if self.config.get("anthropic", {}).get("enabled", False):
            api_key = self.config["anthropic"].get("api_key")
            if api_key:
                try:
                    import anthropic
                    client = anthropic.Anthropic(api_key=api_key)
                    self.providers["anthropic"] = {
                        "name": "Anthropic Claude",
                        "client": client,
                        "models": self.config["anthropic"].get("available_models", []),
                        "default_model": self.config["anthropic"].get("model", "claude-3-opus"),
                        "settings": self.config["anthropic"].get("settings", {})
                    }
                    logger.info("Anthropic provider configured successfully")
                except ImportError:
                    logger.warning("Anthropic package not installed")
                except Exception as e:
                    logger.error(f"Error setting up Anthropic: {e}")
    
    async def get_completion_async(self, prompt: str, provider: Optional[str] = None, 
                                  model: Optional[str] = None, stream: bool = False,
                                  system_prompt: Optional[str] = None) -> Union[str, AsyncGenerator]:
        \"\"\"Get completion from AI provider asynchronously\"\"\"
        if not provider:
            provider = self.config.get("default_provider", "openai")
        
        if provider not in self.providers:
            error_msg = f"Error: Provider '{provider}' not configured or not available"
            logger.error(error_msg)
            return error_msg
        
        if not model:
            model = self.providers[provider]["default_model"]
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": prompt})
        if len(self.conversation_history) > self.max_history * 2:  # *2 because each exchange has user and assistant
            self.conversation_history = self.conversation_history[-self.max_history*2:]
        
        try:
            if provider == "openai":
                return await self._get_openai_completion(prompt, model, stream, system_prompt)
            
            elif provider == "gemini":
                return await self._get_gemini_completion(prompt, model, stream)
            
            elif provider == "anthropic":
                return await self._get_anthropic_completion(prompt, model, stream, system_prompt)
            
            error_msg = f"Provider '{provider}' implementation not complete"
            logger.error(error_msg)
            return error_msg
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            logger.error(f"Error getting completion from {provider}: {e}")
            return error_msg
    
    def get_completion(self, prompt: str, provider: Optional[str] = None, 
                      model: Optional[str] = None, system_prompt: Optional[str] = None) -> str:
        \"\"\"Synchronous wrapper for get_completion_async\"\"\"
        return asyncio.run(self.get_completion_async(prompt, provider, model, False, system_prompt))
    
    async def _get_openai_completion(self, prompt: str, model: str, stream: bool, system_prompt: Optional[str] = None):
        \"\"\"Get completion from OpenAI\"\"\"
        openai_client = self.providers["openai"]["client"].chat.completions
        settings = self.providers["openai"]["settings"]
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation history
        for msg in self.conversation_history:
            messages.append(msg)
        
        response = await openai_client.create(
            model=model,
            messages=messages,
            temperature=settings.get("temperature", 0.7),
            max_tokens=settings.get("max_tokens", 1000),
            top_p=settings.get("top_p", 1.0),
            frequency_penalty=settings.get("frequency_penalty", 0.0),
            presence_penalty=settings.get("presence_penalty", 0.0),
            stream=stream
        )
        
        if stream:
            async def stream_generator():
                async for chunk in response:
                    if chunk.choices and chunk.
