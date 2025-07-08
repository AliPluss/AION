"""
🧠 Context Manager - Screen Context, History, and Session Memory
===============================================================

Tracks user context across all AION screens and maintains conversation history
for context-aware AI responses and intelligent assistance.
"""

import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import deque

@dataclass
class ContextEntry:
    """Single context entry with timestamp and metadata"""
    screen: str
    element: Optional[str]
    action: Optional[str]
    data: Dict[str, Any]
    timestamp: datetime
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "screen": self.screen,
            "element": self.element,
            "action": self.action,
            "data": self.data,
            "timestamp": self.timestamp.isoformat()
        }

@dataclass
class SessionMemory:
    """Session memory for AI conversations"""
    session_id: str
    messages: List[Dict[str, str]]
    context_history: List[ContextEntry]
    created_at: datetime
    last_activity: datetime
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "session_id": self.session_id,
            "messages": self.messages,
            "context_history": [entry.to_dict() for entry in self.context_history],
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat()
        }

class ContextManager:
    """Manages context awareness and session memory for AI interactions"""
    
    def __init__(self, max_context_entries: int = 100, max_session_age_hours: int = 24):
        """Initialize context manager"""
        self.max_context_entries = max_context_entries
        self.max_session_age_hours = max_session_age_hours
        
        # Current context tracking
        self.current_screen = "main"
        self.current_element = None
        self.context_history = deque(maxlen=max_context_entries)
        
        # Session memory
        self.current_session_id = self._generate_session_id()
        self.sessions: Dict[str, SessionMemory] = {}
        self.current_session = SessionMemory(
            session_id=self.current_session_id,
            messages=[],
            context_history=[],
            created_at=datetime.now(),
            last_activity=datetime.now()
        )
        self.sessions[self.current_session_id] = self.current_session
        
        # Context patterns for intelligent assistance
        self.screen_contexts = {
            "main": {
                "description": "Main AION interface with navigation options",
                "available_actions": ["navigate", "search", "chat", "settings"],
                "help_topics": ["navigation", "commands", "features"]
            },
            "plugin_manager": {
                "description": "Plugin management and execution interface",
                "available_actions": ["install", "execute", "configure", "remove"],
                "help_topics": ["plugin_installation", "plugin_execution", "security"]
            },
            "file_editor": {
                "description": "Code editor with syntax highlighting",
                "available_actions": ["edit", "save", "run", "format"],
                "help_topics": ["editing", "syntax", "execution", "debugging"]
            },
            "sandbox": {
                "description": "Secure code execution environment",
                "available_actions": ["execute", "configure", "monitor", "cleanup"],
                "help_topics": ["security", "execution", "monitoring", "limits"]
            },
            "settings": {
                "description": "AION configuration and preferences",
                "available_actions": ["configure", "save", "reset", "export"],
                "help_topics": ["configuration", "preferences", "backup", "restore"]
            },
            "chat": {
                "description": "AI chat interface for conversations",
                "available_actions": ["message", "clear", "save", "export"],
                "help_topics": ["conversation", "commands", "history", "export"]
            }
        }
        
        # Load existing sessions
        self._load_sessions()
        
        logging.info(f"Context Manager initialized with session {self.current_session_id}")
    
    def update_context(self, context: Dict[str, Any]):
        """Update current context with new information"""
        screen = context.get("screen", self.current_screen)
        element = context.get("element", self.current_element)
        action = context.get("action")
        data = context.get("data", {})
        
        # Update current state
        self.current_screen = screen
        self.current_element = element
        
        # Create context entry
        entry = ContextEntry(
            screen=screen,
            element=element,
            action=action,
            data=data,
            timestamp=datetime.now()
        )
        
        # Add to history
        self.context_history.append(entry)
        self.current_session.context_history.append(entry)
        self.current_session.last_activity = datetime.now()
        
        # Save context
        self._save_context()
        
        logging.debug(f"Context updated: {screen}/{element} - {action}")
    
    def get_current_context(self) -> Dict[str, Any]:
        """Get current context information"""
        screen_info = self.screen_contexts.get(self.current_screen, {})
        
        recent_actions = [
            entry.to_dict() for entry in list(self.context_history)[-5:]
        ]
        
        return {
            "current_screen": self.current_screen,
            "current_element": self.current_element,
            "screen_description": screen_info.get("description", ""),
            "available_actions": screen_info.get("available_actions", []),
            "help_topics": screen_info.get("help_topics", []),
            "recent_actions": recent_actions,
            "session_id": self.current_session_id,
            "session_duration": self._get_session_duration(),
            "total_interactions": len(self.current_session.messages)
        }
    
    def get_contextual_prompt(self, user_message: str) -> str:
        """Generate context-aware prompt for AI"""
        context = self.get_current_context()
        
        # Build contextual prompt
        prompt_parts = [
            f"User is currently on the '{context['current_screen']}' screen in AION.",
            f"Screen description: {context['screen_description']}"
        ]
        
        if context['current_element']:
            prompt_parts.append(f"Currently focused on: {context['current_element']}")
        
        if context['available_actions']:
            prompt_parts.append(f"Available actions: {', '.join(context['available_actions'])}")
        
        if context['recent_actions']:
            recent = context['recent_actions'][-1]
            prompt_parts.append(f"Recent action: {recent['action']} on {recent['screen']}")
        
        prompt_parts.extend([
            f"Session duration: {context['session_duration']} minutes",
            f"Total interactions: {context['total_interactions']}",
            "",
            f"User message: {user_message}",
            "",
            "Provide a helpful, context-aware response that considers the user's current location and recent actions in AION."
        ])
        
        return "\n".join(prompt_parts)
    
    def add_message(self, role: str, content: str):
        """Add message to current session"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.current_session.messages.append(message)
        self.current_session.last_activity = datetime.now()
        
        # Limit message history
        if len(self.current_session.messages) > 50:
            self.current_session.messages = self.current_session.messages[-50:]
        
        self._save_sessions()
    
    def get_conversation_history(self, limit: int = 10) -> List[Dict[str, str]]:
        """Get recent conversation history"""
        return self.current_session.messages[-limit:]
    
    def start_new_session(self) -> str:
        """Start a new session and return session ID"""
        # Save current session
        self._save_sessions()
        
        # Create new session
        self.current_session_id = self._generate_session_id()
        self.current_session = SessionMemory(
            session_id=self.current_session_id,
            messages=[],
            context_history=[],
            created_at=datetime.now(),
            last_activity=datetime.now()
        )
        self.sessions[self.current_session_id] = self.current_session
        
        logging.info(f"Started new session: {self.current_session_id}")
        return self.current_session_id
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of current session"""
        return {
            "session_id": self.current_session_id,
            "created_at": self.current_session.created_at.isoformat(),
            "duration_minutes": self._get_session_duration(),
            "message_count": len(self.current_session.messages),
            "context_entries": len(self.current_session.context_history),
            "screens_visited": list(set(
                entry.screen for entry in self.current_session.context_history
            )),
            "most_used_screen": self._get_most_used_screen()
        }
    
    def cleanup_old_sessions(self):
        """Remove old sessions to free memory"""
        cutoff_time = datetime.now() - timedelta(hours=self.max_session_age_hours)
        
        old_sessions = [
            session_id for session_id, session in self.sessions.items()
            if session.last_activity < cutoff_time and session_id != self.current_session_id
        ]
        
        for session_id in old_sessions:
            del self.sessions[session_id]
        
        if old_sessions:
            logging.info(f"Cleaned up {len(old_sessions)} old sessions")
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(datetime.now()) % 10000:04d}"
    
    def _get_session_duration(self) -> int:
        """Get session duration in minutes"""
        duration = datetime.now() - self.current_session.created_at
        return int(duration.total_seconds() / 60)
    
    def _get_most_used_screen(self) -> str:
        """Get the most frequently used screen in current session"""
        if not self.current_session.context_history:
            return self.current_screen
        
        screen_counts = {}
        for entry in self.current_session.context_history:
            screen_counts[entry.screen] = screen_counts.get(entry.screen, 0) + 1
        
        return max(screen_counts, key=screen_counts.get)
    
    def _save_context(self):
        """Save current context to file"""
        try:
            context_dir = Path("context_logs")
            context_dir.mkdir(exist_ok=True)
            
            context_file = context_dir / f"context_{self.current_session_id}.json"
            
            context_data = {
                "current_screen": self.current_screen,
                "current_element": self.current_element,
                "context_history": [entry.to_dict() for entry in self.context_history],
                "last_updated": datetime.now().isoformat()
            }
            
            with open(context_file, 'w') as f:
                json.dump(context_data, f, indent=2)
                
        except Exception as e:
            logging.error(f"Failed to save context: {e}")
    
    def _save_sessions(self):
        """Save all sessions to file"""
        try:
            sessions_dir = Path("session_logs")
            sessions_dir.mkdir(exist_ok=True)
            
            sessions_file = sessions_dir / "sessions.json"
            
            sessions_data = {
                session_id: session.to_dict()
                for session_id, session in self.sessions.items()
            }
            
            with open(sessions_file, 'w') as f:
                json.dump(sessions_data, f, indent=2)
                
        except Exception as e:
            logging.error(f"Failed to save sessions: {e}")
    
    def _load_sessions(self):
        """Load existing sessions from file"""
        try:
            sessions_file = Path("session_logs/sessions.json")
            
            if sessions_file.exists():
                with open(sessions_file, 'r') as f:
                    sessions_data = json.load(f)
                
                # Load sessions (simplified - would need full deserialization)
                logging.info(f"Loaded {len(sessions_data)} existing sessions")
                
        except Exception as e:
            logging.error(f"Failed to load sessions: {e}")

    def get_screen_help(self, screen: str) -> Dict[str, Any]:
        """Get help information for specific screen"""
        return self.screen_contexts.get(screen, {
            "description": f"Unknown screen: {screen}",
            "available_actions": [],
            "help_topics": []
        })
