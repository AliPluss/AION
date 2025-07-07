"""
🚀 AION Advanced Features Module

This module contains all advanced features and capabilities of AION:

- 🤖 Automation Recipes: Intelligent task automation and macro recording
- 📤 Export System: Professional document export in 13+ formats
- 🎤 Voice Control: Speech-to-text and text-to-speech capabilities
- 🔒 Sandbox System: Secure code execution environment
- 📝 Code Editor: Advanced syntax highlighting and analysis
- 📁 File Manager: Comprehensive file operations and management

Each feature is designed with enterprise-grade security, performance,
and user experience in mind. All features support multilingual
operation and comprehensive logging.
"""

from .automation_recipes import AutomationRecipes
from .export_system import ExportSystem
from .voice_control import VoiceControl
from .sandbox_system import SandboxSystem
from .code_editor import CodeEditor
from .file_manager import FileManager

__all__ = [
    "AutomationRecipes",
    "ExportSystem",
    "VoiceControl", 
    "SandboxSystem",
    "CodeEditor",
    "FileManager"
]

# Feature availability flags
FEATURES_AVAILABLE = {
    "automation": True,
    "export": True,
    "voice": True,
    "sandbox": True,
    "editor": True,
    "file_manager": True
}

def get_available_features():
    """Get list of available features"""
    return [feature for feature, available in FEATURES_AVAILABLE.items() if available]

def is_feature_available(feature_name: str) -> bool:
    """Check if a specific feature is available"""
    return FEATURES_AVAILABLE.get(feature_name, False)
