"""
🧠 AION AI Providers
Support for multiple AI providers: OpenAI, DeepSeek, OpenRouter, Gemini
"""

import os
import json
import httpx
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

class AIProvider(Enum):
    """Supported AI providers"""
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    OPENROUTER = "openrouter"
    GEMINI = "gemini"

@dataclass
class AIResponse:
    """AI response data structure"""
    content: str
    provider: str
    model: str
    tokens_used: Optional[int] = None
    cost: Optional[float] = None
    error: Optional[str] = None

class BaseAIProvider(ABC):
    """Base class for AI providers"""
    
    def __init__(self, api_key: str, model: str = None):
        self.api_key = api_key
        self.model = model
        self.client = None
    
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> AIResponse:
        """Generate AI response"""
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        pass

class OpenAIProvider(BaseAIProvider):
    """OpenAI provider implementation"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key, model)
        self.base_url = "https://api.openai.com/v1"
        self.models = [
            "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo",
            "gpt-4o", "gpt-4o-mini"
        ]
    
    async def generate_response(self, prompt: str, **kwargs) -> AIResponse:
        """Generate response using OpenAI API"""
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": kwargs.get("max_tokens", 1000),
                    "temperature": kwargs.get("temperature", 0.7)
                }
                
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    tokens = result.get("usage", {}).get("total_tokens", 0)
                    
                    return AIResponse(
                        content=content,
                        provider="OpenAI",
                        model=self.model,
                        tokens_used=tokens
                    )
                else:
                    error_msg = f"OpenAI API error: {response.status_code}"
                    return AIResponse(
                        content="",
                        provider="OpenAI",
                        model=self.model,
                        error=error_msg
                    )
                    
        except Exception as e:
            return AIResponse(
                content="",
                provider="OpenAI",
                model=self.model,
                error=str(e)
            )
    
    def get_available_models(self) -> List[str]:
        return self.models.copy()

class DeepSeekProvider(BaseAIProvider):
    """DeepSeek provider implementation"""
    
    def __init__(self, api_key: str, model: str = "deepseek-coder"):
        super().__init__(api_key, model)
        self.base_url = "https://api.deepseek.com/v1"
        self.models = [
            "deepseek-coder", "deepseek-chat"
        ]
    
    async def generate_response(self, prompt: str, **kwargs) -> AIResponse:
        """Generate response using DeepSeek API"""
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": kwargs.get("max_tokens", 1000),
                    "temperature": kwargs.get("temperature", 0.7)
                }
                
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    tokens = result.get("usage", {}).get("total_tokens", 0)
                    
                    return AIResponse(
                        content=content,
                        provider="DeepSeek",
                        model=self.model,
                        tokens_used=tokens
                    )
                else:
                    error_msg = f"DeepSeek API error: {response.status_code}"
                    return AIResponse(
                        content="",
                        provider="DeepSeek",
                        model=self.model,
                        error=error_msg
                    )
                    
        except Exception as e:
            return AIResponse(
                content="",
                provider="DeepSeek",
                model=self.model,
                error=str(e)
            )
    
    def get_available_models(self) -> List[str]:
        return self.models.copy()

class OpenRouterProvider(BaseAIProvider):
    """OpenRouter provider implementation"""
    
    def __init__(self, api_key: str, model: str = "mistralai/mistral-7b-instruct"):
        super().__init__(api_key, model)
        self.base_url = "https://openrouter.ai/api/v1"
        self.models = [
            "mistralai/mistral-7b-instruct",
            "meta-llama/llama-2-70b-chat",
            "anthropic/claude-2",
            "openai/gpt-3.5-turbo"
        ]
    
    async def generate_response(self, prompt: str, **kwargs) -> AIResponse:
        """Generate response using OpenRouter API"""
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://aion-terminal.com",
                    "X-Title": "AION Terminal Assistant"
                }
                
                data = {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": kwargs.get("max_tokens", 1000),
                    "temperature": kwargs.get("temperature", 0.7)
                }
                
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    tokens = result.get("usage", {}).get("total_tokens", 0)
                    
                    return AIResponse(
                        content=content,
                        provider="OpenRouter",
                        model=self.model,
                        tokens_used=tokens
                    )
                else:
                    error_msg = f"OpenRouter API error: {response.status_code}"
                    return AIResponse(
                        content="",
                        provider="OpenRouter",
                        model=self.model,
                        error=error_msg
                    )
                    
        except Exception as e:
            return AIResponse(
                content="",
                provider="OpenRouter",
                model=self.model,
                error=str(e)
            )
    
    def get_available_models(self) -> List[str]:
        return self.models.copy()

class GeminiProvider(BaseAIProvider):
    """Google Gemini provider implementation"""
    
    def __init__(self, api_key: str, model: str = "gemini-pro"):
        super().__init__(api_key, model)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.models = [
            "gemini-pro", "gemini-pro-vision"
        ]
    
    async def generate_response(self, prompt: str, **kwargs) -> AIResponse:
        """Generate response using Gemini API"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/models/{self.model}:generateContent"
                params = {"key": self.api_key}
                
                data = {
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }],
                    "generationConfig": {
                        "maxOutputTokens": kwargs.get("max_tokens", 1000),
                        "temperature": kwargs.get("temperature", 0.7)
                    }
                }
                
                response = await client.post(
                    url,
                    params=params,
                    json=data,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["candidates"][0]["content"]["parts"][0]["text"]
                    
                    return AIResponse(
                        content=content,
                        provider="Gemini",
                        model=self.model
                    )
                else:
                    error_msg = f"Gemini API error: {response.status_code}"
                    return AIResponse(
                        content="",
                        provider="Gemini",
                        model=self.model,
                        error=error_msg
                    )
                    
        except Exception as e:
            return AIResponse(
                content="",
                provider="Gemini",
                model=self.model,
                error=str(e)
            )
    
    def get_available_models(self) -> List[str]:
        return self.models.copy()

class AIManager:
    """AI provider manager"""
    
    def __init__(self):
        self.providers: Dict[str, BaseAIProvider] = {}
        self.current_provider: Optional[str] = None
        self.load_config()
    
    def load_config(self):
        """Load AI provider configuration"""
        config_file = os.path.expanduser("~/.aion/ai_config.json")
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.setup_providers(config)
            except Exception as e:
                print(f"Error loading AI config: {e}")
    
    def setup_providers(self, config: Dict[str, Any]):
        """Setup AI providers from configuration"""
        for provider_name, provider_config in config.items():
            if not provider_config.get("enabled", False):
                continue
                
            api_key = provider_config.get("api_key")
            model = provider_config.get("model")
            
            if not api_key:
                continue
            
            try:
                if provider_name == "openai":
                    self.providers["openai"] = OpenAIProvider(api_key, model)
                elif provider_name == "deepseek":
                    self.providers["deepseek"] = DeepSeekProvider(api_key, model)
                elif provider_name == "openrouter":
                    self.providers["openrouter"] = OpenRouterProvider(api_key, model)
                elif provider_name == "gemini":
                    self.providers["gemini"] = GeminiProvider(api_key, model)
                
                if not self.current_provider:
                    self.current_provider = provider_name
                    
            except Exception as e:
                print(f"Error setting up {provider_name}: {e}")
    
    def add_provider(self, name: str, provider: BaseAIProvider):
        """Add a new AI provider"""
        self.providers[name] = provider
        if not self.current_provider:
            self.current_provider = name
    
    def set_current_provider(self, name: str) -> bool:
        """Set the current active provider"""
        if name in self.providers:
            self.current_provider = name
            return True
        return False
    
    async def generate_response(self, prompt: str, **kwargs) -> AIResponse:
        """Generate response using current provider"""
        if not self.current_provider or self.current_provider not in self.providers:
            return AIResponse(
                content="",
                provider="None",
                model="None",
                error="No AI provider configured"
            )
        
        provider = self.providers[self.current_provider]
        return await provider.generate_response(prompt, **kwargs)
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return list(self.providers.keys())
    
    def get_provider_models(self, provider_name: str) -> List[str]:
        """Get available models for a provider"""
        if provider_name in self.providers:
            return self.providers[provider_name].get_available_models()
        return []
