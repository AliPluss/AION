"""
🧠 AION Advanced AI Providers System
Professional AI integration with multiple providers, caching, monitoring, and security
Features: OpenAI, DeepSeek, OpenRouter, Gemini with advanced management
"""

import os
import json
import time
import hashlib
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from contextlib import asynccontextmanager

# Optional imports with fallbacks
try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    httpx = None

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    Fernet = None

class AIProvider(Enum):
    """Supported AI providers"""
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    OPENROUTER = "openrouter"
    GEMINI = "gemini"

class MessageRole(Enum):
    """Message roles for conversations"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class CacheStrategy(Enum):
    """Caching strategies"""
    NONE = "none"
    MEMORY = "memory"
    DISK = "disk"
    HYBRID = "hybrid"

@dataclass
class ConversationMessage:
    """Single message in a conversation"""
    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class UsageStats:
    """Usage statistics for AI providers"""
    total_requests: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    last_request_time: Optional[datetime] = None

@dataclass
class AIResponse:
    """Enhanced AI response data structure"""
    content: str
    provider: str
    model: str
    tokens_used: Optional[int] = None
    cost: Optional[float] = None
    error: Optional[str] = None
    response_time: Optional[float] = None
    cached: bool = False
    conversation_id: Optional[str] = None
    message_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "content": self.content,
            "provider": self.provider,
            "model": self.model,
            "tokens_used": self.tokens_used,
            "cost": self.cost,
            "error": self.error,
            "response_time": self.response_time,
            "cached": self.cached,
            "conversation_id": self.conversation_id,
            "message_id": self.message_id,
            "metadata": self.metadata
        }

@dataclass
class ProviderConfig:
    """Configuration for AI providers"""
    api_key: str
    model: str
    enabled: bool = True
    max_tokens: int = 1000
    temperature: float = 0.7
    timeout: float = 30.0
    rate_limit: int = 60  # requests per minute
    cost_per_token: float = 0.0
    custom_headers: Dict[str, str] = field(default_factory=dict)

class ResponseCache:
    """Advanced response caching system"""

    def __init__(self, strategy: CacheStrategy = CacheStrategy.MEMORY, max_size: int = 1000):
        self.strategy = strategy
        self.max_size = max_size
        self.memory_cache: Dict[str, Dict[str, Any]] = {}
        self.cache_dir = Path.home() / ".aion" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _generate_cache_key(self, prompt: str, provider: str, model: str, **kwargs) -> str:
        """Generate cache key for request"""
        cache_data = f"{provider}:{model}:{prompt}:{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.md5(cache_data.encode()).hexdigest()

    def get(self, prompt: str, provider: str, model: str, **kwargs) -> Optional[AIResponse]:
        """Get cached response"""
        cache_key = self._generate_cache_key(prompt, provider, model, **kwargs)

        if self.strategy in [CacheStrategy.MEMORY, CacheStrategy.HYBRID]:
            if cache_key in self.memory_cache:
                cached_data = self.memory_cache[cache_key]
                # Check if cache is still valid (24 hours)
                if datetime.now() - cached_data["timestamp"] < timedelta(hours=24):
                    response_data = cached_data["response"]
                    response_data["cached"] = True
                    return AIResponse(**response_data)

        if self.strategy in [CacheStrategy.DISK, CacheStrategy.HYBRID]:
            cache_file = self.cache_dir / f"{cache_key}.json"
            if cache_file.exists():
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cached_data = json.load(f)

                    # Check if cache is still valid
                    timestamp = datetime.fromisoformat(cached_data["timestamp"])
                    if datetime.now() - timestamp < timedelta(hours=24):
                        response_data = cached_data["response"]
                        response_data["cached"] = True
                        return AIResponse(**response_data)
                except Exception:
                    pass  # Ignore cache errors

        return None

    def set(self, prompt: str, provider: str, model: str, response: AIResponse, **kwargs):
        """Cache response"""
        cache_key = self._generate_cache_key(prompt, provider, model, **kwargs)
        cache_data = {
            "timestamp": datetime.now(),
            "response": response.to_dict()
        }

        if self.strategy in [CacheStrategy.MEMORY, CacheStrategy.HYBRID]:
            # Implement LRU eviction
            if len(self.memory_cache) >= self.max_size:
                oldest_key = min(self.memory_cache.keys(),
                               key=lambda k: self.memory_cache[k]["timestamp"])
                del self.memory_cache[oldest_key]

            self.memory_cache[cache_key] = cache_data

        if self.strategy in [CacheStrategy.DISK, CacheStrategy.HYBRID]:
            cache_file = self.cache_dir / f"{cache_key}.json"
            try:
                cache_data_serializable = {
                    "timestamp": cache_data["timestamp"].isoformat(),
                    "response": cache_data["response"]
                }
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(cache_data_serializable, f, indent=2)
            except Exception:
                pass  # Ignore cache errors

class BaseAIProvider(ABC):
    """Enhanced base class for AI providers with professional features"""

    def __init__(self, config: ProviderConfig):
        self.config = config
        self.api_key = config.api_key
        self.model = config.model
        self.client = None
        self.usage_stats = UsageStats()
        self.conversations: Dict[str, List[ConversationMessage]] = {}
        self.rate_limiter = RateLimiter(config.rate_limit)

        # Encrypt API key if crypto is available
        if CRYPTO_AVAILABLE and config.api_key:
            self._setup_encryption()

    def _setup_encryption(self):
        """Setup API key encryption"""
        try:
            key_file = Path.home() / ".aion" / "encryption.key"
            if not key_file.exists():
                key = Fernet.generate_key()
                key_file.parent.mkdir(parents=True, exist_ok=True)
                with open(key_file, 'wb') as f:
                    f.write(key)
            else:
                with open(key_file, 'rb') as f:
                    key = f.read()

            self.cipher = Fernet(key)
            # Encrypt the API key
            self.encrypted_api_key = self.cipher.encrypt(self.api_key.encode())
        except Exception:
            self.cipher = None
            self.encrypted_api_key = None

    def _get_decrypted_api_key(self) -> str:
        """Get decrypted API key"""
        if self.cipher and self.encrypted_api_key:
            try:
                return self.cipher.decrypt(self.encrypted_api_key).decode()
            except Exception:
                pass
        return self.api_key

    async def _rate_limit_check(self):
        """Check rate limiting"""
        await self.rate_limiter.acquire()

    def _update_usage_stats(self, response: AIResponse, response_time: float):
        """Update usage statistics"""
        self.usage_stats.total_requests += 1
        self.usage_stats.last_request_time = datetime.now()

        if response.error:
            self.usage_stats.failed_requests += 1
        else:
            self.usage_stats.successful_requests += 1
            if response.tokens_used:
                self.usage_stats.total_tokens += response.tokens_used
            if response.cost:
                self.usage_stats.total_cost += response.cost

        # Update average response time
        total_successful = self.usage_stats.successful_requests
        if total_successful > 0:
            current_avg = self.usage_stats.average_response_time
            self.usage_stats.average_response_time = (
                (current_avg * (total_successful - 1) + response_time) / total_successful
            )

    def add_conversation_message(self, conversation_id: str, role: MessageRole, content: str):
        """Add message to conversation history"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []

        message = ConversationMessage(role=role, content=content)
        self.conversations[conversation_id].append(message)

        # Keep only last 50 messages per conversation
        if len(self.conversations[conversation_id]) > 50:
            self.conversations[conversation_id] = self.conversations[conversation_id][-50:]

    def get_conversation_history(self, conversation_id: str) -> List[ConversationMessage]:
        """Get conversation history"""
        return self.conversations.get(conversation_id, [])

    def clear_conversation(self, conversation_id: str):
        """Clear conversation history"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]

    @abstractmethod
    async def generate_response(self, prompt: str, conversation_id: Optional[str] = None, **kwargs) -> AIResponse:
        """Generate AI response with conversation support"""
        pass

    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        pass

    def get_usage_stats(self) -> UsageStats:
        """Get usage statistics"""
        return self.usage_stats

    def reset_usage_stats(self):
        """Reset usage statistics"""
        self.usage_stats = UsageStats()

class RateLimiter:
    """Rate limiting for API requests"""

    def __init__(self, requests_per_minute: int):
        self.requests_per_minute = requests_per_minute
        self.requests = []
        self.lock = asyncio.Lock()

    async def acquire(self):
        """Acquire rate limit permission"""
        async with self.lock:
            now = time.time()
            # Remove requests older than 1 minute
            self.requests = [req_time for req_time in self.requests if now - req_time < 60]

            if len(self.requests) >= self.requests_per_minute:
                # Wait until we can make another request
                sleep_time = 60 - (now - self.requests[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                    # Clean up again after sleeping
                    now = time.time()
                    self.requests = [req_time for req_time in self.requests if now - req_time < 60]

            self.requests.append(now)

class OpenAIProvider(BaseAIProvider):
    """Enhanced OpenAI provider with professional features"""

    def __init__(self, config: ProviderConfig):
        if not config.model:
            config.model = "gpt-3.5-turbo"
        super().__init__(config)
        self.base_url = "https://api.openai.com/v1"
        self.models = [
            "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo",
            "gpt-4o", "gpt-4o-mini", "gpt-4-turbo-preview"
        ]

        # Model-specific pricing (per 1K tokens)
        self.pricing = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.0015, "output": 0.002},
            "gpt-4o": {"input": 0.005, "output": 0.015},
            "gpt-4o-mini": {"input": 0.00015, "output": 0.0006}
        }
    
    async def generate_response(self, prompt: str, conversation_id: Optional[str] = None, **kwargs) -> AIResponse:
        """Generate response using OpenAI API with advanced features"""
        if not HTTPX_AVAILABLE:
            return AIResponse(
                content="",
                provider="OpenAI",
                model=self.model,
                error="httpx library not available"
            )

        start_time = time.time()

        try:
            # Rate limiting
            await self._rate_limit_check()

            # Build messages for conversation context
            messages = []

            # Add conversation history if available
            if conversation_id:
                history = self.get_conversation_history(conversation_id)
                for msg in history[-10:]:  # Last 10 messages for context
                    messages.append({
                        "role": msg.role.value,
                        "content": msg.content
                    })

            # Add current prompt
            messages.append({"role": "user", "content": prompt})

            # Get decrypted API key
            api_key = self._get_decrypted_api_key()

            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }

                # Add custom headers
                headers.update(self.config.custom_headers)

                data = {
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
                    "temperature": kwargs.get("temperature", self.config.temperature),
                    "stream": kwargs.get("stream", False)
                }

                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=self.config.timeout
                )

                response_time = time.time() - start_time

                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    usage = result.get("usage", {})

                    # Calculate cost
                    cost = self._calculate_cost(usage)

                    ai_response = AIResponse(
                        content=content,
                        provider="OpenAI",
                        model=self.model,
                        tokens_used=usage.get("total_tokens", 0),
                        cost=cost,
                        response_time=response_time,
                        conversation_id=conversation_id,
                        message_id=f"openai_{int(time.time() * 1000)}",
                        metadata={
                            "prompt_tokens": usage.get("prompt_tokens", 0),
                            "completion_tokens": usage.get("completion_tokens", 0),
                            "finish_reason": result["choices"][0].get("finish_reason")
                        }
                    )

                    # Add to conversation history
                    if conversation_id:
                        self.add_conversation_message(conversation_id, MessageRole.USER, prompt)
                        self.add_conversation_message(conversation_id, MessageRole.ASSISTANT, content)

                    # Update usage stats
                    self._update_usage_stats(ai_response, response_time)

                    return ai_response

                else:
                    error_msg = f"OpenAI API error: {response.status_code}"
                    if response.status_code == 429:
                        error_msg += " - Rate limit exceeded"
                    elif response.status_code == 401:
                        error_msg += " - Invalid API key"
                    elif response.status_code == 400:
                        error_msg += " - Bad request"

                    ai_response = AIResponse(
                        content="",
                        provider="OpenAI",
                        model=self.model,
                        error=error_msg,
                        response_time=response_time,
                        conversation_id=conversation_id
                    )

                    self._update_usage_stats(ai_response, response_time)
                    return ai_response

        except Exception as e:
            response_time = time.time() - start_time
            ai_response = AIResponse(
                content="",
                provider="OpenAI",
                model=self.model,
                error=f"Request failed: {str(e)}",
                response_time=response_time,
                conversation_id=conversation_id
            )

            self._update_usage_stats(ai_response, response_time)
            return ai_response

    def _calculate_cost(self, usage: Dict[str, int]) -> float:
        """Calculate cost based on token usage"""
        if self.model not in self.pricing:
            return 0.0

        pricing = self.pricing[self.model]
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)

        cost = (prompt_tokens / 1000 * pricing["input"] +
                completion_tokens / 1000 * pricing["output"])

        return round(cost, 6)
    
    def get_available_models(self) -> List[str]:
        """Get available OpenAI models"""
        return self.models.copy()

    async def validate_api_key(self) -> bool:
        """Validate API key by making a test request"""
        if not HTTPX_AVAILABLE:
            return False

        try:
            api_key = self._get_decrypted_api_key()
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }

                response = await client.get(
                    f"{self.base_url}/models",
                    headers=headers,
                    timeout=10.0
                )

                return response.status_code == 200
        except Exception:
            return False

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

class AdvancedAIManager:
    """
    🚀 Advanced AI Provider Manager

    Professional AI management system with:
    - Multi-provider support with automatic failover
    - Response caching and optimization
    - Usage monitoring and cost tracking
    - Conversation management
    - Security and encryption
    - Rate limiting and error handling
    """

    def __init__(self, cache_strategy: CacheStrategy = CacheStrategy.HYBRID):
        self.providers: Dict[str, BaseAIProvider] = {}
        self.current_provider: Optional[str] = None
        self.cache = ResponseCache(cache_strategy)
        self.config_file = Path.home() / ".aion" / "ai_config.json"
        self.usage_log_file = Path.home() / ".aion" / "usage_log.json"
        self.conversations: Dict[str, List[ConversationMessage]] = {}
        self.provider_health: Dict[str, bool] = {}

        # Ensure directories exist
        self.config_file.parent.mkdir(parents=True, exist_ok=True)

        self.load_config()
    
    def load_config(self):
        """Load AI provider configuration with enhanced error handling"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.setup_providers(config)
            except Exception as e:
                print(f"Error loading AI config: {e}")
                self._create_default_config()
        else:
            self._create_default_config()

    def _create_default_config(self):
        """Create default configuration file"""
        default_config = {
            "openai": {
                "enabled": False,
                "api_key": "",
                "model": "gpt-3.5-turbo",
                "max_tokens": 1000,
                "temperature": 0.7,
                "timeout": 30.0,
                "rate_limit": 60,
                "custom_headers": {}
            },
            "deepseek": {
                "enabled": False,
                "api_key": "",
                "model": "deepseek-coder",
                "max_tokens": 1000,
                "temperature": 0.7,
                "timeout": 30.0,
                "rate_limit": 60,
                "custom_headers": {}
            },
            "openrouter": {
                "enabled": False,
                "api_key": "",
                "model": "mistralai/mistral-7b-instruct",
                "max_tokens": 1000,
                "temperature": 0.7,
                "timeout": 30.0,
                "rate_limit": 60,
                "custom_headers": {}
            },
            "gemini": {
                "enabled": False,
                "api_key": "",
                "model": "gemini-pro",
                "max_tokens": 1000,
                "temperature": 0.7,
                "timeout": 30.0,
                "rate_limit": 60,
                "custom_headers": {}
            }
        }

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2)
        except Exception as e:
            print(f"Error creating default config: {e}")

    def setup_providers(self, config: Dict[str, Any]):
        """Setup AI providers from configuration with enhanced features"""
        for provider_name, provider_config in config.items():
            if not provider_config.get("enabled", False):
                continue

            api_key = provider_config.get("api_key")
            if not api_key:
                continue

            try:
                # Create ProviderConfig object
                config_obj = ProviderConfig(
                    api_key=api_key,
                    model=provider_config.get("model", ""),
                    enabled=provider_config.get("enabled", True),
                    max_tokens=provider_config.get("max_tokens", 1000),
                    temperature=provider_config.get("temperature", 0.7),
                    timeout=provider_config.get("timeout", 30.0),
                    rate_limit=provider_config.get("rate_limit", 60),
                    cost_per_token=provider_config.get("cost_per_token", 0.0),
                    custom_headers=provider_config.get("custom_headers", {})
                )

                # Create provider instance
                if provider_name == "openai":
                    self.providers["openai"] = OpenAIProvider(config_obj)
                elif provider_name == "deepseek":
                    # Note: DeepSeekProvider needs to be updated to use ProviderConfig
                    # For now, create a basic instance
                    self.providers["deepseek"] = DeepSeekProvider(api_key, config_obj.model)
                elif provider_name == "openrouter":
                    # Note: OpenRouterProvider needs to be updated to use ProviderConfig
                    self.providers["openrouter"] = OpenRouterProvider(api_key, config_obj.model)
                elif provider_name == "gemini":
                    # Note: GeminiProvider needs to be updated to use ProviderConfig
                    self.providers["gemini"] = GeminiProvider(api_key, config_obj.model)

                # Set as current provider if none set
                if not self.current_provider:
                    self.current_provider = provider_name

                # Initialize provider health as unknown
                self.provider_health[provider_name] = True

            except Exception as e:
                print(f"Error setting up {provider_name}: {e}")
                self.provider_health[provider_name] = False
    
    async def generate_response(self, prompt: str, conversation_id: Optional[str] = None, **kwargs) -> AIResponse:
        """Generate response with caching, failover, and advanced features"""
        # Check cache first
        cached_response = self.cache.get(prompt, self.current_provider or "none",
                                       self.get_current_model(), **kwargs)
        if cached_response:
            return cached_response

        # Try current provider first
        if self.current_provider and self.current_provider in self.providers:
            try:
                provider = self.providers[self.current_provider]
                response = await provider.generate_response(prompt, conversation_id, **kwargs)

                if not response.error:
                    # Cache successful response
                    self.cache.set(prompt, self.current_provider, provider.model, response, **kwargs)
                    self._log_usage(response)
                    return response
                else:
                    # Mark provider as unhealthy
                    self.provider_health[self.current_provider] = False

            except Exception as e:
                self.provider_health[self.current_provider] = False
                print(f"Provider {self.current_provider} failed: {e}")

        # Try failover to other healthy providers
        for provider_name, provider in self.providers.items():
            if (provider_name != self.current_provider and
                self.provider_health.get(provider_name, True)):
                try:
                    response = await provider.generate_response(prompt, conversation_id, **kwargs)
                    if not response.error:
                        # Cache successful response
                        self.cache.set(prompt, provider_name, provider.model, response, **kwargs)
                        self._log_usage(response)
                        # Switch to working provider
                        self.current_provider = provider_name
                        self.provider_health[provider_name] = True
                        return response
                except Exception as e:
                    self.provider_health[provider_name] = False
                    print(f"Failover provider {provider_name} failed: {e}")

        # All providers failed
        return AIResponse(
            content="",
            provider="None",
            model="None",
            error="All AI providers are currently unavailable"
        )

    def _log_usage(self, response: AIResponse):
        """Log usage statistics"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "provider": response.provider,
                "model": response.model,
                "tokens_used": response.tokens_used,
                "cost": response.cost,
                "response_time": response.response_time,
                "conversation_id": response.conversation_id
            }

            # Append to usage log
            if self.usage_log_file.exists():
                with open(self.usage_log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []

            logs.append(log_entry)

            # Keep only last 1000 entries
            if len(logs) > 1000:
                logs = logs[-1000:]

            with open(self.usage_log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2)

        except Exception as e:
            print(f"Error logging usage: {e}")

    def add_provider(self, name: str, provider: BaseAIProvider):
        """Add a new AI provider"""
        self.providers[name] = provider
        self.provider_health[name] = True
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

    def get_current_provider(self) -> Optional[str]:
        """Get the current active provider"""
        return self.current_provider

    def set_provider(self, provider_name: str) -> bool:
        """Set the active provider (alias for set_current_provider)"""
        return self.set_current_provider(provider_name)

    def get_provider_info(self, provider_name: str) -> Dict[str, Any]:
        """Get detailed information about a provider"""
        if provider_name not in self.providers:
            return {"error": f"Provider {provider_name} not found"}

        provider = self.providers[provider_name]
        return {
            "name": provider_name,
            "model": provider.model,
            "available_models": provider.get_available_models(),
            "active": provider_name == self.current_provider
        }

    def get_all_providers_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all providers"""
        return {
            name: self.get_provider_info(name)
            for name in self.providers.keys()
        }

    def is_provider_available(self, provider_name: str) -> bool:
        """Check if a provider is available"""
        return provider_name in self.providers

    def remove_provider(self, provider_name: str) -> bool:
        """Remove a provider"""
        if provider_name in self.providers:
            del self.providers[provider_name]
            if provider_name in self.provider_health:
                del self.provider_health[provider_name]
            if self.current_provider == provider_name:
                # Set to first available provider or None
                self.current_provider = next(iter(self.providers.keys()), None)
            return True
        return False

    def get_current_model(self) -> str:
        """Get current model name"""
        if self.current_provider and self.current_provider in self.providers:
            return self.providers[self.current_provider].model
        return "None"

    async def health_check(self) -> Dict[str, bool]:
        """Check health of all providers"""
        health_results = {}

        for provider_name, provider in self.providers.items():
            try:
                if hasattr(provider, 'validate_api_key'):
                    is_healthy = await provider.validate_api_key()
                else:
                    # Basic health check - try a simple request
                    test_response = await provider.generate_response("test", max_tokens=1)
                    is_healthy = not test_response.error

                health_results[provider_name] = is_healthy
                self.provider_health[provider_name] = is_healthy

            except Exception:
                health_results[provider_name] = False
                self.provider_health[provider_name] = False

        return health_results

    def get_usage_summary(self) -> Dict[str, Any]:
        """Get comprehensive usage summary"""
        summary = {
            "total_providers": len(self.providers),
            "active_provider": self.current_provider,
            "provider_health": self.provider_health.copy(),
            "provider_stats": {}
        }

        for provider_name, provider in self.providers.items():
            stats = provider.get_usage_stats()
            summary["provider_stats"][provider_name] = {
                "total_requests": stats.total_requests,
                "successful_requests": stats.successful_requests,
                "failed_requests": stats.failed_requests,
                "total_tokens": stats.total_tokens,
                "total_cost": stats.total_cost,
                "average_response_time": stats.average_response_time,
                "last_request_time": stats.last_request_time.isoformat() if stats.last_request_time else None
            }

        return summary

    def reset_all_usage_stats(self):
        """Reset usage statistics for all providers"""
        for provider in self.providers.values():
            provider.reset_usage_stats()

    def save_config(self):
        """Save current configuration to file"""
        config = {}

        for provider_name, provider in self.providers.items():
            config[provider_name] = {
                "enabled": True,
                "api_key": provider.api_key,  # Note: This saves unencrypted key
                "model": provider.model,
                "max_tokens": provider.config.max_tokens if hasattr(provider, 'config') else 1000,
                "temperature": provider.config.temperature if hasattr(provider, 'config') else 0.7,
                "timeout": provider.config.timeout if hasattr(provider, 'config') else 30.0,
                "rate_limit": provider.config.rate_limit if hasattr(provider, 'config') else 60,
                "custom_headers": provider.config.custom_headers if hasattr(provider, 'config') else {}
            }

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

# Backward compatibility
AIManager = AdvancedAIManager
