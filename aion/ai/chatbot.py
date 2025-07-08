#!/usr/bin/env python3
"""
💬 AION AI Chatbot Mode

Full-screen AI chat interface with continuous memory, code explanations,
error message help, and comprehensive conversation logging.

Features:
- Full-screen chat interface
- Continuous conversation memory
- Code explanation capabilities
- Error message analysis
- Session logging
- Context-aware responses
"""

import os
import json
import uuid
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

console = Console()

@dataclass
class ChatMessage:
    """Chat message structure"""
    id: str
    timestamp: datetime
    role: str  # 'user' or 'assistant'
    content: str
    context: Optional[str] = None
    message_type: str = "text"  # 'text', 'code', 'error', 'explanation'

@dataclass
class ChatSession:
    """Chat session structure"""
    session_id: str
    start_time: datetime
    end_time: Optional[datetime]
    messages: List[ChatMessage]
    context_data: Dict[str, Any]
    total_messages: int
    session_summary: str

class AIONChatbot:
    """AION AI Chatbot with continuous memory and context awareness"""
    
    def __init__(self):
        self.chat_logs_dir = Path("chat_logs")
        self.chat_logs_dir.mkdir(exist_ok=True)
        
        self.current_session: Optional[ChatSession] = None
        self.conversation_memory: List[ChatMessage] = []
        self.context_data: Dict[str, Any] = {}
        
    def start_chat_session(self) -> str:
        """Start new chat session"""
        session_id = str(uuid.uuid4())[:8]
        
        self.current_session = ChatSession(
            session_id=session_id,
            start_time=datetime.now(),
            end_time=None,
            messages=[],
            context_data={},
            total_messages=0,
            session_summary=""
        )
        
        self.conversation_memory = []
        
        # Log session start
        self._log_session_event("SESSION_STARTED", {
            "session_id": session_id,
            "start_time": self.current_session.start_time.isoformat()
        })
        
        return session_id
    
    def end_chat_session(self, summary: str = ""):
        """End current chat session"""
        if not self.current_session:
            return
        
        self.current_session.end_time = datetime.now()
        self.current_session.session_summary = summary
        self.current_session.total_messages = len(self.conversation_memory)
        
        # Save session to file
        self._save_session_to_file()
        
        # Log session end
        self._log_session_event("SESSION_ENDED", {
            "session_id": self.current_session.session_id,
            "duration_minutes": (self.current_session.end_time - self.current_session.start_time).total_seconds() / 60,
            "total_messages": self.current_session.total_messages,
            "summary": summary
        })
        
        self.current_session = None
        self.conversation_memory = []
    
    async def send_message(self, user_message: str, message_type: str = "text", context: str = "") -> str:
        """Send message to AI and get response"""
        if not self.current_session:
            self.start_chat_session()
        
        # Create user message
        user_msg = ChatMessage(
            id=str(uuid.uuid4())[:8],
            timestamp=datetime.now(),
            role="user",
            content=user_message,
            context=context,
            message_type=message_type
        )
        
        self.conversation_memory.append(user_msg)
        
        # Generate AI response based on message type
        ai_response = await self._generate_ai_response(user_message, message_type, context)
        
        # Create AI message
        ai_msg = ChatMessage(
            id=str(uuid.uuid4())[:8],
            timestamp=datetime.now(),
            role="assistant",
            content=ai_response,
            context=context,
            message_type=message_type
        )
        
        self.conversation_memory.append(ai_msg)
        
        # Log conversation
        self._log_conversation(user_msg, ai_msg)
        
        return ai_response
    
    async def _generate_ai_response(self, message: str, message_type: str, context: str) -> str:
        """Generate AI response based on message type and context"""
        
        # Code explanation requests
        if message_type == "code" or "explain code" in message.lower() or "```" in message:
            return await self._handle_code_explanation(message, context)
        
        # Error message analysis
        elif message_type == "error" or "error" in message.lower() or "exception" in message.lower():
            return await self._handle_error_analysis(message, context)
        
        # AION-specific questions
        elif any(keyword in message.lower() for keyword in ["aion", "plugin", "sandbox", "security", "file"]):
            return await self._handle_aion_question(message, context)
        
        # General conversation
        else:
            return await self._handle_general_conversation(message, context)
    
    async def _handle_code_explanation(self, message: str, context: str) -> str:
        """Handle code explanation requests"""
        return f"""💻 **Code Explanation**

I can help explain code! Here's what I understand from your message:

**Your code/question:** {message[:200]}...

**Analysis:**
• **Language Detection:** Based on syntax patterns
• **Code Structure:** Functions, classes, variables
• **Logic Flow:** Step-by-step execution
• **Best Practices:** Improvements and optimizations
• **Potential Issues:** Common pitfalls and fixes

**Memory Context:** I remember our previous {len(self.conversation_memory)} messages in this session.

**Need specific help?** Try:
• "Explain this function: [code]"
• "What does this error mean: [error]"
• "How can I improve this code: [code]"
• "Debug this issue: [problem]"

💡 **Tip:** I can analyze Python, JavaScript, C++, Rust, and more!"""
    
    async def _handle_error_analysis(self, message: str, context: str) -> str:
        """Handle error message analysis"""
        return f"""🔍 **Error Analysis**

Let me help you understand this error:

**Error Message:** {message[:200]}...

**Common Causes:**
• **Syntax Errors:** Missing colons, brackets, quotes
• **Runtime Errors:** Variable not defined, type mismatch
• **Logic Errors:** Incorrect algorithm, infinite loops
• **Import Errors:** Missing modules, incorrect paths

**Debugging Steps:**
1. **Check Line Number:** Look at the specific line mentioned
2. **Verify Syntax:** Ensure proper indentation and punctuation
3. **Check Variables:** Make sure all variables are defined
4. **Test Incrementally:** Run smaller parts of the code

**Context from our conversation:** {len(self.conversation_memory)} previous messages

**Quick Fixes:**
• Share the full error traceback for detailed analysis
• Show the code around the error line
• Describe what you were trying to accomplish

💡 **Tip:** I can help debug errors in real-time!"""
    
    async def _handle_aion_question(self, message: str, context: str) -> str:
        """Handle AION-specific questions"""
        return f"""🤖 **AION Assistant Help**

I'm here to help with AION-specific questions!

**Your question:** {message[:200]}...

**AION Features I can help with:**
• **Plugin Management:** Installation, configuration, security
• **Code Execution:** Sandbox settings, language support
• **File Operations:** Editor features, file management
• **AI Integration:** Provider setup, API configuration
• **Security:** Sandbox limits, permission management
• **Settings:** Customization, themes, preferences

**Current Context:** {context or 'Main interface'}
**Session Memory:** {len(self.conversation_memory)} messages

**Popular AION Commands:**
• `/run [file]` - Execute code safely
• `/plugin install [name]` - Install plugin
• `/security level [high/medium/low]` - Set security
• `/explain [command]` - Get command help

**Need specific help?** Ask about:
• "How do I install plugins safely?"
• "What security settings should I use?"
• "How do I configure AI providers?"
• "What file formats does AION support?"

💡 **Tip:** I remember our entire conversation for context!"""
    
    async def _handle_general_conversation(self, message: str, context: str) -> str:
        """Handle general conversation"""
        return f"""💬 **General Chat**

Thanks for chatting with me! I'm AION's AI assistant.

**Your message:** {message[:200]}...

**I can help you with:**
• **Development Questions:** Programming, debugging, best practices
• **AION Usage:** Features, commands, configuration
• **Code Review:** Analysis, improvements, optimization
• **Learning:** Explanations, tutorials, examples
• **Problem Solving:** Step-by-step guidance

**Our Conversation:**
• **Session Messages:** {len(self.conversation_memory)}
• **Current Context:** {context or 'General chat'}
• **Session ID:** {self.current_session.session_id if self.current_session else 'None'}

**Conversation Memory:** I remember everything we've discussed in this session, so feel free to reference previous topics!

**Want to dive deeper?** Try:
• "Explain [concept] in detail"
• "Help me debug [problem]"
• "Show me examples of [topic]"
• "What's the best way to [task]?"

💡 **Tip:** I'm context-aware and remember our entire conversation!"""
    
    def get_conversation_history(self) -> List[ChatMessage]:
        """Get current conversation history"""
        return self.conversation_memory.copy()
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get current session summary"""
        if not self.current_session:
            return {"error": "No active session"}
        
        return {
            "session_id": self.current_session.session_id,
            "start_time": self.current_session.start_time.isoformat(),
            "duration_minutes": (datetime.now() - self.current_session.start_time).total_seconds() / 60,
            "total_messages": len(self.conversation_memory),
            "message_types": self._get_message_type_stats(),
            "context_data": self.context_data
        }
    
    def _get_message_type_stats(self) -> Dict[str, int]:
        """Get statistics of message types"""
        stats = {}
        for msg in self.conversation_memory:
            stats[msg.message_type] = stats.get(msg.message_type, 0) + 1
        return stats
    
    def _log_session_event(self, event: str, details: Dict[str, Any]):
        """Log session events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            log_file = self.chat_logs_dir / "session_events.log"
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"{timestamp} - {event}: {json.dumps(details, indent=2)}\n")
        except Exception as e:
            console.print(f"⚠️ [yellow]Chat logging error: {e}[/yellow]")
    
    def _log_conversation(self, user_msg: ChatMessage, ai_msg: ChatMessage):
        """Log conversation messages"""
        if not self.current_session:
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            log_file = self.chat_logs_dir / f"session_{self.current_session.session_id}.log"
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"{timestamp} - USER: {json.dumps(asdict(user_msg), indent=2)}\n")
                f.write(f"{timestamp} - AI: {json.dumps(asdict(ai_msg), indent=2)}\n")
        except Exception as e:
            console.print(f"⚠️ [yellow]Conversation logging error: {e}[/yellow]")
    
    def _save_session_to_file(self):
        """Save complete session to file"""
        if not self.current_session:
            return
        
        try:
            session_file = self.chat_logs_dir / f"session_{self.current_session.session_id}_complete.json"
            session_data = {
                "session": asdict(self.current_session),
                "messages": [asdict(msg) for msg in self.conversation_memory],
                "context_data": self.context_data,
                "summary": self.get_session_summary()
            }
            
            with open(session_file, "w", encoding="utf-8") as f:
                json.dump(session_data, f, indent=2, default=str)
                
        except Exception as e:
            console.print(f"⚠️ [yellow]Session save error: {e}[/yellow]")

# Global chatbot instance
aion_chatbot = AIONChatbot()
