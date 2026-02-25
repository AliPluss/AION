"""
⚙️ Config Loader - YAML Configuration Management for AI Engine
==============================================================

Loads settings from config.yaml and environment variables for AI providers,
features, and system configuration with validation and defaults.
"""

import os
import yaml
import logging
from typing import Dict, Any, Optional, Union, List
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class AIProviderConfig:
    """Configuration for individual AI provider"""
    name: str
    api_key: str
    base_url: str
    model: str
    max_tokens: int
    temperature: float
    enabled: bool = True

@dataclass
class AIEngineConfig:
    """Complete AI engine configuration"""
    providers: Dict[str, AIProviderConfig]
    default_provider: str
    features: Dict[str, bool]
    performance: Dict[str, Any]
    security: Dict[str, Any]
    logging: Dict[str, Any]

class ConfigLoader:
    """Configuration loader with validation and environment support"""
    
    def __init__(self, config_file: str = "config.yaml"):
        """Initialize configuration loader"""
        self.config_file = Path(config_file)
        self.config_data = {}
        self.env_loaded = False
        
        # Load environment variables
        self._load_environment()
        
        # Load configuration
        self._load_config()
        
        # Validate configuration
        self._validate_config()
        
        logging.info(f"Configuration loaded from {self.config_file}")
    
    def _load_environment(self):
        """Load environment variables from .env file"""
        try:
            # Load from .env file if it exists
            env_file = Path(".env")
            if env_file.exists():
                load_dotenv(env_file)
                self.env_loaded = True
                logging.info("Environment variables loaded from .env file")
            else:
                logging.info("No .env file found, using system environment variables")
                
        except Exception as e:
            logging.warning(f"Failed to load environment variables: {e}")
    
    def _load_config(self):
        """Load configuration from YAML file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config_data = yaml.safe_load(f) or {}
                logging.info(f"Configuration loaded from {self.config_file}")
            else:
                # Create default configuration
                self.config_data = self._create_default_config()
                self._save_config()
                logging.info(f"Created default configuration at {self.config_file}")
                
        except Exception as e:
            logging.error(f"Failed to load configuration: {e}")
            self.config_data = self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration"""
        return {
            "ai_engine": {
                "default_provider": "openai",
                "features": {
                    "chat": True,
                    "search": True,
                    "voice": True,
                    "command_explanation": True,
                    "context_awareness": True,
                    "safety_layer": True
                },
                "performance": {
                    "max_concurrent_requests": 5,
                    "request_timeout": 30,
                    "cache_enabled": True,
                    "cache_ttl": 3600
                },
                "security": {
                    "dangerous_command_detection": True,
                    "require_confirmation": True,
                    "safety_warnings": True,
                    "command_logging": True
                },
                "logging": {
                    "level": "INFO",
                    "max_log_size": "10MB",
                    "backup_count": 5,
                    "async_logging": True
                }
            },
            "providers": {
                "openai": {
                    "model": "gpt-3.5-turbo",
                    "max_tokens": 2000,
                    "temperature": 0.7,
                    "enabled": True
                },
                "deepseek": {
                    "model": "deepseek-chat",
                    "max_tokens": 2000,
                    "temperature": 0.7,
                    "enabled": True
                },
                "anthropic": {
                    "model": "claude-3-sonnet-20240229",
                    "max_tokens": 2000,
                    "temperature": 0.7,
                    "enabled": True
                },
                "google": {
                    "model": "gemini-pro",
                    "max_tokens": 2000,
                    "temperature": 0.7,
                    "enabled": True
                },
                "openrouter": {
                    "model": "openai/gpt-3.5-turbo",
                    "max_tokens": 2000,
                    "temperature": 0.7,
                    "enabled": True
                }
            },
            "interface": {
                "language": "english",
                "theme": "dark",
                "animations": True,
                "arrow_navigation": True,
                "inline_icons": True
            }
        }
    
    def _validate_config(self):
        """Validate configuration structure and values"""
        try:
            # Validate AI engine section
            if "ai_engine" not in self.config_data:
                self.config_data["ai_engine"] = self._create_default_config()["ai_engine"]
            
            # Validate providers section
            if "providers" not in self.config_data:
                self.config_data["providers"] = self._create_default_config()["providers"]
            
            # Validate default provider exists
            default_provider = self.get_ai_config("default_provider", "openai")
            if default_provider not in self.config_data["providers"]:
                self.config_data["ai_engine"]["default_provider"] = "openai"
                logging.warning(f"Default provider '{default_provider}' not found, using 'openai'")
            
            # Validate API keys
            missing_keys = []
            for provider_name, provider_config in self.config_data["providers"].items():
                if provider_config.get("enabled", True):
                    api_key = self.get(f"{provider_name.upper()}_API_KEY")
                    if not api_key:
                        missing_keys.append(provider_name)
            
            if missing_keys:
                logging.warning(f"Missing API keys for providers: {', '.join(missing_keys)}")
            
            logging.info("Configuration validation completed")
            
        except Exception as e:
            logging.error(f"Configuration validation failed: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with environment variable override"""
        # Check environment variables first
        env_value = os.getenv(key)
        if env_value is not None:
            return env_value
        
        # Check configuration file
        keys = key.lower().split('.')
        value = self.config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_ai_config(self, key: str, default: Any = None) -> Any:
        """Get AI engine specific configuration"""
        return self.get(f"ai_engine.{key}", default)
    
    def get_provider_config(self, provider: str, key: str, default: Any = None) -> Any:
        """Get provider specific configuration"""
        return self.get(f"providers.{provider}.{key}", default)
    
    def get_interface_config(self, key: str, default: Any = None) -> Any:
        """Get interface specific configuration"""
        return self.get(f"interface.{key}", default)
    
    def get_ai_engine_config(self) -> AIEngineConfig:
        """Get complete AI engine configuration"""
        providers = {}
        
        for provider_name, provider_data in self.config_data.get("providers", {}).items():
            api_key = self.get(f"{provider_name.upper()}_API_KEY", "")
            
            providers[provider_name] = AIProviderConfig(
                name=provider_name,
                api_key=api_key,
                base_url=self._get_provider_base_url(provider_name),
                model=provider_data.get("model", "gpt-3.5-turbo"),
                max_tokens=provider_data.get("max_tokens", 2000),
                temperature=provider_data.get("temperature", 0.7),
                enabled=provider_data.get("enabled", True) and bool(api_key)
            )
        
        return AIEngineConfig(
            providers=providers,
            default_provider=self.get_ai_config("default_provider", "openai"),
            features=self.get_ai_config("features", {}),
            performance=self.get_ai_config("performance", {}),
            security=self.get_ai_config("security", {}),
            logging=self.get_ai_config("logging", {})
        )
    
    def _get_provider_base_url(self, provider: str) -> str:
        """Get base URL for AI provider"""
        urls = {
            "openai": "https://api.openai.com/v1/chat/completions",
            "deepseek": "https://api.deepseek.com/v1/chat/completions",
            "anthropic": "https://api.anthropic.com/v1/messages",
            "google": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            "openrouter": "https://openrouter.ai/api/v1/chat/completions"
        }
        return urls.get(provider, "")
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.lower().split('.')
        config = self.config_data
        
        # Navigate to parent
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set value
        config[keys[-1]] = value
        
        # Save configuration
        self._save_config()
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled"""
        return self.get_ai_config(f"features.{feature}", True)
    
    def get_provider_list(self) -> List[str]:
        """Get list of available providers"""
        return list(self.config_data.get("providers", {}).keys())
    
    def get_enabled_providers(self) -> List[str]:
        """Get list of enabled providers with API keys"""
        enabled = []
        for provider_name, provider_config in self.config_data.get("providers", {}).items():
            if provider_config.get("enabled", True):
                api_key = self.get(f"{provider_name.upper()}_API_KEY")
                if api_key:
                    enabled.append(provider_name)
        return enabled
    
    def _save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.config_data, f, default_flow_style=False, indent=2, allow_unicode=True)
            logging.debug(f"Configuration saved to {self.config_file}")
        except Exception as e:
            logging.error(f"Failed to save configuration: {e}")
    
    def reload(self):
        """Reload configuration from file"""
        self._load_config()
        self._validate_config()
        logging.info("Configuration reloaded")
    
    def export_config(self, export_file: str):
        """Export configuration to file"""
        try:
            export_path = Path(export_file)
            with open(export_path, 'w') as f:
                yaml.dump(self.config_data, f, default_flow_style=False, indent=2)
            logging.info(f"Configuration exported to {export_path}")
        except Exception as e:
            logging.error(f"Failed to export configuration: {e}")
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get configuration summary"""
        enabled_providers = self.get_enabled_providers()
        
        return {
            "config_file": str(self.config_file),
            "env_loaded": self.env_loaded,
            "default_provider": self.get_ai_config("default_provider"),
            "enabled_providers": enabled_providers,
            "total_providers": len(self.get_provider_list()),
            "features_enabled": sum(1 for f in self.get_ai_config("features", {}).values() if f),
            "cache_enabled": self.get_ai_config("performance.cache_enabled", True),
            "safety_enabled": self.get_ai_config("security.dangerous_command_detection", True)
        }

# Global config loader instance
config_loader = ConfigLoader()
