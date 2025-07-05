"""
🔐 AION Dynamic Security System
HMAC-SHA256 based security with time-based token generation
"""

import hashlib
import hmac
import time
import secrets
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pathlib import Path

class SecurityManager:
    """Dynamic security system for AION"""
    
    def __init__(self):
        self.secret_key = self._get_or_create_secret_key()
        self.session_tokens: Dict[str, Dict[str, Any]] = {}
        self.token_lifetime = 3600  # 1 hour in seconds
        self.max_attempts = 3
        self.lockout_duration = 300  # 5 minutes
        self.failed_attempts: Dict[str, Dict[str, Any]] = {}
    
    def _get_or_create_secret_key(self) -> bytes:
        """Get or create a secret key for HMAC operations"""
        key_file = Path.home() / ".aion" / "security.key"
        
        try:
            if key_file.exists():
                with open(key_file, 'rb') as f:
                    return f.read()
            else:
                # Create new secret key
                key_file.parent.mkdir(exist_ok=True)
                secret_key = secrets.token_bytes(32)  # 256-bit key
                with open(key_file, 'wb') as f:
                    f.write(secret_key)
                # Set restrictive permissions (Unix-like systems)
                if hasattr(os, 'chmod'):
                    os.chmod(key_file, 0o600)
                return secret_key
        except Exception as e:
            # Fallback to environment-based key
            env_key = os.environ.get('AION_SECRET_KEY')
            if env_key:
                return env_key.encode('utf-8')
            else:
                # Generate temporary key (not persistent)
                return secrets.token_bytes(32)
    
    def generate_session_token(self, user_id: str = "default") -> str:
        """Generate a time-based session token"""
        timestamp = int(time.time())
        
        # Create payload
        payload = f"{user_id}:{timestamp}:{secrets.token_hex(16)}"
        
        # Generate HMAC signature
        signature = hmac.new(
            self.secret_key,
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Combine payload and signature
        token = f"{payload}:{signature}"
        
        # Store token info
        self.session_tokens[token] = {
            'user_id': user_id,
            'created_at': timestamp,
            'last_used': timestamp,
            'is_active': True
        }
        
        return token
    
    def validate_token(self, token: str) -> bool:
        """Validate a session token"""
        try:
            # Check if token exists in our records
            if token not in self.session_tokens:
                return False
            
            token_info = self.session_tokens[token]
            
            # Check if token is active
            if not token_info.get('is_active', False):
                return False
            
            # Check token expiration
            current_time = int(time.time())
            if current_time - token_info['created_at'] > self.token_lifetime:
                self._invalidate_token(token)
                return False
            
            # Parse token components
            parts = token.split(':')
            if len(parts) != 4:
                return False
            
            user_id, timestamp, nonce, signature = parts
            
            # Reconstruct payload
            payload = f"{user_id}:{timestamp}:{nonce}"
            
            # Verify HMAC signature
            expected_signature = hmac.new(
                self.secret_key,
                payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                return False
            
            # Update last used timestamp
            token_info['last_used'] = current_time
            
            return True
            
        except Exception as e:
            print(f"Token validation error: {e}")
            return False
    
    def _invalidate_token(self, token: str):
        """Invalidate a specific token"""
        if token in self.session_tokens:
            self.session_tokens[token]['is_active'] = False
    
    def cleanup_expired_tokens(self):
        """Remove expired tokens from memory"""
        current_time = int(time.time())
        expired_tokens = []
        
        for token, info in self.session_tokens.items():
            if current_time - info['created_at'] > self.token_lifetime:
                expired_tokens.append(token)
        
        for token in expired_tokens:
            del self.session_tokens[token]
    
    def check_rate_limit(self, identifier: str, max_requests: int = 10, window: int = 60) -> bool:
        """Check if identifier is within rate limits"""
        current_time = int(time.time())
        
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = {
                'count': 0,
                'window_start': current_time,
                'locked_until': 0
            }
        
        attempt_info = self.failed_attempts[identifier]
        
        # Check if currently locked out
        if current_time < attempt_info['locked_until']:
            return False
        
        # Reset window if expired
        if current_time - attempt_info['window_start'] > window:
            attempt_info['count'] = 0
            attempt_info['window_start'] = current_time
            attempt_info['locked_until'] = 0
        
        # Check rate limit
        if attempt_info['count'] >= max_requests:
            attempt_info['locked_until'] = current_time + self.lockout_duration
            return False
        
        return True
    
    def record_failed_attempt(self, identifier: str):
        """Record a failed authentication attempt"""
        current_time = int(time.time())
        
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = {
                'count': 0,
                'window_start': current_time,
                'locked_until': 0
            }
        
        self.failed_attempts[identifier]['count'] += 1
        
        # Lock out if too many attempts
        if self.failed_attempts[identifier]['count'] >= self.max_attempts:
            self.failed_attempts[identifier]['locked_until'] = current_time + self.lockout_duration
    
    def is_command_allowed(self, command: str, user_level: str = "user") -> bool:
        """Check if a command is allowed for the user level"""
        # Define restricted commands
        restricted_commands = {
            "admin": [],  # Admin can run everything
            "user": [
                "rm -rf", "del /f", "format", "fdisk",
                "shutdown", "reboot", "halt", "poweroff",
                "passwd", "sudo", "su", "chmod 777",
                "dd if=", "mkfs", "parted", "gparted"
            ],
            "guest": [
                "rm", "del", "move", "mv", "cp", "copy",
                "mkdir", "rmdir", "touch", "nano", "vim",
                "git", "npm", "pip", "cargo", "go"
            ]
        }
        
        if user_level not in restricted_commands:
            user_level = "guest"
        
        blocked_commands = restricted_commands[user_level]
        
        # Check if command contains any blocked patterns
        command_lower = command.lower().strip()
        for blocked in blocked_commands:
            if blocked.lower() in command_lower:
                return False
        
        return True
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get current security status"""
        current_time = int(time.time())
        active_tokens = sum(1 for info in self.session_tokens.values() 
                          if info.get('is_active', False) and 
                          current_time - info['created_at'] <= self.token_lifetime)
        
        return {
            'active_sessions': active_tokens,
            'total_tokens': len(self.session_tokens),
            'failed_attempts': len(self.failed_attempts),
            'security_level': 'high',
            'last_cleanup': current_time
        }

    def is_command_safe(self, command: str) -> bool:
        """Check if command is safe to execute"""
        return self.is_command_allowed(command, "guest")

    def log_security_event(self, event: str):
        """Log security events"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] SECURITY: {event}"
        print(log_entry)  # In production, use proper logging
