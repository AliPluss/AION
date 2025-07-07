"""
💻 AION User Interfaces Module

Professional user interface components for AION:

- 💻 CLI: Command Line Interface with rich formatting and multilingual support
- 🖥️ TUI: Terminal User Interface with advanced interactive elements
- 🌐 Web: Web Interface with FastAPI backend and responsive frontend

All interfaces feature:
- Comprehensive multilingual support (7 languages)
- Professional rich text formatting and styling
- Secure session management and authentication
- Real-time system monitoring and status display
- Advanced error handling and user feedback
- Consistent user experience across all modes
- Professional logging and audit trails
"""

from .cli import CLI
from .tui import TUI
from .web import WebInterface

__all__ = [
    "CLI",
    "TUI", 
    "WebInterface"
]

# Interface availability status
INTERFACES_STATUS = {
    "cli": {"available": True, "description": "Command Line Interface"},
    "tui": {"available": True, "description": "Terminal User Interface"},
    "web": {"available": True, "description": "Web Interface"}
}

def get_available_interfaces():
    """Get list of available interfaces"""
    return [name for name, status in INTERFACES_STATUS.items() if status["available"]]

def get_interface_info(interface_name: str) -> dict:
    """Get information about a specific interface"""
    return INTERFACES_STATUS.get(interface_name, {"available": False, "description": "Unknown interface"})
