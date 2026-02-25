"""
🧠 AI Interface - Central Access Point for All AI Logic
======================================================

This is the main interface that coordinates all AI functionality across AION.
It provides a unified API for chat, search, explanation, voice, and context-aware assistance.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pathlib import Path

from .provider_router import ProviderRouter
from .context_manager import ContextManager
from .chat_engine import ChatEngine
from .command_explainer import CommandExplainer
from .ai_logger import AILogger
from .config_loader import ConfigLoader

class AIInterface:
    """Central AI interface for all AION AI functionality"""
    
    def __init__(self):
        """Initialize the AI interface with all components"""
        self.config = ConfigLoader()
        self.logger = AILogger()
        self.provider_router = ProviderRouter(self.config)
        self.context_manager = ContextManager()
        self.chat_engine = ChatEngine(self.provider_router, self.logger)
        self.command_explainer = CommandExplainer(self.provider_router, self.logger)
        
        # Performance tracking
        self.request_count = 0
        self.cache_hits = 0
        self.total_response_time = 0.0
        
        # Safety settings
        self.safety_enabled = True
        self.dangerous_commands = {
            'rm -rf', 'del /f', 'format', 'fdisk', 'dd if=', 
            'sudo rm', 'chmod 777', 'killall', 'shutdown'
        }
        
        self.logger.log_info("AI Interface initialized successfully")
    
    async def chat(self, message: str, context: Optional[Dict] = None) -> str:
        """Handle chat messages with full context awareness"""
        try:
            self.request_count += 1
            start_time = datetime.now()
            
            # Update context
            if context:
                self.context_manager.update_context(context)
            
            # Get current context
            current_context = self.context_manager.get_current_context()
            
            # Process chat message
            response = await self.chat_engine.process_message(message, current_context)
            
            # Log performance
            response_time = (datetime.now() - start_time).total_seconds()
            self.total_response_time += response_time
            
            self.logger.log_chat(message, response, response_time)
            
            return response
            
        except Exception as e:
            error_msg = f"Chat error: {e}"
            self.logger.log_error(error_msg)
            return f"⚠️ Sorry, I encountered an error: {e}"
    
    async def explain_command(self, command: str, context: Optional[Dict] = None) -> str:
        """Explain a command with safety assessment"""
        try:
            self.request_count += 1
            start_time = datetime.now()
            
            # Safety check
            if self.safety_enabled and self._is_dangerous_command(command):
                safety_warning = "⚠️ **DANGER**: This command could be harmful to your system!"
            else:
                safety_warning = None
            
            # Get explanation
            explanation = await self.command_explainer.explain(command, context)
            
            # Add safety warning if needed
            if safety_warning:
                explanation = f"{safety_warning}\n\n{explanation}"
            
            # Log performance
            response_time = (datetime.now() - start_time).total_seconds()
            self.total_response_time += response_time
            
            self.logger.log_explanation(command, explanation, response_time)
            
            return explanation
            
        except Exception as e:
            error_msg = f"Command explanation error: {e}"
            self.logger.log_error(error_msg)
            return f"⚠️ Unable to explain command: {e}"
    
    async def search(self, query: str, sources: Optional[List[str]] = None, max_results: int = 10) -> Dict:
        """Perform intelligent search across multiple sources"""
        try:
            self.request_count += 1
            start_time = datetime.now()
            
            # Import smart search
            from aion.ai.smart_search import smart_search
            
            # Perform search
            search_results = await smart_search.search(query, sources, max_results)
            
            # Enhance results with AI context
            enhanced_results = await self._enhance_search_results(search_results)
            
            # Log performance
            response_time = (datetime.now() - start_time).total_seconds()
            self.total_response_time += response_time
            
            self.logger.log_search(query, enhanced_results, response_time)
            
            return enhanced_results
            
        except Exception as e:
            error_msg = f"Search error: {e}"
            self.logger.log_error(error_msg)
            return {"error": str(e), "results": []}
    
    async def voice_input(self, audio_data: bytes) -> str:
        """Process voice input and return text response"""
        try:
            self.request_count += 1
            start_time = datetime.now()
            
            # Convert speech to text (placeholder for actual implementation)
            text = await self._speech_to_text(audio_data)
            
            # Process as chat message
            response = await self.chat(text, {"input_type": "voice"})
            
            # Log performance
            response_time = (datetime.now() - start_time).total_seconds()
            self.total_response_time += response_time
            
            self.logger.log_voice(text, response, response_time)
            
            return response
            
        except Exception as e:
            error_msg = f"Voice input error: {e}"
            self.logger.log_error(error_msg)
            return f"⚠️ Voice processing error: {e}"
    
    async def get_contextual_help(self, screen: str, element: Optional[str] = None) -> str:
        """Get context-sensitive help for current screen/element"""
        try:
            context = {
                "screen": screen,
                "element": element,
                "timestamp": datetime.now().isoformat()
            }
            
            self.context_manager.update_context(context)
            
            # Generate contextual help
            help_prompt = f"Provide helpful guidance for the {screen} screen"
            if element:
                help_prompt += f", specifically for the {element} element"
            
            response = await self.chat(help_prompt, context)
            
            return response
            
        except Exception as e:
            return f"⚠️ Unable to provide contextual help: {e}"
    
    def switch_provider(self, provider_name: str) -> bool:
        """Switch to a different AI provider"""
        try:
            success = self.provider_router.switch_provider(provider_name)
            if success:
                self.logger.log_info(f"Switched to AI provider: {provider_name}")
            else:
                self.logger.log_error(f"Failed to switch to provider: {provider_name}")
            return success
        except Exception as e:
            self.logger.log_error(f"Provider switch error: {e}")
            return False
    
    def get_performance_stats(self) -> Dict:
        """Get AI engine performance statistics"""
        avg_response_time = (
            self.total_response_time / self.request_count 
            if self.request_count > 0 else 0
        )
        
        return {
            "total_requests": self.request_count,
            "cache_hits": self.cache_hits,
            "cache_hit_rate": self.cache_hits / max(self.request_count, 1),
            "average_response_time": avg_response_time,
            "current_provider": self.provider_router.current_provider,
            "available_providers": self.provider_router.get_available_providers()
        }
    
    def _is_dangerous_command(self, command: str) -> bool:
        """Check if a command is potentially dangerous"""
        command_lower = command.lower()
        return any(dangerous in command_lower for dangerous in self.dangerous_commands)
    
    async def _enhance_search_results(self, search_results) -> Dict:
        """Enhance search results with AI insights"""
        # This would add AI-generated summaries, relevance scoring, etc.
        return {
            "query": search_results.query,
            "results": [
                {
                    "title": result.title,
                    "url": result.url,
                    "snippet": result.snippet,
                    "source": result.source,
                    "score": result.score,
                    "ai_summary": f"This result discusses {result.title.lower()}"
                }
                for result in search_results.results
            ],
            "total_results": len(search_results.results),
            "search_time": search_results.search_time,
            "ai_enhanced": True
        }
    
    async def _speech_to_text(self, audio_data: bytes) -> str:
        """Convert speech to text (placeholder implementation)"""
        # This would integrate with speech recognition services
        # For now, return a placeholder
        return "Voice input received (speech-to-text not yet implemented)"
    
    def shutdown(self):
        """Gracefully shutdown the AI interface"""
        self.logger.log_info("AI Interface shutting down")
        self.provider_router.shutdown()
        self.chat_engine.shutdown()
        self.logger.log_info("AI Interface shutdown complete")

# Global AI interface instance
ai_interface = AIInterface()
