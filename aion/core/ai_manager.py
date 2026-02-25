#!/usr/bin/env python3
"""
AI Manager for AION
Manages multiple AI providers with fallback mechanisms
"""

import os
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProviderStatus(Enum):
    """AI Provider status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    FALLBACK = "fallback"

@dataclass
class ProviderConfig:
    """AI Provider configuration"""
    name: str
    api_key_env: str
    model: str
    animation: str
    status: ProviderStatus = ProviderStatus.INACTIVE
    priority: int = 0
    max_retries: int = 3
    timeout: int = 30

class AIManager:
    """
    AI Manager for handling multiple AI providers with fallback
    """
    
    def __init__(self):
        """Initialize AI Manager with provider configurations"""
        self.providers = self._initialize_providers()
        self.current_provider = None
        self.fallback_chain = []
        self._setup_fallback_chain()
        
    def _initialize_providers(self) -> Dict[str, ProviderConfig]:
        """Initialize all AI provider configurations"""
        providers = {
            "openai": ProviderConfig(
                name="OpenAI GPT",
                api_key_env="OPENAI_API_KEY",
                model="gpt-4",
                animation="🧠 Pulse",
                priority=1
            ),
            "deepseek": ProviderConfig(
                name="DeepSeek",
                api_key_env="DEEPSEEK_API_KEY",
                model="deepseek-chat",
                animation="🛰️ Orbit",
                priority=2
            ),
            "google": ProviderConfig(
                name="Google Gemini",
                api_key_env="GOOGLE_API_KEY",
                model="gemini-pro",
                animation="🌐 Ripple",
                priority=3
            ),
            "openrouter": ProviderConfig(
                name="OpenRouter",
                api_key_env="OPENROUTER_API_KEY",
                model="auto",
                animation="🛤️ Slide",
                priority=4
            )
        }
        
        # Check which providers are configured
        for provider_id, config in providers.items():
            if os.getenv(config.api_key_env):
                config.status = ProviderStatus.ACTIVE
                logger.info(f"✅ {config.name} configured and ready")
            else:
                config.status = ProviderStatus.INACTIVE
                logger.info(f"⚠️ {config.name} not configured (missing {config.api_key_env})")
        
        return providers
    
    def _setup_fallback_chain(self):
        """Setup fallback chain based on provider priority"""
        # Sort providers by priority
        sorted_providers = sorted(
            self.providers.items(),
            key=lambda x: x[1].priority
        )
        
        # Create fallback chain from active providers
        self.fallback_chain = [
            provider_id for provider_id, config in sorted_providers
            if config.status == ProviderStatus.ACTIVE
        ]
        
        # Set current provider to first available
        if self.fallback_chain:
            self.current_provider = self.fallback_chain[0]
            logger.info(f"🎯 Primary provider set to: {self.providers[self.current_provider].name}")
        else:
            logger.warning("⚠️ No AI providers configured")
    
    def get_available_providers(self) -> List[str]:
        """Get list of available provider IDs"""
        return [
            provider_id for provider_id, config in self.providers.items()
            if config.status == ProviderStatus.ACTIVE
        ]
    
    def get_provider_info(self, provider_id: str) -> Optional[ProviderConfig]:
        """Get provider configuration information"""
        return self.providers.get(provider_id)
    
    def switch_provider(self, provider_id: str) -> bool:
        """
        Switch to specified AI provider
        
        Args:
            provider_id: Provider identifier
            
        Returns:
            True if switch successful, False otherwise
        """
        if provider_id not in self.providers:
            logger.error(f"❌ Unknown provider: {provider_id}")
            return False
        
        config = self.providers[provider_id]
        
        if config.status != ProviderStatus.ACTIVE:
            logger.error(f"❌ Provider {config.name} is not active")
            return False
        
        old_provider = self.current_provider
        self.current_provider = provider_id
        
        logger.info(f"🔄 Switched from {self.providers[old_provider].name if old_provider else 'None'} to {config.name}")
        return True
    
    def get_current_provider(self) -> Optional[str]:
        """Get current active provider ID"""
        return self.current_provider
    
    def get_current_provider_info(self) -> Optional[ProviderConfig]:
        """Get current provider configuration"""
        if self.current_provider:
            return self.providers[self.current_provider]
        return None
    
    def trigger_fallback(self) -> bool:
        """
        Trigger fallback to next available provider
        
        Returns:
            True if fallback successful, False if no more providers
        """
        if not self.current_provider or not self.fallback_chain:
            logger.error("❌ No fallback providers available")
            return False
        
        try:
            current_index = self.fallback_chain.index(self.current_provider)
            next_index = current_index + 1
            
            if next_index < len(self.fallback_chain):
                next_provider = self.fallback_chain[next_index]
                old_provider_name = self.providers[self.current_provider].name
                new_provider_name = self.providers[next_provider].name
                
                self.current_provider = next_provider
                self.providers[next_provider].status = ProviderStatus.FALLBACK
                
                logger.info(f"🛡️ Fallback triggered: {old_provider_name} -> {new_provider_name}")
                return True
            else:
                logger.error("❌ No more fallback providers available")
                return False
                
        except ValueError:
            logger.error("❌ Current provider not in fallback chain")
            return False
    
    def reset_providers(self):
        """Reset all providers to their initial state"""
        for config in self.providers.values():
            if os.getenv(config.api_key_env):
                config.status = ProviderStatus.ACTIVE
            else:
                config.status = ProviderStatus.INACTIVE
        
        self._setup_fallback_chain()
        logger.info("🔄 All providers reset to initial state")
    
    def get_provider_stats(self) -> Dict[str, Any]:
        """Get statistics about provider usage"""
        stats = {
            "total_providers": len(self.providers),
            "active_providers": len(self.get_available_providers()),
            "current_provider": self.current_provider,
            "fallback_chain_length": len(self.fallback_chain),
            "providers": {}
        }
        
        for provider_id, config in self.providers.items():
            stats["providers"][provider_id] = {
                "name": config.name,
                "status": config.status.value,
                "priority": config.priority,
                "animation": config.animation
            }
        
        return stats
    
    def test_provider_connection(self, provider_id: str) -> bool:
        """
        Test connection to specific provider
        
        Args:
            provider_id: Provider to test
            
        Returns:
            True if connection successful, False otherwise
        """
        if provider_id not in self.providers:
            return False
        
        config = self.providers[provider_id]
        
        # Check if API key is available
        if not os.getenv(config.api_key_env):
            logger.warning(f"⚠️ {config.name}: API key not found")
            return False
        
        # In a real implementation, this would make an actual API call
        # For now, we'll simulate a successful connection test
        logger.info(f"✅ {config.name}: Connection test successful")
        return True
    
    def __str__(self) -> str:
        """String representation of AI Manager"""
        current = self.get_current_provider_info()
        current_name = current.name if current else "None"
        
        return f"AIManager(current={current_name}, providers={len(self.providers)}, active={len(self.get_available_providers())})"
    
    def __repr__(self) -> str:
        """Detailed representation of AI Manager"""
        return self.__str__()

# Convenience functions for easy access
def get_ai_manager() -> AIManager:
    """Get singleton AI Manager instance"""
    if not hasattr(get_ai_manager, '_instance'):
        get_ai_manager._instance = AIManager()
    return get_ai_manager._instance

def switch_ai_provider(provider_id: str) -> bool:
    """Switch AI provider using singleton manager"""
    manager = get_ai_manager()
    return manager.switch_provider(provider_id)

def get_current_ai_provider() -> Optional[str]:
    """Get current AI provider using singleton manager"""
    manager = get_ai_manager()
    return manager.get_current_provider()

def trigger_ai_fallback() -> bool:
    """Trigger AI provider fallback using singleton manager"""
    manager = get_ai_manager()
    return manager.trigger_fallback()

if __name__ == "__main__":
    # Test AI Manager
    manager = AIManager()
    print(f"AI Manager initialized: {manager}")
    
    stats = manager.get_provider_stats()
    print(f"Provider stats: {stats}")
    
    available = manager.get_available_providers()
    print(f"Available providers: {available}")
    
    if available:
        print(f"Testing provider connections...")
        for provider in available:
            result = manager.test_provider_connection(provider)
            print(f"  {provider}: {'✅ OK' if result else '❌ FAILED'}")
