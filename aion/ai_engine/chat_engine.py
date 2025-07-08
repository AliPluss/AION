"""
💬 Chat Engine - Full Terminal Chat Assistant with Persistent Memory
===================================================================

Handles all /chat functionality with persistent AI chat overlay,
cross-screen support, and comprehensive conversation management.
"""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
import uuid

@dataclass
class ChatMessage:
    """Individual chat message with metadata"""
    id: str
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime
    context: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "context": self.context
        }

@dataclass
class ChatSession:
    """Complete chat session with messages and metadata"""
    session_id: str
    messages: List[ChatMessage]
    created_at: datetime
    last_activity: datetime
    total_tokens: int = 0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "session_id": self.session_id,
            "messages": [msg.to_dict() for msg in self.messages],
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "total_tokens": self.total_tokens
        }

class ChatEngine:
    """Advanced chat engine with persistent memory and context awareness"""
    
    def __init__(self, provider_router, ai_logger):
        """Initialize chat engine"""
        self.provider_router = provider_router
        self.ai_logger = ai_logger
        
        # Chat sessions
        self.current_session: Optional[ChatSession] = None
        self.sessions: Dict[str, ChatSession] = {}
        
        # Chat logs directory
        self.chat_logs_dir = Path("chat_logs")
        self.chat_logs_dir.mkdir(exist_ok=True)
        
        # Performance tracking
        self.total_messages = 0
        self.total_sessions = 0
        
        # Chat modes
        self.chat_modes = {
            "general": "General conversation and assistance",
            "code": "Code explanation and programming help",
            "debug": "Error analysis and debugging assistance",
            "aion": "AION-specific questions and guidance"
        }
        
        self.current_mode = "general"
        
        # Load existing sessions
        self._load_sessions()
        
        logging.info("Chat Engine initialized successfully")
    
    async def start_new_session(self) -> str:
        """Start a new chat session"""
        session_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        
        session = ChatSession(
            session_id=session_id,
            messages=[],
            created_at=datetime.now(),
            last_activity=datetime.now()
        )
        
        self.current_session = session
        self.sessions[session_id] = session
        self.total_sessions += 1
        
        # Log session start
        self.ai_logger.log_chat_session_start(session_id)
        
        # Save initial session
        await self._save_session(session)
        
        logging.info(f"Started new chat session: {session_id}")
        return session_id
    
    async def process_message(self, message: str, context: Optional[Dict] = None) -> str:
        """Process a chat message and return AI response"""
        
        # Start new session if none exists
        if not self.current_session:
            await self.start_new_session()
        
        try:
            # Create user message
            user_message = ChatMessage(
                id=str(uuid.uuid4()),
                role="user",
                content=message,
                timestamp=datetime.now(),
                context=context
            )
            
            # Add to session
            self.current_session.messages.append(user_message)
            self.current_session.last_activity = datetime.now()
            self.total_messages += 1
            
            # Determine message type and generate appropriate response
            message_type = self._classify_message(message)
            response_content = await self._generate_response(message, message_type, context)
            
            # Create assistant message
            assistant_message = ChatMessage(
                id=str(uuid.uuid4()),
                role="assistant",
                content=response_content,
                timestamp=datetime.now(),
                context={"message_type": message_type}
            )
            
            # Add to session
            self.current_session.messages.append(assistant_message)
            self.current_session.last_activity = datetime.now()
            
            # Save session
            await self._save_session(self.current_session)
            
            # Log the interaction
            self.ai_logger.log_chat_interaction(
                self.current_session.session_id,
                message,
                response_content,
                message_type
            )
            
            return response_content
            
        except Exception as e:
            error_msg = f"Chat processing error: {e}"
            logging.error(error_msg)
            self.ai_logger.log_error(error_msg)
            return f"⚠️ I encountered an error processing your message: {e}"
    
    def _classify_message(self, message: str) -> str:
        """Classify message type for appropriate response generation"""
        message_lower = message.lower()
        
        # Code-related keywords
        code_keywords = ['code', 'function', 'class', 'variable', 'error', 'bug', 'debug', 
                        'syntax', 'python', 'javascript', 'rust', 'c++', 'programming']
        
        # AION-specific keywords
        aion_keywords = ['aion', 'plugin', 'sandbox', 'terminal', 'command', 'interface',
                        'tui', 'cli', 'settings', 'configuration']
        
        # Error/debugging keywords
        debug_keywords = ['error', 'exception', 'traceback', 'failed', 'broken', 'fix',
                         'troubleshoot', 'problem', 'issue']
        
        if any(keyword in message_lower for keyword in debug_keywords):
            return "debug"
        elif any(keyword in message_lower for keyword in code_keywords):
            return "code"
        elif any(keyword in message_lower for keyword in aion_keywords):
            return "aion"
        else:
            return "general"
    
    async def _generate_response(self, message: str, message_type: str, context: Optional[Dict] = None) -> str:
        """Generate appropriate response based on message type"""
        
        # Build context-aware prompt
        conversation_history = self._get_conversation_context()
        
        if message_type == "code":
            prompt = self._build_code_prompt(message, conversation_history, context)
        elif message_type == "debug":
            prompt = self._build_debug_prompt(message, conversation_history, context)
        elif message_type == "aion":
            prompt = self._build_aion_prompt(message, conversation_history, context)
        else:
            prompt = self._build_general_prompt(message, conversation_history, context)
        
        # Get AI response
        response = await self.provider_router.query(prompt, context)
        
        return response
    
    def _build_code_prompt(self, message: str, history: str, context: Optional[Dict] = None) -> str:
        """Build prompt for code-related questions"""
        return f"""You are an expert programming assistant helping with code-related questions in the AION terminal.

Context: User is asking about programming/code in AION terminal environment.
Recent conversation:
{history}

Current question: {message}

Provide a helpful, technical response with:
- Clear explanations
- Code examples if relevant
- Best practices
- AION-specific considerations if applicable

Response:"""
    
    def _build_debug_prompt(self, message: str, history: str, context: Optional[Dict] = None) -> str:
        """Build prompt for debugging/error questions"""
        return f"""You are a debugging expert helping to solve technical problems in AION.

Context: User is experiencing an error or technical issue.
Recent conversation:
{history}

Problem description: {message}

Provide a systematic debugging response with:
- Problem analysis
- Possible causes
- Step-by-step solutions
- Prevention tips
- AION-specific troubleshooting if relevant

Response:"""
    
    def _build_aion_prompt(self, message: str, history: str, context: Optional[Dict] = None) -> str:
        """Build prompt for AION-specific questions"""
        return f"""You are the AION AI assistant, expert in all AION terminal features and functionality.

Context: User is asking about AION features, commands, or usage.
Recent conversation:
{history}

AION question: {message}

Provide comprehensive guidance about:
- AION features and capabilities
- Command usage and examples
- Interface navigation
- Configuration options
- Best practices for AION usage

Response:"""
    
    def _build_general_prompt(self, message: str, history: str, context: Optional[Dict] = None) -> str:
        """Build prompt for general conversation"""
        return f"""You are a helpful AI assistant in the AION terminal environment.

Recent conversation:
{history}

User message: {message}

Provide a helpful, friendly response that:
- Addresses the user's question directly
- Is conversational and engaging
- Offers additional relevant information
- Maintains context from previous messages

Response:"""
    
    def _get_conversation_context(self, limit: int = 5) -> str:
        """Get recent conversation context for prompts"""
        if not self.current_session or not self.current_session.messages:
            return "No previous conversation."
        
        recent_messages = self.current_session.messages[-limit*2:]  # Get last few exchanges
        
        context_lines = []
        for msg in recent_messages:
            role_prefix = "User" if msg.role == "user" else "Assistant"
            context_lines.append(f"{role_prefix}: {msg.content[:200]}...")
        
        return "\n".join(context_lines)
    
    async def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of current chat session"""
        if not self.current_session:
            return {"error": "No active session"}
        
        return {
            "session_id": self.current_session.session_id,
            "message_count": len(self.current_session.messages),
            "created_at": self.current_session.created_at.isoformat(),
            "duration_minutes": self._get_session_duration(),
            "last_activity": self.current_session.last_activity.isoformat(),
            "total_tokens": self.current_session.total_tokens
        }
    
    async def export_session(self, session_id: Optional[str] = None) -> str:
        """Export chat session to file"""
        session = self.sessions.get(session_id) if session_id else self.current_session
        
        if not session:
            return "No session to export"
        
        export_file = self.chat_logs_dir / f"export_{session.session_id}.json"
        
        try:
            with open(export_file, 'w') as f:
                json.dump(session.to_dict(), f, indent=2)
            
            return f"Session exported to: {export_file}"
            
        except Exception as e:
            return f"Export failed: {e}"
    
    async def clear_session(self):
        """Clear current session messages"""
        if self.current_session:
            self.current_session.messages.clear()
            self.current_session.last_activity = datetime.now()
            await self._save_session(self.current_session)
            logging.info(f"Cleared session: {self.current_session.session_id}")
    
    def get_chat_stats(self) -> Dict[str, Any]:
        """Get chat engine statistics"""
        return {
            "total_sessions": self.total_sessions,
            "total_messages": self.total_messages,
            "active_sessions": len(self.sessions),
            "current_session_id": self.current_session.session_id if self.current_session else None,
            "current_mode": self.current_mode,
            "available_modes": list(self.chat_modes.keys())
        }
    
    def _get_session_duration(self) -> int:
        """Get current session duration in minutes"""
        if not self.current_session:
            return 0
        
        duration = datetime.now() - self.current_session.created_at
        return int(duration.total_seconds() / 60)
    
    async def _save_session(self, session: ChatSession):
        """Save chat session to file"""
        try:
            session_file = self.chat_logs_dir / f"session_{session.session_id}.json"
            
            with open(session_file, 'w') as f:
                json.dump(session.to_dict(), f, indent=2)
                
        except Exception as e:
            logging.error(f"Failed to save chat session: {e}")
    
    def _load_sessions(self):
        """Load existing chat sessions"""
        try:
            for session_file in self.chat_logs_dir.glob("session_*.json"):
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                
                # Simplified loading - would need full deserialization
                logging.info(f"Found existing session: {session_data['session_id']}")
                
        except Exception as e:
            logging.error(f"Failed to load chat sessions: {e}")
    
    def shutdown(self):
        """Gracefully shutdown chat engine"""
        if self.current_session:
            asyncio.create_task(self._save_session(self.current_session))
        
        logging.info("Chat Engine shutdown complete")
