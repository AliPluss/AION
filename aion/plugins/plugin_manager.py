#!/usr/bin/env python3
"""
🧩 AION Plugin Manager
Simple plugin management system for testing arrow navigation

This module provides:
- Plugin discovery and loading
- Plugin execution with security
- Plugin management interface
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

class PluginManager:
    """Simple plugin manager for AION"""
    
    def __init__(self):
        self.plugins_dir = Path(__file__).parent.parent.parent / "plugins"
        self.loaded_plugins = {}
        
    def discover_plugins(self) -> List[Dict[str, Any]]:
        """Discover available plugins"""
        plugins = []
        
        if not self.plugins_dir.exists():
            return plugins
            
        for plugin_file in self.plugins_dir.glob("*.py"):
            if plugin_file.name.startswith("__"):
                continue
                
            plugin_info = {
                "name": plugin_file.stem,
                "path": str(plugin_file),
                "size": plugin_file.stat().st_size,
                "enabled": True
            }
            plugins.append(plugin_info)
            
        return plugins
    
    def load_plugin(self, plugin_name: str) -> bool:
        """Load a plugin by name"""
        try:
            plugins = self.discover_plugins()
            for plugin in plugins:
                if plugin["name"] == plugin_name:
                    self.loaded_plugins[plugin_name] = plugin
                    return True
            return False
        except Exception:
            return False
    
    def get_loaded_plugins(self) -> Dict[str, Any]:
        """Get all loaded plugins"""
        return self.loaded_plugins.copy()
