"""
🧩 AION Plugin System
Extensible plugin architecture for AION
"""

import os
import sys
import json
import importlib
import importlib.util
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio

class PluginType(Enum):
    """Plugin types"""
    COMMAND = "command"
    AI_PROVIDER = "ai_provider"
    EXECUTOR = "executor"
    INTERFACE = "interface"
    UTILITY = "utility"

@dataclass
class PluginInfo:
    """Plugin information"""
    name: str
    version: str
    description: str
    author: str
    plugin_type: PluginType
    dependencies: List[str]
    enabled: bool = True
    file_path: Optional[str] = None

class BasePlugin(ABC):
    """Base class for all plugins"""
    
    def __init__(self):
        self.name = "Unknown Plugin"
        self.version = "1.0.0"
        self.description = "A plugin for AION"
        self.author = "Unknown"
        self.plugin_type = PluginType.UTILITY
        self.dependencies = []
        self.enabled = True
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the plugin"""
        pass
    
    @abstractmethod
    async def cleanup(self):
        """Cleanup plugin resources"""
        pass
    
    def get_info(self) -> PluginInfo:
        """Get plugin information"""
        return PluginInfo(
            name=self.name,
            version=self.version,
            description=self.description,
            author=self.author,
            plugin_type=self.plugin_type,
            dependencies=self.dependencies,
            enabled=self.enabled
        )

class CommandPlugin(BasePlugin):
    """Base class for command plugins"""
    
    def __init__(self):
        super().__init__()
        self.plugin_type = PluginType.COMMAND
        self.commands = {}
    
    @abstractmethod
    def register_commands(self) -> Dict[str, Callable]:
        """Register plugin commands"""
        pass
    
    async def initialize(self) -> bool:
        """Initialize command plugin"""
        try:
            self.commands = self.register_commands()
            return True
        except Exception as e:
            print(f"Error initializing command plugin {self.name}: {e}")
            return False

class AIProviderPlugin(BasePlugin):
    """Base class for AI provider plugins"""
    
    def __init__(self):
        super().__init__()
        self.plugin_type = PluginType.AI_PROVIDER
    
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate AI response"""
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Get available models"""
        pass

class ExecutorPlugin(BasePlugin):
    """Base class for executor plugins"""
    
    def __init__(self):
        super().__init__()
        self.plugin_type = PluginType.EXECUTOR
    
    @abstractmethod
    async def execute_code(self, code: str, language: str, **kwargs) -> Dict[str, Any]:
        """Execute code"""
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        """Get supported languages"""
        pass

class PluginManager:
    """Plugin manager for AION"""
    
    def __init__(self):
        self.plugins: Dict[str, BasePlugin] = {}
        self.plugin_info: Dict[str, PluginInfo] = {}
        self.plugin_dirs = [
            Path(__file__).parent.parent / "plugins",
            Path.home() / ".aion" / "plugins"
        ]
        
        # Create plugin directories if they don't exist
        for plugin_dir in self.plugin_dirs:
            plugin_dir.mkdir(parents=True, exist_ok=True)
        
        self.load_config()
    
    def load_config(self):
        """Load plugin configuration"""
        config_file = Path.home() / ".aion" / "plugins_config.json"
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"Error loading plugin config: {e}")
                self.config = {}
        else:
            self.config = {}
    
    def save_config(self):
        """Save plugin configuration"""
        config_file = Path.home() / ".aion" / "plugins_config.json"
        
        try:
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving plugin config: {e}")
    
    async def discover_plugins(self):
        """Discover plugins in plugin directories"""
        for plugin_dir in self.plugin_dirs:
            if not plugin_dir.exists():
                continue
            
            for plugin_file in plugin_dir.glob("*.py"):
                if plugin_file.name.startswith("__"):
                    continue
                
                await self._load_plugin_file(plugin_file)
    
    async def _load_plugin_file(self, plugin_file: Path):
        """Load a plugin from file"""
        try:
            # Load module
            spec = importlib.util.spec_from_file_location(
                plugin_file.stem, plugin_file
            )
            if spec is None or spec.loader is None:
                return
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find plugin classes
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                
                if (isinstance(attr, type) and 
                    issubclass(attr, BasePlugin) and 
                    attr != BasePlugin):
                    
                    # Create plugin instance
                    plugin = attr()
                    plugin_info = plugin.get_info()
                    plugin_info.file_path = str(plugin_file)
                    
                    # Check if plugin is enabled in config
                    plugin_config = self.config.get(plugin_info.name, {})
                    plugin.enabled = plugin_config.get("enabled", True)
                    
                    if plugin.enabled:
                        # Initialize plugin
                        if await plugin.initialize():
                            self.plugins[plugin_info.name] = plugin
                            self.plugin_info[plugin_info.name] = plugin_info
                            print(f"✅ Loaded plugin: {plugin_info.name} v{plugin_info.version}")
                        else:
                            print(f"❌ Failed to initialize plugin: {plugin_info.name}")
                    else:
                        print(f"⏸️ Plugin disabled: {plugin_info.name}")
                        self.plugin_info[plugin_info.name] = plugin_info
                    
                    break
                    
        except Exception as e:
            print(f"Error loading plugin {plugin_file}: {e}")
    
    def get_plugins(self, plugin_type: Optional[PluginType] = None) -> List[PluginInfo]:
        """Get list of plugins, optionally filtered by type"""
        plugins = list(self.plugin_info.values())
        
        if plugin_type:
            plugins = [p for p in plugins if p.plugin_type == plugin_type]
        
        return plugins
    
    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """Get a specific plugin by name"""
        return self.plugins.get(name)
    
    def enable_plugin(self, name: str) -> bool:
        """Enable a plugin"""
        if name in self.plugin_info:
            self.config[name] = self.config.get(name, {})
            self.config[name]["enabled"] = True
            self.save_config()
            
            # If plugin is not loaded, try to load it
            if name not in self.plugins:
                plugin_info = self.plugin_info[name]
                if plugin_info.file_path:
                    asyncio.create_task(self._load_plugin_file(Path(plugin_info.file_path)))
            
            return True
        return False
    
    def disable_plugin(self, name: str) -> bool:
        """Disable a plugin"""
        if name in self.plugin_info:
            self.config[name] = self.config.get(name, {})
            self.config[name]["enabled"] = False
            self.save_config()
            
            # Cleanup plugin if loaded
            if name in self.plugins:
                plugin = self.plugins[name]
                asyncio.create_task(plugin.cleanup())
                del self.plugins[name]
                plugin.enabled = False
            
            return True
        return False
    
    def get_command_plugins(self) -> Dict[str, CommandPlugin]:
        """Get all command plugins"""
        return {
            name: plugin for name, plugin in self.plugins.items()
            if isinstance(plugin, CommandPlugin)
        }
    
    def get_ai_provider_plugins(self) -> Dict[str, AIProviderPlugin]:
        """Get all AI provider plugins"""
        return {
            name: plugin for name, plugin in self.plugins.items()
            if isinstance(plugin, AIProviderPlugin)
        }
    
    def get_executor_plugins(self) -> Dict[str, ExecutorPlugin]:
        """Get all executor plugins"""
        return {
            name: plugin for name, plugin in self.plugins.items()
            if isinstance(plugin, ExecutorPlugin)
        }
    
    async def install_plugin(self, plugin_path: str) -> bool:
        """Install a plugin from file or URL"""
        try:
            plugin_file = Path(plugin_path)
            
            if plugin_file.exists():
                # Copy to plugins directory
                target_dir = self.plugin_dirs[1]  # User plugins directory
                target_file = target_dir / plugin_file.name
                
                import shutil
                shutil.copy2(plugin_file, target_file)
                
                # Load the plugin
                await self._load_plugin_file(target_file)
                return True
            else:
                print(f"Plugin file not found: {plugin_path}")
                return False
                
        except Exception as e:
            print(f"Error installing plugin: {e}")
            return False
    
    async def uninstall_plugin(self, name: str) -> bool:
        """Uninstall a plugin"""
        try:
            if name in self.plugin_info:
                plugin_info = self.plugin_info[name]
                
                # Cleanup plugin
                if name in self.plugins:
                    await self.plugins[name].cleanup()
                    del self.plugins[name]
                
                # Remove plugin file if in user directory
                if plugin_info.file_path:
                    plugin_file = Path(plugin_info.file_path)
                    user_plugins_dir = self.plugin_dirs[1]
                    
                    if plugin_file.parent == user_plugins_dir:
                        plugin_file.unlink()
                
                # Remove from config
                if name in self.config:
                    del self.config[name]
                    self.save_config()
                
                del self.plugin_info[name]
                return True
            
            return False
            
        except Exception as e:
            print(f"Error uninstalling plugin: {e}")
            return False
    
    async def cleanup_all(self):
        """Cleanup all plugins"""
        for plugin in self.plugins.values():
            try:
                await plugin.cleanup()
            except Exception as e:
                print(f"Error cleaning up plugin {plugin.name}: {e}")

# Example plugins for demonstration

class ExampleCommandPlugin(CommandPlugin):
    """Example command plugin"""
    
    def __init__(self):
        super().__init__()
        self.name = "Example Commands"
        self.version = "1.0.0"
        self.description = "Example command plugin for AION"
        self.author = "AION Team"
    
    def register_commands(self) -> Dict[str, Callable]:
        """Register example commands"""
        return {
            "hello": self.hello_command,
            "time": self.time_command
        }
    
    async def hello_command(self, *args) -> str:
        """Hello world command"""
        name = args[0] if args else "World"
        return f"Hello, {name}! 👋"
    
    async def time_command(self, *args) -> str:
        """Current time command"""
        import datetime
        return f"Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    async def cleanup(self):
        """Cleanup resources"""
        pass

class ExampleUtilityPlugin(BasePlugin):
    """Example utility plugin"""
    
    def __init__(self):
        super().__init__()
        self.name = "Example Utilities"
        self.version = "1.0.0"
        self.description = "Example utility plugin for AION"
        self.author = "AION Team"
        self.plugin_type = PluginType.UTILITY
    
    async def initialize(self) -> bool:
        """Initialize utility plugin"""
        print(f"Initializing {self.name}")
        return True
    
    async def cleanup(self):
        """Cleanup resources"""
        print(f"Cleaning up {self.name}")
    
    def format_text(self, text: str, style: str = "normal") -> str:
        """Format text with different styles"""
        if style == "upper":
            return text.upper()
        elif style == "lower":
            return text.lower()
        elif style == "title":
            return text.title()
        else:
            return text
