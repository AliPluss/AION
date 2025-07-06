#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧩 AION Plugin System - Base Plugin Class
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import json
import os

class BasePlugin(ABC):
    """Base class for all AION plugins"""

    def __init__(self):
        self.name = "Unknown Plugin"
        self.version = "1.0.0"
        self.description = "A plugin for AION"
        self.author = "Unknown"
        self.enabled = True
        self.config = {}

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the plugin"""
        pass

    @abstractmethod
    def execute(self, command: str, args: List[str]) -> Dict[str, Any]:
        """Execute plugin command"""
        pass

    @abstractmethod
    def get_commands(self) -> List[str]:
        """Get list of available commands"""
        pass

    def get_info(self) -> Dict[str, Any]:
        """Get plugin information"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "enabled": self.enabled,
            "commands": self.get_commands()
        }

    def load_config(self, config_path: str) -> bool:
        """Load plugin configuration"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading config: {e}")
            return False

    def save_config(self, config_path: str) -> bool:
        """Save plugin configuration"""
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
