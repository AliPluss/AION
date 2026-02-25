"""
🤖 AION - AI Operating Node

A professional multilingual terminal-based AI assistant with advanced features.

This package provides comprehensive AI assistance with:
- Multi-provider AI integration (OpenAI, DeepSeek, Gemini, OpenRouter)
- Multilingual support (7 languages with RTL support)
- Advanced security with dynamic encryption
- Professional code execution environment
- Comprehensive system integrations
- Voice control and automation features
- Export capabilities and file management
- Plugin system for extensibility

The AION system is designed for professional use with enterprise-grade
security, performance monitoring, and comprehensive feature set.
"""

__version__ = "2.0.0"
__author__ = "AION Development Team"
__email__ = "project.django.rst@gmail.com"
__license__ = "MIT"
__description__ = "AI Operating Node - Professional Terminal AI Assistant"

# Core imports - handle import errors gracefully
try:
    from .main import app
    from .core.ai_providers import AIProviderManager
    from .core.security import SecurityManager
    from .core.plugins import PluginManager
    from .utils.translator import Translator
    from .interfaces.cli import CLI
    from .interfaces.tui import TUI
    from .interfaces.web import WebInterface
except ImportError:
    # Fallback for development/testing
    app = None
    AIProviderManager = None
    SecurityManager = None
    PluginManager = None
    Translator = None
    CLI = None
    TUI = None
    WebInterface = None

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__description__",
    "app",
    "AIProviderManager",
    "SecurityManager", 
    "PluginManager",
    "Translator",
    "CLI",
    "TUI",
    "WebInterface"
]

# Package metadata for setuptools
PACKAGE_INFO = {
    "name": "aion-ai",
    "version": __version__,
    "description": __description__,
    "author": __author__,
    "author_email": __email__,
    "license": __license__,
    "url": "https://github.com/AliPluss/AION",
    "keywords": ["ai", "assistant", "terminal", "multilingual", "automation"],
    "classifiers": [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Shells",
        "Topic :: Utilities"
    ]
}
