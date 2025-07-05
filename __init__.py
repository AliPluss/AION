"""
🤖 AION - AI Operating Node

A multilingual terminal-based AI assistant with advanced features.
"""

__version__ = "1.0.0"
__author__ = "AION Development Team"
__email__ = "dev@aion-ai.com"
__license__ = "MIT"

# Core imports - handle import errors gracefully
try:
    from . import main
    from .core.ai_providers import AIProviderManager
    from .core.security import SecurityManager
    from .core.plugins import PluginManager
    from .utils.translator import Translator
except ImportError:
    # Fallback to absolute imports
    try:
        import main
        from core.ai_providers import AIProviderManager
        from core.security import SecurityManager
        from core.plugins import PluginManager
        from utils.translator import Translator
    except ImportError:
        # Define minimal interface if imports fail
        main = None
        AIProviderManager = None
        SecurityManager = None
        PluginManager = None
        Translator = None

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "main",
    "AIProviderManager",
    "SecurityManager",
    "PluginManager",
    "Translator"
]
