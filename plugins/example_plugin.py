"""
🧩 Example AION Plugin
Demonstrates how to create plugins for AION
"""

import asyncio
import datetime
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable

# Import AION plugin base classes
import sys
sys.path.append(str(Path(__file__).parent.parent))

from core.plugins import BasePlugin, CommandPlugin, PluginType

class WeatherPlugin(CommandPlugin):
    """Example weather plugin"""
    
    def __init__(self):
        super().__init__()
        self.name = "Weather Plugin"
        self.version = "1.0.0"
        self.description = "Get weather information (demo plugin)"
        self.author = "AION Team"
        self.dependencies = []
    
    def register_commands(self) -> Dict[str, Callable]:
        """Register weather commands"""
        return {
            "weather": self.get_weather,
            "forecast": self.get_forecast,
            "weather-help": self.show_help
        }
    
    async def get_weather(self, *args) -> str:
        """Get current weather (mock implementation)"""
        city = args[0] if args else "Unknown City"
        
        # Mock weather data
        weather_data = {
            "temperature": "22°C",
            "condition": "Sunny",
            "humidity": "65%",
            "wind": "10 km/h"
        }
        
        return f"""
🌤️ Weather in {city}:
Temperature: {weather_data['temperature']}
Condition: {weather_data['condition']}
Humidity: {weather_data['humidity']}
Wind: {weather_data['wind']}

Note: This is a demo plugin with mock data.
"""
    
    async def get_forecast(self, *args) -> str:
        """Get weather forecast (mock implementation)"""
        city = args[0] if args else "Unknown City"
        days = int(args[1]) if len(args) > 1 and args[1].isdigit() else 3
        
        forecast = []
        for i in range(days):
            date = datetime.datetime.now() + datetime.timedelta(days=i)
            forecast.append(f"{date.strftime('%Y-%m-%d')}: 20-25°C, Partly Cloudy")
        
        return f"""
📅 {days}-day forecast for {city}:
{chr(10).join(forecast)}

Note: This is a demo plugin with mock data.
"""
    
    async def show_help(self, *args) -> str:
        """Show weather plugin help"""
        return """
🌤️ Weather Plugin Help:

Commands:
  weather [city]        - Get current weather
  forecast [city] [days] - Get weather forecast
  weather-help          - Show this help

Examples:
  weather London
  forecast Paris 5
  weather-help
"""
    
    async def cleanup(self):
        """Cleanup plugin resources"""
        pass

