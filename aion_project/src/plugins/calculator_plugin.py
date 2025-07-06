#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧮 Calculator Plugin for AION
"""

from src.plugins.base_plugin import BasePlugin
from typing import Dict, List, Any
import math

class CalculatorPlugin(BasePlugin):
    """Simple calculator plugin"""

    def __init__(self):
        super().__init__()
        self.name = "Calculator"
        self.version = "1.0.0"
        self.description = "Simple calculator with basic math operations"
        self.author = "AION Team"

    def initialize(self) -> bool:
        """Initialize calculator plugin"""
        return True

    def execute(self, command: str, args: List[str]) -> Dict[str, Any]:
        """Execute calculator command"""
        try:
            if command == "add" and len(args) >= 2:
                result = sum(float(arg) for arg in args)
                return {"success": True, "result": result, "operation": "addition"}

            elif command == "subtract" and len(args) == 2:
                result = float(args[0]) - float(args[1])
                return {"success": True, "result": result, "operation": "subtraction"}

            elif command == "multiply" and len(args) >= 2:
                result = 1
                for arg in args:
                    result *= float(arg)
                return {"success": True, "result": result, "operation": "multiplication"}

            elif command == "divide" and len(args) == 2:
                if float(args[1]) == 0:
                    return {"success": False, "error": "Division by zero"}
                result = float(args[0]) / float(args[1])
                return {"success": True, "result": result, "operation": "division"}

            elif command == "sqrt" and len(args) == 1:
                result = math.sqrt(float(args[0]))
                return {"success": True, "result": result, "operation": "square root"}

            elif command == "power" and len(args) == 2:
                result = float(args[0]) ** float(args[1])
                return {"success": True, "result": result, "operation": "power"}

            else:
                return {"success": False, "error": "Invalid command or arguments"}

        except ValueError:
            return {"success": False, "error": "Invalid number format"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_commands(self) -> List[str]:
        """Get available calculator commands"""
        return ["add", "subtract", "multiply", "divide", "sqrt", "power"]
