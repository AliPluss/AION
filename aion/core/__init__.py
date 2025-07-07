"""
🧠 AION Core System Module

Core functionality and system components for AION:

- 🤖 AI Providers: Multi-provider AI integration with advanced management
- 🔒 Security: Dynamic security with HMAC+AES encryption and threat monitoring
- 📋 Task Manager: Advanced task scheduling and execution with dependencies
- ⚡ Executor: Professional code execution engine with multi-language support
- 🔌 Plugins: Dynamic plugin system with security validation
- ⚙️ Settings Manager: Comprehensive configuration management

All core modules are designed with enterprise-grade security, performance
monitoring, and comprehensive error handling for production use.
"""

# Import with fallbacks for missing modules
try:
    from .ai_providers import AdvancedAIManager as AIProviderManager
except ImportError:
    AIProviderManager = None

try:
    from .security import SecurityManager
except ImportError:
    SecurityManager = None

try:
    from .task_manager import AdvancedTaskManager as TaskManager
except ImportError:
    TaskManager = None

try:
    from .executor import CodeExecutor
except ImportError:
    CodeExecutor = None

try:
    from .plugins import PluginManager
except ImportError:
    PluginManager = None

try:
    from .settings_manager import SettingsManager
except ImportError:
    SettingsManager = None

__all__ = [
    "AIProviderManager",
    "SecurityManager",
    "TaskManager",
    "CodeExecutor",
    "PluginManager",
    "SettingsManager"
]

# Core system status
CORE_MODULES_STATUS = {
    "ai_providers": AIProviderManager is not None,
    "security": SecurityManager is not None,
    "task_manager": TaskManager is not None,
    "executor": CodeExecutor is not None,
    "plugins": PluginManager is not None,
    "settings_manager": SettingsManager is not None
}

def get_core_status():
    """Get status of all core modules"""
    return CORE_MODULES_STATUS

def is_core_module_available(module_name: str) -> bool:
    """Check if a core module is available"""
    return CORE_MODULES_STATUS.get(module_name, False)