class CalculatorPlugin(CommandPlugin):
    """Example calculator plugin"""
    
    def __init__(self):
        super().__init__()
        self.name = "Calculator Plugin"
        self.version = "1.0.0"
        self.description = "Basic calculator functionality"
        self.author = "AION Team"
        self.dependencies = []
    
    def register_commands(self) -> Dict[str, Callable]:
        """Register calculator commands"""
        return {
            "calc": self.calculate,
            "add": self.add,
            "subtract": self.subtract,
            "multiply": self.multiply,
            "divide": self.divide,
            "calc-help": self.show_help
        }
    
    async def calculate(self, *args) -> str:
        """Evaluate mathematical expression"""
        if not args:
            return "❌ Please provide a mathematical expression"
        
        expression = " ".join(args)
        
        try:
            # Simple evaluation (be careful with eval in real applications)
            # This is just for demonstration
            allowed_chars = set("0123456789+-*/.() ")
            if not all(c in allowed_chars for c in expression):
                return "❌ Invalid characters in expression"
            
            result = eval(expression)
            return f"🧮 {expression} = {result}"
        
        except Exception as e:
            return f"❌ Error calculating: {str(e)}"
    
    async def add(self, *args) -> str:
        """Add numbers"""
        if len(args) < 2:
            return "❌ Please provide at least 2 numbers"
        
        try:
            numbers = [float(arg) for arg in args]
            result = sum(numbers)
            return f"➕ {' + '.join(args)} = {result}"
        except ValueError:
            return "❌ Invalid numbers provided"
    
    async def subtract(self, *args) -> str:
        """Subtract numbers"""
        if len(args) != 2:
            return "❌ Please provide exactly 2 numbers"
        
        try:
            a, b = float(args[0]), float(args[1])
            result = a - b
            return f"➖ {args[0]} - {args[1]} = {result}"
        except ValueError:
            return "❌ Invalid numbers provided"
    
    async def multiply(self, *args) -> str:
        """Multiply numbers"""
        if len(args) < 2:
            return "❌ Please provide at least 2 numbers"
        
        try:
            result = 1
            for arg in args:
                result *= float(arg)
            return f"✖️ {' × '.join(args)} = {result}"
        except ValueError:
            return "❌ Invalid numbers provided"
    
    async def divide(self, *args) -> str:
        """Divide numbers"""
        if len(args) != 2:
            return "❌ Please provide exactly 2 numbers"
        
        try:
            a, b = float(args[0]), float(args[1])
            if b == 0:
                return "❌ Cannot divide by zero"
            result = a / b
            return f"➗ {args[0]} ÷ {args[1]} = {result}"
        except ValueError:
            return "❌ Invalid numbers provided"
    
    async def show_help(self, *args) -> str:
        """Show calculator plugin help"""
        return """
🧮 Calculator Plugin Help:

Commands:
  calc <expression>     - Evaluate mathematical expression
  add <numbers...>      - Add numbers
  subtract <a> <b>      - Subtract b from a
  multiply <numbers...> - Multiply numbers
  divide <a> <b>        - Divide a by b
  calc-help            - Show this help

Examples:
  calc 2 + 3 * 4
  add 10 20 30
  subtract 100 25
  multiply 5 6 7
  divide 20 4
"""
    
    async def cleanup(self):
        """Cleanup plugin resources"""
        pass

class SystemInfoPlugin(BasePlugin):
    """Example system information plugin"""
    
    def __init__(self):
        super().__init__()
        self.name = "System Info Plugin"
        self.version = "1.0.0"
        self.description = "Get system information"
        self.author = "AION Team"
        self.plugin_type = PluginType.UTILITY
        self.dependencies = []
    
    async def initialize(self) -> bool:
        """Initialize system info plugin"""
        try:
            import platform
            import psutil
            self.platform = platform
            self.psutil = psutil
            return True
        except ImportError:
            print("⚠️ psutil not installed, some features may not work")
            import platform
            self.platform = platform
            self.psutil = None
            return True
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get basic system information"""
        info = {
            "system": self.platform.system(),
            "release": self.platform.release(),
            "version": self.platform.version(),
            "machine": self.platform.machine(),
            "processor": self.platform.processor(),
            "python_version": self.platform.python_version()
        }
        
        if self.psutil:
            try:
                info.update({
                    "cpu_count": self.psutil.cpu_count(),
                    "memory_total": f"{self.psutil.virtual_memory().total // (1024**3)} GB",
                    "memory_available": f"{self.psutil.virtual_memory().available // (1024**3)} GB",
                    "disk_usage": f"{self.psutil.disk_usage('/').percent}%"
                })
            except Exception:
                pass
        
        return info
    
    def format_system_info(self) -> str:
        """Format system information as string"""
        info = self.get_system_info()
        
        formatted = "💻 System Information:\n"
        formatted += f"OS: {info.get('system', 'Unknown')} {info.get('release', '')}\n"
        formatted += f"Machine: {info.get('machine', 'Unknown')}\n"
        formatted += f"Processor: {info.get('processor', 'Unknown')}\n"
        formatted += f"Python: {info.get('python_version', 'Unknown')}\n"
        
        if 'cpu_count' in info:
            formatted += f"CPU Cores: {info['cpu_count']}\n"
        if 'memory_total' in info:
            formatted += f"Memory: {info['memory_available']} / {info['memory_total']}\n"
        if 'disk_usage' in info:
            formatted += f"Disk Usage: {info['disk_usage']}\n"
        
        return formatted
    
    async def cleanup(self):
        """Cleanup plugin resources"""
        pass

# Plugin registration
# AION will automatically discover and load these plugins
PLUGINS = [
    WeatherPlugin,
    CalculatorPlugin,
    SystemInfoPlugin
]
