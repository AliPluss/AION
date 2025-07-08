"""
🔌 Provider Router - Multi-AI Provider Management with Failover
==============================================================

Manages multiple AI providers (OpenAI, DeepSeek, Anthropic, Google, OpenRouter)
with intelligent routing, failover, and load balancing capabilities.
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

class ProviderStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    RATE_LIMITED = "rate_limited"

@dataclass
class ProviderConfig:
    name: str
    api_key: str
    base_url: str
    model: str
    max_tokens: int
    temperature: float
    status: ProviderStatus = ProviderStatus.INACTIVE
    last_used: Optional[datetime] = None
    error_count: int = 0
    rate_limit_reset: Optional[datetime] = None

class ProviderRouter:
    """Intelligent AI provider routing with failover and load balancing"""
    
    def __init__(self, config_loader):
        """Initialize provider router with configuration"""
        self.config_loader = config_loader
        self.providers: Dict[str, ProviderConfig] = {}
        self.current_provider = None
        self.session = None
        
        # Performance tracking
        self.request_counts = {}
        self.response_times = {}
        self.error_counts = {}
        
        # Initialize providers
        self._initialize_providers()
        
        # Start health check task
        self.health_check_task = None
        
    def _initialize_providers(self):
        """Initialize all AI providers from configuration"""
        
        # OpenAI Configuration
        self.providers["openai"] = ProviderConfig(
            name="openai",
            api_key=self.config_loader.get("OPENAI_API_KEY", ""),
            base_url="https://api.openai.com/v1/chat/completions",
            model="gpt-3.5-turbo",
            max_tokens=2000,
            temperature=0.7
        )
        
        # DeepSeek Configuration
        self.providers["deepseek"] = ProviderConfig(
            name="deepseek",
            api_key=self.config_loader.get("DEEPSEEK_API_KEY", ""),
            base_url="https://api.deepseek.com/v1/chat/completions",
            model="deepseek-chat",
            max_tokens=2000,
            temperature=0.7
        )
        
        # Anthropic Configuration
        self.providers["anthropic"] = ProviderConfig(
            name="anthropic",
            api_key=self.config_loader.get("ANTHROPIC_API_KEY", ""),
            base_url="https://api.anthropic.com/v1/messages",
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            temperature=0.7
        )
        
        # Google Configuration
        self.providers["google"] = ProviderConfig(
            name="google",
            api_key=self.config_loader.get("GOOGLE_API_KEY", ""),
            base_url="https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            model="gemini-pro",
            max_tokens=2000,
            temperature=0.7
        )
        
        # OpenRouter Configuration
        self.providers["openrouter"] = ProviderConfig(
            name="openrouter",
            api_key=self.config_loader.get("OPENROUTER_API_KEY", ""),
            base_url="https://openrouter.ai/api/v1/chat/completions",
            model="openai/gpt-3.5-turbo",
            max_tokens=2000,
            temperature=0.7
        )
        
        # Set default provider
        self.current_provider = self._select_best_provider()
        
        # Initialize request tracking
        for provider_name in self.providers.keys():
            self.request_counts[provider_name] = 0
            self.response_times[provider_name] = []
            self.error_counts[provider_name] = 0
    
    async def query(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Send query to current AI provider with failover"""
        
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        # Try current provider first
        result = await self._try_provider(self.current_provider, prompt, context)
        
        if result["success"]:
            return result["response"]
        
        # Failover to other providers
        for provider_name, provider in self.providers.items():
            if provider_name != self.current_provider and provider.status == ProviderStatus.ACTIVE:
                result = await self._try_provider(provider_name, prompt, context)
                if result["success"]:
                    # Switch to working provider
                    self.current_provider = provider_name
                    return result["response"]
        
        # All providers failed
        return "⚠️ All AI providers are currently unavailable. Please try again later."
    
    async def _try_provider(self, provider_name: str, prompt: str, context: Optional[Dict] = None) -> Dict:
        """Try to get response from specific provider"""
        
        if provider_name not in self.providers:
            return {"success": False, "error": "Provider not found"}
        
        provider = self.providers[provider_name]
        
        # Check if provider is available
        if provider.status != ProviderStatus.ACTIVE:
            if not await self._check_provider_health(provider_name):
                return {"success": False, "error": "Provider unavailable"}
        
        # Check rate limiting
        if provider.rate_limit_reset and datetime.now() < provider.rate_limit_reset:
            return {"success": False, "error": "Rate limited"}
        
        try:
            start_time = datetime.now()
            
            # Prepare request based on provider
            if provider_name == "openai":
                response = await self._query_openai(provider, prompt, context)
            elif provider_name == "deepseek":
                response = await self._query_deepseek(provider, prompt, context)
            elif provider_name == "anthropic":
                response = await self._query_anthropic(provider, prompt, context)
            elif provider_name == "google":
                response = await self._query_google(provider, prompt, context)
            elif provider_name == "openrouter":
                response = await self._query_openrouter(provider, prompt, context)
            else:
                return {"success": False, "error": "Unknown provider"}
            
            # Track performance
            response_time = (datetime.now() - start_time).total_seconds()
            self.request_counts[provider_name] += 1
            self.response_times[provider_name].append(response_time)
            
            # Update provider status
            provider.last_used = datetime.now()
            provider.error_count = 0
            provider.status = ProviderStatus.ACTIVE
            
            return {"success": True, "response": response}
            
        except Exception as e:
            # Handle errors
            self.error_counts[provider_name] += 1
            provider.error_count += 1
            
            # Mark provider as error if too many failures
            if provider.error_count >= 3:
                provider.status = ProviderStatus.ERROR
            
            return {"success": False, "error": str(e)}
    
    async def _query_openai(self, provider: ProviderConfig, prompt: str, context: Optional[Dict] = None) -> str:
        """Query OpenAI API"""
        headers = {
            "Authorization": f"Bearer {provider.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": provider.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": provider.max_tokens,
            "temperature": provider.temperature
        }
        
        async with self.session.post(provider.base_url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
            elif response.status == 429:
                provider.rate_limit_reset = datetime.now() + timedelta(minutes=1)
                provider.status = ProviderStatus.RATE_LIMITED
                raise Exception("Rate limited")
            else:
                raise Exception(f"API error: {response.status}")
    
    async def _query_deepseek(self, provider: ProviderConfig, prompt: str, context: Optional[Dict] = None) -> str:
        """Query DeepSeek API"""
        # Similar implementation to OpenAI
        return await self._query_openai(provider, prompt, context)
    
    async def _query_anthropic(self, provider: ProviderConfig, prompt: str, context: Optional[Dict] = None) -> str:
        """Query Anthropic API"""
        headers = {
            "x-api-key": provider.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": provider.model,
            "max_tokens": provider.max_tokens,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        async with self.session.post(provider.base_url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result["content"][0]["text"]
            else:
                raise Exception(f"Anthropic API error: {response.status}")
    
    async def _query_google(self, provider: ProviderConfig, prompt: str, context: Optional[Dict] = None) -> str:
        """Query Google Gemini API"""
        headers = {
            "Content-Type": "application/json"
        }
        
        url = f"{provider.base_url}?key={provider.api_key}"
        
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": provider.temperature,
                "maxOutputTokens": provider.max_tokens
            }
        }
        
        async with self.session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result["candidates"][0]["content"]["parts"][0]["text"]
            else:
                raise Exception(f"Google API error: {response.status}")
    
    async def _query_openrouter(self, provider: ProviderConfig, prompt: str, context: Optional[Dict] = None) -> str:
        """Query OpenRouter API"""
        headers = {
            "Authorization": f"Bearer {provider.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://aion-ai.com",
            "X-Title": "AION AI Terminal"
        }
        
        data = {
            "model": provider.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": provider.max_tokens,
            "temperature": provider.temperature
        }
        
        async with self.session.post(provider.base_url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception(f"OpenRouter API error: {response.status}")
    
    async def _check_provider_health(self, provider_name: str) -> bool:
        """Check if provider is healthy and available"""
        try:
            # Simple health check with minimal query
            result = await self._try_provider(provider_name, "Hello", None)
            return result["success"]
        except:
            return False
    
    def _select_best_provider(self) -> str:
        """Select the best available provider based on performance"""
        available_providers = [
            name for name, provider in self.providers.items()
            if provider.api_key and provider.status != ProviderStatus.ERROR
        ]
        
        if not available_providers:
            return "openai"  # Default fallback
        
        # Select provider with lowest error rate
        best_provider = min(
            available_providers,
            key=lambda name: self.error_counts.get(name, 0)
        )
        
        return best_provider
    
    def switch_provider(self, provider_name: str) -> bool:
        """Manually switch to a specific provider"""
        if provider_name in self.providers and self.providers[provider_name].api_key:
            self.current_provider = provider_name
            return True
        return False
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return [
            name for name, provider in self.providers.items()
            if provider.api_key and provider.status != ProviderStatus.ERROR
        ]
    
    def get_provider_stats(self) -> Dict:
        """Get performance statistics for all providers"""
        stats = {}
        
        for name, provider in self.providers.items():
            avg_response_time = (
                sum(self.response_times[name]) / len(self.response_times[name])
                if self.response_times[name] else 0
            )
            
            stats[name] = {
                "status": provider.status.value,
                "requests": self.request_counts[name],
                "errors": self.error_counts[name],
                "avg_response_time": avg_response_time,
                "last_used": provider.last_used.isoformat() if provider.last_used else None,
                "model": provider.model
            }
        
        return stats

    def get_current_provider(self) -> str:
        """Get the name of the current active provider"""
        return self.current_provider

    def is_provider_ready(self, provider_name: str) -> bool:
        """Check if a provider is ready for use"""
        if provider_name not in self.providers:
            return False

        provider = self.providers[provider_name]
        return (provider.api_key is not None and
                provider.api_key.strip() != "" and
                provider.status != ProviderStatus.ERROR)

    def shutdown(self):
        """Gracefully shutdown the provider router"""
        if self.session:
            asyncio.create_task(self.session.close())
        
        if self.health_check_task:
            self.health_check_task.cancel()

# Global provider router instance
from .config_loader import config_loader
provider_router = ProviderRouter(config_loader)
