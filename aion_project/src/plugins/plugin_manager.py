#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧩 AION Plugin Manager
"""

import os
import sys
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class PluginManager:
    """Manages AION plugins"""

    def __init__(self, plugins_dir: str = "src/plugins"):
        self.plugins_dir = Path(plugins_dir)
        self.loaded_plugins: Dict[str, Any] = {}
        self.plugin_configs: Dict[str, Dict] = {}

    def discover_plugins(self) -> List[str]:
        """Discover available plugins"""
        plugins = []
        if not self.plugins_dir.exists():
            return plugins

        for file_path in self.plugins_dir.glob("*.py"):
            if file_path.name not in ["__init__.py", "base_plugin.py"]:
                plugins.append(file_path.stem)
        return plugins

    def load_plugin(self, plugin_name: str) -> bool:
        """Load a specific plugin"""
        try:
            plugin_path = self.plugins_dir / f"{plugin_name}.py"
            if not plugin_path.exists():
                console.print(f"[red]❌ Plugin {plugin_name} not found[/red]")
                return False

            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find plugin class
            plugin_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and
                    hasattr(attr, 'initialize') and
                    attr_name != 'BasePlugin'):
                    plugin_class = attr
                    break

            if plugin_class:
                plugin_instance = plugin_class()
                if plugin_instance.initialize():
                    self.loaded_plugins[plugin_name] = plugin_instance
                    console.print(f"[green]✅ Plugin {plugin_name} loaded successfully[/green]")
                    return True

            console.print(f"[red]❌ Failed to initialize plugin {plugin_name}[/red]")
            return False

        except Exception as e:
            console.print(f"[red]❌ Error loading plugin {plugin_name}: {e}[/red]")
            return False

    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a specific plugin"""
        if plugin_name in self.loaded_plugins:
            del self.loaded_plugins[plugin_name]
            console.print(f"[yellow]🔄 Plugin {plugin_name} unloaded[/yellow]")
            return True
        return False

    def load_all_plugins(self) -> int:
        """Load all available plugins"""
        plugins = self.discover_plugins()
        loaded_count = 0

        for plugin_name in plugins:
            if self.load_plugin(plugin_name):
                loaded_count += 1

        return loaded_count

    def execute_plugin_command(self, plugin_name: str, command: str, args: List[str]) -> Optional[Dict[str, Any]]:
        """Execute a command from a specific plugin"""
        if plugin_name not in self.loaded_plugins:
            console.print(f"[red]❌ Plugin {plugin_name} not loaded[/red]")
            return None

        try:
            return self.loaded_plugins[plugin_name].execute(command, args)
        except Exception as e:
            console.print(f"[red]❌ Error executing command: {e}[/red]")
            return None

    def list_plugins(self) -> None:
        """Display list of available and loaded plugins"""
        table = Table(title="🧩 AION Plugins")
        table.add_column("Plugin Name", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Version", style="yellow")
        table.add_column("Description", style="white")

        all_plugins = self.discover_plugins()

        for plugin_name in all_plugins:
            if plugin_name in self.loaded_plugins:
                plugin = self.loaded_plugins[plugin_name]
                info = plugin.get_info()
                table.add_row(
                    info["name"],
                    "✅ Loaded",
                    info["version"],
                    info["description"]
                )
            else:
                table.add_row(
                    plugin_name,
                    "❌ Not Loaded",
                    "Unknown",
                    "Plugin not loaded"
                )

        console.print(table)

    def get_plugin_commands(self, plugin_name: str) -> List[str]:
        """Get available commands for a plugin"""
        if plugin_name in self.loaded_plugins:
            return self.loaded_plugins[plugin_name].get_commands()
        return []

    def get_all_commands(self) -> Dict[str, List[str]]:
        """Get all available commands from all loaded plugins"""
        commands = {}
        for plugin_name, plugin in self.loaded_plugins.items():
            commands[plugin_name] = plugin.get_commands()
        return commands
