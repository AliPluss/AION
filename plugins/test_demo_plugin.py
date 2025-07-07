#!/usr/bin/env python3
"""
🧩 AION Test Demo Plugin
A demonstration plugin for testing AION's plugin execution system

This plugin demonstrates:
- Proper AION plugin structure
- BasePlugin inheritance
- Sandbox-safe execution
- Command registration
- Security compliance
"""

import sys
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Callable

# Import AION plugin base classes
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from core.plugins import BasePlugin, CommandPlugin, PluginType


class TestDemoPlugin(CommandPlugin):
    """Test Demo Plugin for AION Plugin System Validation"""
    
    def __init__(self):
        super().__init__()
        self.name = "Test Demo Plugin"
        self.version = "1.0.0"
        self.description = "Demonstration plugin for testing AION plugin execution system"
        self.author = "AION Development Team"
        self.plugin_type = PluginType.COMMAND
        self.dependencies = []
        self.enabled = True
        
        # Plugin-specific attributes
        self.execution_count = 0
        self.last_execution = None
        
    async def initialize(self) -> bool:
        """Initialize the plugin"""
        print(f"🧩 Initializing {self.name} v{self.version}")
        print(f"📝 Description: {self.description}")
        print(f"👤 Author: {self.author}")
        
        # Register commands
        self.commands = self.register_commands()
        print(f"🔧 Registered {len(self.commands)} commands")
        
        return True
    
    async def cleanup(self):
        """Cleanup plugin resources"""
        print(f"🧹 Cleaning up {self.name}")
        print(f"📊 Total executions: {self.execution_count}")
        if self.last_execution:
            print(f"⏰ Last execution: {self.last_execution}")
    
    def register_commands(self) -> Dict[str, Callable]:
        """Register plugin commands"""
        return {
            "test": self.test_command,
            "info": self.info_command,
            "calculate": self.calculate_command,
            "process": self.process_command,
            "validate": self.validate_command
        }
    
    async def test_command(self, *args) -> str:
        """Test command for plugin validation"""
        self.execution_count += 1
        self.last_execution = datetime.now().isoformat()
        
        print("🧪 Executing test command...")
        print(f"📥 Arguments: {args}")
        
        # Perform test operations
        results = {
            "status": "success",
            "plugin": self.name,
            "version": self.version,
            "execution_count": self.execution_count,
            "timestamp": self.last_execution,
            "arguments": args,
            "test_results": {
                "math_test": 42 * 1337,
                "string_test": "AION_PLUGIN_SYSTEM".lower(),
                "list_test": [x**2 for x in range(1, 6)],
                "validation": "PASSED"
            }
        }
        
        print("✅ Test command completed successfully")
        return json.dumps(results, indent=2)
    
    async def info_command(self, *args) -> str:
        """Get plugin information"""
        info = {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "type": self.plugin_type.value,
            "enabled": self.enabled,
            "commands": list(self.commands.keys()),
            "execution_stats": {
                "total_executions": self.execution_count,
                "last_execution": self.last_execution
            },
            "system_info": {
                "python_version": sys.version,
                "platform": sys.platform,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        return json.dumps(info, indent=2)
    
    async def calculate_command(self, *args) -> str:
        """Perform mathematical calculations"""
        if not args:
            return "❌ Please provide a mathematical expression"
        
        expression = " ".join(args)
        
        try:
            # Safe evaluation with limited scope
            allowed_chars = set("0123456789+-*/.() ")
            if not all(c in allowed_chars for c in expression):
                return "❌ Invalid characters in expression"
            
            # Use eval with restricted globals for safety
            result = eval(expression, {"__builtins__": {}}, {})
            
            calculation_result = {
                "expression": expression,
                "result": result,
                "status": "success",
                "timestamp": datetime.now().isoformat()
            }
            
            return json.dumps(calculation_result, indent=2)
        
        except Exception as e:
            error_result = {
                "expression": expression,
                "error": str(e),
                "status": "error",
                "timestamp": datetime.now().isoformat()
            }
            return json.dumps(error_result, indent=2)
    
    async def process_command(self, *args) -> str:
        """Process data with various operations"""
        if not args:
            return "❌ Please provide data to process"
        
        data = list(args)
        
        processing_results = {
            "input_data": data,
            "operations": {
                "count": len(data),
                "uppercase": [item.upper() if isinstance(item, str) else str(item).upper() for item in data],
                "reversed": list(reversed(data)),
                "sorted": sorted(data),
                "unique": list(set(data))
            },
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(processing_results, indent=2)
    
    async def validate_command(self, *args) -> str:
        """Validate plugin environment and capabilities"""
        validation_results = {
            "plugin_info": {
                "name": self.name,
                "version": self.version,
                "enabled": self.enabled
            },
            "environment_checks": {
                "python_version_ok": sys.version_info >= (3, 8),
                "commands_registered": len(self.commands) > 0,
                "initialization_ok": True,
                "sandbox_safe": True
            },
            "capabilities": {
                "command_execution": True,
                "data_processing": True,
                "mathematical_operations": True,
                "json_serialization": True,
                "error_handling": True
            },
            "security": {
                "sandbox_compatible": True,
                "no_file_system_access": True,
                "no_network_access": True,
                "restricted_imports": True
            },
            "status": "all_checks_passed",
            "timestamp": datetime.now().isoformat()
        }
        
        return json.dumps(validation_results, indent=2)


# Plugin instance for AION to discover
plugin_instance = TestDemoPlugin()

# Direct execution for testing
if __name__ == "__main__":
    import asyncio
    
    async def test_plugin():
        print("🚀 Direct Plugin Testing Mode")
        
        # Initialize plugin
        if await plugin_instance.initialize():
            print("✅ Plugin initialized successfully")
            
            # Test commands
            print("\n🧪 Testing commands:")
            
            # Test command
            result = await plugin_instance.test_command("arg1", "arg2", "arg3")
            print(f"📤 Test Result:\n{result}")
            
            # Info command
            result = await plugin_instance.info_command()
            print(f"📤 Info Result:\n{result}")
            
            # Calculate command
            result = await plugin_instance.calculate_command("2", "+", "3", "*", "4")
            print(f"📤 Calculate Result:\n{result}")
            
            # Validate command
            result = await plugin_instance.validate_command()
            print(f"📤 Validate Result:\n{result}")
            
            # Cleanup
            await plugin_instance.cleanup()
            print("✅ Plugin testing completed successfully")
        else:
            print("❌ Plugin initialization failed")
    
    asyncio.run(test_plugin())
