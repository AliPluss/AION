"""
📊 AI Logger - Comprehensive Logging for All AI Operations
==========================================================

Writes AI responses, performance metrics, and interaction data to structured logs
for analysis, debugging, and performance optimization.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
import threading
from queue import Queue

@dataclass
class LogEntry:
    """Individual log entry with metadata"""
    timestamp: datetime
    log_type: str
    data: Dict[str, Any]
    session_id: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "log_type": self.log_type,
            "data": self.data,
            "session_id": self.session_id
        }

class AILogger:
    """Comprehensive AI logging system with async processing"""
    
    def __init__(self, max_queue_size: int = 1000):
        """Initialize AI logger"""
        self.max_queue_size = max_queue_size
        
        # Create log directories
        self.log_dirs = {
            "test_logs": Path("test_logs"),
            "chat_logs": Path("chat_logs"),
            "search_logs": Path("search_logs"),
            "voice_logs": Path("voice_logs"),
            "performance_logs": Path("performance_logs")
        }
        
        for log_dir in self.log_dirs.values():
            log_dir.mkdir(exist_ok=True)
        
        # Log files
        self.log_files = {
            "ai_terminal_assistant": self.log_dirs["test_logs"] / "ai_terminal_assistant.log",
            "chat_session": self.log_dirs["chat_logs"] / "session.log",
            "search_query": self.log_dirs["search_logs"] / "query.log",
            "voice_input": self.log_dirs["voice_logs"] / "input_output.log",
            "performance": self.log_dirs["performance_logs"] / "ai_performance.log",
            "errors": self.log_dirs["test_logs"] / "ai_errors.log"
        }
        
        # Async logging queue
        self.log_queue = Queue(maxsize=max_queue_size)
        self.logging_thread = threading.Thread(target=self._process_log_queue, daemon=True)
        self.logging_thread.start()
        
        # Performance tracking
        self.performance_stats = {
            "total_requests": 0,
            "total_response_time": 0.0,
            "error_count": 0,
            "cache_hits": 0,
            "provider_usage": {}
        }
        
        logging.info("AI Logger initialized successfully")
    
    def log_chat(self, user_message: str, ai_response: str, response_time: float, session_id: Optional[str] = None):
        """Log chat interaction"""
        log_data = {
            "user_message": user_message[:500],  # Truncate long messages
            "ai_response": ai_response[:1000],
            "response_time": response_time,
            "message_length": len(user_message),
            "response_length": len(ai_response)
        }
        
        self._queue_log("chat_interaction", log_data, session_id)
        self._update_performance_stats("chat", response_time)
    
    def log_chat_session_start(self, session_id: str):
        """Log chat session start"""
        log_data = {
            "action": "session_start",
            "session_id": session_id
        }
        
        self._queue_log("chat_session", log_data, session_id)
    
    def log_chat_interaction(self, session_id: str, user_message: str, ai_response: str, message_type: str):
        """Log detailed chat interaction"""
        log_data = {
            "session_id": session_id,
            "user_message": user_message[:500],
            "ai_response": ai_response[:1000],
            "message_type": message_type,
            "interaction_time": datetime.now().isoformat()
        }
        
        self._queue_log("chat_detailed", log_data, session_id)
    
    def log_search(self, query: str, results: Dict, response_time: float):
        """Log search operation"""
        log_data = {
            "query": query,
            "result_count": len(results.get("results", [])),
            "sources": results.get("sources", []),
            "response_time": response_time,
            "ai_enhanced": results.get("ai_enhanced", False)
        }
        
        self._queue_log("search_query", log_data)
        self._update_performance_stats("search", response_time)
    
    def log_explanation(self, command: str, explanation: str, response_time: float):
        """Log command explanation"""
        log_data = {
            "command": command,
            "explanation_length": len(explanation),
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        }
        
        self._queue_log("command_explanation", log_data)
        self._update_performance_stats("explanation", response_time)
    
    def log_command_explanation(self, command: str, security_level: str, explanation_length: int):
        """Log detailed command explanation"""
        log_data = {
            "command": command,
            "security_level": security_level,
            "explanation_length": explanation_length,
            "timestamp": datetime.now().isoformat()
        }
        
        self._queue_log("command_detailed", log_data)
    
    def log_voice(self, text_input: str, ai_response: str, response_time: float):
        """Log voice interaction"""
        log_data = {
            "text_input": text_input,
            "ai_response": ai_response[:1000],
            "response_time": response_time,
            "input_method": "voice"
        }
        
        self._queue_log("voice_interaction", log_data)
        self._update_performance_stats("voice", response_time)
    
    def log_context_update(self, screen: str, element: Optional[str], action: Optional[str]):
        """Log context updates"""
        log_data = {
            "screen": screen,
            "element": element,
            "action": action,
            "timestamp": datetime.now().isoformat()
        }
        
        self._queue_log("context_update", log_data)
    
    def log_provider_switch(self, old_provider: str, new_provider: str, reason: str):
        """Log AI provider switches"""
        log_data = {
            "old_provider": old_provider,
            "new_provider": new_provider,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        }
        
        self._queue_log("provider_switch", log_data)
    
    def log_error(self, error_message: str, error_type: str = "general", context: Optional[Dict] = None):
        """Log errors"""
        log_data = {
            "error_message": error_message,
            "error_type": error_type,
            "context": context or {},
            "timestamp": datetime.now().isoformat()
        }
        
        self._queue_log("error", log_data)
        self.performance_stats["error_count"] += 1
    
    def log_info(self, message: str, category: str = "general"):
        """Log informational messages"""
        log_data = {
            "message": message,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }
        
        self._queue_log("info", log_data)
    
    def log_performance_metrics(self, metrics: Dict[str, Any]):
        """Log performance metrics"""
        log_data = {
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }
        
        self._queue_log("performance", log_data)
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        avg_response_time = (
            self.performance_stats["total_response_time"] / 
            max(self.performance_stats["total_requests"], 1)
        )
        
        return {
            "total_requests": self.performance_stats["total_requests"],
            "average_response_time": avg_response_time,
            "error_count": self.performance_stats["error_count"],
            "error_rate": self.performance_stats["error_count"] / max(self.performance_stats["total_requests"], 1),
            "cache_hits": self.performance_stats["cache_hits"],
            "cache_hit_rate": self.performance_stats["cache_hits"] / max(self.performance_stats["total_requests"], 1),
            "provider_usage": self.performance_stats["provider_usage"]
        }
    
    def export_logs(self, log_type: str, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> str:
        """Export logs for analysis"""
        try:
            export_file = self.log_dirs["test_logs"] / f"export_{log_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # This would filter and export logs based on criteria
            # For now, return file path
            return str(export_file)
            
        except Exception as e:
            self.log_error(f"Log export failed: {e}", "export")
            return ""
    
    def _queue_log(self, log_type: str, data: Dict[str, Any], session_id: Optional[str] = None):
        """Queue log entry for async processing"""
        try:
            log_entry = LogEntry(
                timestamp=datetime.now(),
                log_type=log_type,
                data=data,
                session_id=session_id
            )
            
            if not self.log_queue.full():
                self.log_queue.put(log_entry)
            else:
                # Queue is full, log directly (blocking)
                self._write_log_entry(log_entry)
                
        except Exception as e:
            logging.error(f"Failed to queue log entry: {e}")
    
    def _process_log_queue(self):
        """Process log queue in background thread"""
        while True:
            try:
                log_entry = self.log_queue.get()
                if log_entry is None:  # Shutdown signal
                    break
                
                self._write_log_entry(log_entry)
                self.log_queue.task_done()
                
            except Exception as e:
                logging.error(f"Log processing error: {e}")
    
    def _write_log_entry(self, log_entry: LogEntry):
        """Write log entry to appropriate file"""
        try:
            # Determine target file based on log type
            if log_entry.log_type in ["chat_interaction", "chat_detailed", "chat_session"]:
                target_file = self.log_files["chat_session"]
            elif log_entry.log_type == "search_query":
                target_file = self.log_files["search_query"]
            elif log_entry.log_type == "voice_interaction":
                target_file = self.log_files["voice_input"]
            elif log_entry.log_type in ["command_explanation", "command_detailed"]:
                target_file = self.log_dirs["test_logs"] / "system_command_explanation.log"
            elif log_entry.log_type == "error":
                target_file = self.log_files["errors"]
            elif log_entry.log_type == "performance":
                target_file = self.log_files["performance"]
            else:
                target_file = self.log_files["ai_terminal_assistant"]
            
            # Write log entry
            with open(target_file, 'a', encoding='utf-8') as f:
                f.write(f"{json.dumps(log_entry.to_dict())}\n")
                
        except Exception as e:
            logging.error(f"Failed to write log entry: {e}")
    
    def _update_performance_stats(self, operation_type: str, response_time: float):
        """Update performance statistics"""
        self.performance_stats["total_requests"] += 1
        self.performance_stats["total_response_time"] += response_time
        
        if operation_type not in self.performance_stats["provider_usage"]:
            self.performance_stats["provider_usage"][operation_type] = 0
        self.performance_stats["provider_usage"][operation_type] += 1
    
    def shutdown(self):
        """Gracefully shutdown logger"""
        # Signal shutdown to background thread
        self.log_queue.put(None)
        
        # Wait for queue to be processed
        self.log_queue.join()
        
        # Wait for thread to finish
        if self.logging_thread.is_alive():
            self.logging_thread.join(timeout=5)
        
        logging.info("AI Logger shutdown complete")
