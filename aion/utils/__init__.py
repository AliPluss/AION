"""
🛠️ AION Utilities Module

Core utility functions and helper classes for AION:

- 🌐 Translator: Multilingual support with RTL text handling
- 🇸🇦 Arabic Support: Advanced Arabic text processing and display
- 🔧 Helpers: Common utility functions for file operations, logging, and validation

All utilities are designed with:
- Professional error handling and validation
- Comprehensive logging and debugging support
- Cross-platform compatibility
- Performance optimization
- Security-first approach
- Extensive documentation and examples
"""

from .translator import Translator
from .arabic_support import ArabicSupport
from .helpers import (
    calculate_file_checksum,
    setup_logging,
    validate_path_safety,
    check_dependencies
)

__all__ = [
    "Translator",
    "ArabicSupport",
    "calculate_file_checksum",
    "setup_logging", 
    "validate_path_safety",
    "check_dependencies"
]

# Utility module status
UTILS_STATUS = {
    "translator": True,
    "arabic_support": True,
    "helpers": True
}

def get_utils_status():
    """Get status of all utility modules"""
    return UTILS_STATUS
