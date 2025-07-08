"""
🧠 AION AI Engine - Complete AI Integration System
=================================================

This module provides the complete AI engine for AION with:
- Multi-provider AI routing and failover
- Context-aware assistance across all screens
- Comprehensive chat and explanation systems
- Voice input support
- Advanced caching and safety features
- Performance optimization and async processing

Author: AION Development Team
Version: 1.0.0-ai-final-release
"""

from .ai_interface import AIInterface
from .provider_router import ProviderRouter
from .context_manager import ContextManager
from .chat_engine import ChatEngine
from .command_explainer import CommandExplainer
from .ai_logger import AILogger
from .config_loader import ConfigLoader

# Initialize the main AI interface
ai_engine = AIInterface()

__all__ = [
    'AIInterface',
    'ProviderRouter', 
    'ContextManager',
    'ChatEngine',
    'CommandExplainer',
    'AILogger',
    'ConfigLoader',
    'ai_engine'
]

__version__ = "1.0.0-ai-final-release"
