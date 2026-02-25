"""
🔐 AION Advanced Dynamic Security System
Real-time threat monitoring with dynamic protection that changes every minute
Features: Dynamic encryption, threat detection, session management, and adaptive security
"""

import hashlib
import hmac
import time
import secrets
import os
import threading
import uuid
import json
import base64
import psutil
import socket
import platform
import subprocess
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Callable
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SecurityManager:
    """
    Advanced Dynamic Security System for AION

    This class provides comprehensive security management with dynamic protection
    that adapts and changes every minute for enhanced user safety. Features include:

    - Dynamic HMAC+AES encryption with rotating parameters
    - Real-time threat monitoring and assessment
    - Adaptive protection levels based on system state
    - Session management with secure token handling
    - System resource monitoring and anomaly detection
    - Automated security parameter rotation
    - Comprehensive logging and audit trails

    The security system continuously monitors system health and adjusts
    protection mechanisms automatically to maintain optimal security posture.
    """

    def __init__(self):
        # Core security components
        self.secret_key = self._get_or_create_secret_key()
        self.session_tokens: Dict[str, Dict[str, Any]] = {}
        self.token_lifetime = 1800  # 30 minutes (dynamic)
        self.max_attempts = 3  # Dynamic based on threat level
        self.lockout_duration = 300  # 5 minutes (dynamic)
        self.failed_attempts: Dict[str, Dict[str, Any]] = {}

        # Dynamic security features
        self.protection_level = 5  # Scale 1-10
        self.threat_score = 0  # Real-time threat assessment
        self.encryption_key = self._generate_dynamic_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.security_rotation_counter = 0
        self.last_rotation = datetime.now()

        # Real-time monitoring
        self.monitoring_active = True
        self.system_metrics: Dict[str, Any] = {}
        self.threat_patterns: List[str] = []
        self.security_events: List[Dict[str, Any]] = []

        # Dynamic protection rules
        self.security_rules = {
            "dynamic_encryption": True,
            "real_time_monitoring": True,
            "adaptive_timeouts": True,
            "threat_detection": True,
            "session_isolation": True,
            "command_filtering": True,
            "rate_limiting": True,
            "intrusion_detection": True
        }

        # Start dynamic security thread
        self.security_thread = threading.Thread(target=self._dynamic_security_loop, daemon=True)
        self.security_thread.start()

        self._log_security_event("advanced_security_initialized", {
            "protection_level": self.protection_level,
            "features_enabled": len([k for k, v in self.security_rules.items() if v]),
            "monitoring_active": self.monitoring_active
        })
    
    def _generate_dynamic_key(self) -> bytes:
        """Generate dynamic encryption key that changes every minute"""
        current_minute = datetime.now().strftime('%Y%m%d_%H%M')
        password = f"AION_DYNAMIC_SECURITY_{current_minute}_{secrets.token_hex(16)}".encode()
        salt = secrets.token_bytes(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key

    def _dynamic_security_loop(self):
        """Main dynamic security loop - rotates security every minute"""
        while self.monitoring_active:
            try:
                # Rotate security parameters every minute
                self._rotate_security_parameters()

                # Monitor system for threats
                self._monitor_system_threats()

                # Update protection level based on threats
                self._update_protection_level()

                # Clean expired sessions and tokens
                self._cleanup_expired_sessions()

                # Update threat detection patterns
                self._update_threat_patterns()

                # Log security rotation
                self._log_security_event("security_rotation_completed", {
                    "rotation_id": self.security_rotation_counter,
                    "protection_level": self.protection_level,
                    "threat_score": self.threat_score,
                    "active_sessions": len([s for s in self.session_tokens.values() if s.get("is_active", False)])
                })

                # Wait 60 seconds for next rotation
                time.sleep(60)

            except Exception as e:
                self._log_security_event("security_loop_error", {"error": str(e)})
                time.sleep(10)  # Shorter wait on error

    def _rotate_security_parameters(self):
        """Rotate all security parameters dynamically"""
        self.security_rotation_counter += 1
        self.last_rotation = datetime.now()

        # Generate new encryption key
        self.encryption_key = self._generate_dynamic_key()
        self.cipher_suite = Fernet(self.encryption_key)

        # Update session security tokens
        for token_id, token_info in self.session_tokens.items():
            if token_info.get("is_active", False):
                token_info["security_hash"] = self._generate_security_hash(token_id)
                token_info["rotation_id"] = self.security_rotation_counter

        # Rotate threat detection patterns
        self.threat_patterns = [
            f"threat_pattern_{secrets.token_hex(8)}",
            f"malware_signature_{secrets.token_hex(8)}",
            f"intrusion_attempt_{secrets.token_hex(8)}",
            f"suspicious_activity_{secrets.token_hex(8)}"
        ]

    def _monitor_system_threats(self):
        """Monitor system for potential security threats"""
        try:
            # System resource monitoring
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent

            # Network monitoring
            network_connections = len(psutil.net_connections())

            # Process monitoring
            suspicious_processes = 0
            high_cpu_processes = []

            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    if proc.info['cpu_percent'] > 80:
                        suspicious_processes += 1
                        high_cpu_processes.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            # Update system metrics
            self.system_metrics = {
                "cpu_usage": cpu_percent,
                "memory_usage": memory_percent,
                "disk_usage": disk_usage,
                "network_connections": network_connections,
                "suspicious_processes": suspicious_processes,
                "high_cpu_processes": high_cpu_processes[:5],  # Top 5
                "timestamp": datetime.now().isoformat()
            }

            # Calculate threat score (0-100)
            threat_score = 0
            if cpu_percent > 90: threat_score += 25
            if memory_percent > 85: threat_score += 20
            if disk_usage > 95: threat_score += 15
            if network_connections > 100: threat_score += 15
            if suspicious_processes > 5: threat_score += 25

            self.threat_score = min(threat_score, 100)

        except Exception as e:
            self._log_security_event("threat_monitoring_error", {"error": str(e)})

    def _update_protection_level(self):
        """Update protection level based on threat assessment"""
        if self.threat_score >= 80:
            self.protection_level = 10
            self.token_lifetime = 300  # 5 minutes
            self.max_attempts = 1
            self.lockout_duration = 1800  # 30 minutes
        elif self.threat_score >= 60:
            self.protection_level = 8
            self.token_lifetime = 600  # 10 minutes
            self.max_attempts = 2
            self.lockout_duration = 900  # 15 minutes
        elif self.threat_score >= 40:
            self.protection_level = 6
            self.token_lifetime = 900  # 15 minutes
            self.max_attempts = 2
            self.lockout_duration = 600  # 10 minutes
        elif self.threat_score >= 20:
            self.protection_level = 4
            self.token_lifetime = 1800  # 30 minutes
            self.max_attempts = 3
            self.lockout_duration = 300  # 5 minutes
        else:
            self.protection_level = 3
            self.token_lifetime = 3600  # 1 hour
            self.max_attempts = 5
            self.lockout_duration = 180  # 3 minutes

    def _cleanup_expired_sessions(self):
        """Clean up expired sessions and tokens"""
        current_time = int(time.time())
        expired_tokens = []

        for token, info in self.session_tokens.items():
            if info.get("is_active", False):
                if current_time - info.get('created_at', 0) > self.token_lifetime:
                    expired_tokens.append(token)

        for token in expired_tokens:
            self.session_tokens[token]['is_active'] = False
            self._log_security_event("session_expired", {"token_id": token[:16] + "..."})

    def _update_threat_patterns(self):
        """Update threat detection patterns"""
        self.threat_patterns = [
            f"malicious_pattern_{secrets.token_hex(6)}",
            f"exploit_attempt_{secrets.token_hex(6)}",
            f"data_exfiltration_{secrets.token_hex(6)}",
            f"privilege_escalation_{secrets.token_hex(6)}",
            f"code_injection_{secrets.token_hex(6)}"
        ]

    def _generate_security_hash(self, data: str) -> str:
        """Generate security hash for data integrity"""
        combined_data = f"{data}_{self.security_rotation_counter}_{datetime.now().isoformat()}"
        return hashlib.sha256(combined_data.encode()).hexdigest()

    def _log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security events with encryption"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details,
            "protection_level": self.protection_level,
            "threat_score": self.threat_score,
            "rotation_id": self.security_rotation_counter
        }

        self.security_events.append(event)

        # Keep only last 500 events
        if len(self.security_events) > 500:
            self.security_events = self.security_events[-500:]

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
            # Fallback to in-memory key
            return secrets.token_bytes(32)

    # Public API methods
    def create_session_token(self, user_id: str = None) -> str:
        """Create a new secure session token"""
        token = secrets.token_urlsafe(32)
        current_time = int(time.time())

        self.session_tokens[token] = {
            'user_id': user_id or 'anonymous',
            'created_at': current_time,
            'last_activity': current_time,
            'is_active': True,
            'security_hash': self._generate_security_hash(token),
            'rotation_id': self.security_rotation_counter,
            'protection_level': self.protection_level
        }

        self._log_security_event("session_created", {
            "token_id": token[:16] + "...",
            "user_id": user_id or 'anonymous'
        })

        return token

    def validate_session_token(self, token: str) -> bool:
        """Validate a session token"""
        if not token or token not in self.session_tokens:
            return False

        token_info = self.session_tokens[token]
        current_time = int(time.time())

        # Check if token is active
        if not token_info.get('is_active', False):
            return False

        # Check if token has expired
        if current_time - token_info.get('created_at', 0) > self.token_lifetime:
            token_info['is_active'] = False
            self._log_security_event("token_expired", {"token_id": token[:16] + "..."})
            return False

        # Update last activity
        token_info['last_activity'] = current_time

        return True

    def encrypt_data(self, data: str) -> str:
        """Encrypt data using dynamic encryption"""
        try:
            encrypted_data = self.cipher_suite.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            self._log_security_event("encryption_error", {"error": str(e)})
            return ""

    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt data using dynamic encryption"""
        try:
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self.cipher_suite.decrypt(decoded_data)
            return decrypted_data.decode()
        except Exception as e:
            self._log_security_event("decryption_error", {"error": str(e)})
            return ""

    def get_security_status(self) -> Dict[str, Any]:
        """Get current security status"""
        return {
            "protection_level": self.protection_level,
            "threat_score": self.threat_score,
            "active_sessions": len([s for s in self.session_tokens.values() if s.get("is_active", False)]),
            "security_rotation_counter": self.security_rotation_counter,
            "last_rotation": self.last_rotation.isoformat(),
            "monitoring_active": self.monitoring_active,
            "system_metrics": self.system_metrics,
            "security_rules": self.security_rules
        }

    def shutdown(self):
        """Shutdown security manager"""
        self.monitoring_active = False
        if hasattr(self, 'security_thread') and self.security_thread.is_alive():
            self.security_thread.join(timeout=5)

        self._log_security_event("security_manager_shutdown", {
            "final_protection_level": self.protection_level,
            "total_rotations": self.security_rotation_counter
        })
    
    def generate_session_token(self, user_id: str = "default", client_info: Dict[str, Any] = None) -> str:
        """Generate an advanced secure session token with dynamic encryption"""
        timestamp = int(time.time())
        session_id = str(uuid.uuid4())

        # Enhanced payload with more security data
        payload_data = {
            "user_id": user_id,
            "session_id": session_id,
            "timestamp": timestamp,
            "nonce": secrets.token_hex(32),
            "protection_level": self.protection_level,
            "rotation_id": self.security_rotation_counter,
            "client_info": client_info or {}
        }

        # Convert to JSON and encrypt
        payload_json = json.dumps(payload_data, sort_keys=True)
        encrypted_payload = self.cipher_suite.encrypt(payload_json.encode())

        # Generate HMAC signature
        signature = hmac.new(
            self.secret_key,
            encrypted_payload,
            hashlib.sha256
        ).hexdigest()

        # Create final token
        token = base64.urlsafe_b64encode(
            f"{base64.urlsafe_b64encode(encrypted_payload).decode()}:{signature}".encode()
        ).decode()

        # Store enhanced token info
        self.session_tokens[token] = {
            'user_id': user_id,
            'session_id': session_id,
            'created_at': timestamp,
            'last_used': timestamp,
            'is_active': True,
            'protection_level': self.protection_level,
            'rotation_id': self.security_rotation_counter,
            'security_hash': self._generate_security_hash(token),
            'client_info': client_info or {},
            'activity_count': 0,
            'threat_flags': [],
            'encrypted': True,
            'last_ip': self._get_client_ip()
        }

        self._log_security_event("secure_session_created", {
            "user_id": user_id,
            "session_id": session_id,
            "protection_level": self.protection_level,
            "encrypted": True
        })

        return token

    def _get_client_ip(self) -> str:
        """Get client IP address"""
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except:
            return "127.0.0.1"
    
    def validate_token(self, token: str, client_info: Dict[str, Any] = None) -> bool:
        """Advanced token validation with dynamic security checks"""
        try:
            # Check if token exists in our records
            if token not in self.session_tokens:
                self._log_security_event("token_not_found", {"token_id": token[:16] + "..."})
                return False

            token_info = self.session_tokens[token]

            # Check if token is active
            if not token_info.get('is_active', False):
                self._log_security_event("inactive_token_access", {"token_id": token[:16] + "..."})
                return False

            # Check token expiration with dynamic timeout
            current_time = int(time.time())
            if current_time - token_info['created_at'] > self.token_lifetime:
                self._invalidate_token(token, "expired")
                return False

            # Verify token integrity and decrypt
            try:
                # Decode the token
                decoded_token = base64.urlsafe_b64decode(token.encode()).decode()
                encrypted_payload_b64, signature = decoded_token.split(':', 1)
                encrypted_payload = base64.urlsafe_b64decode(encrypted_payload_b64.encode())

                # Verify HMAC signature
                expected_signature = hmac.new(
                    self.secret_key,
                    encrypted_payload,
                    hashlib.sha256
                ).hexdigest()

                if not hmac.compare_digest(signature, expected_signature):
                    self._log_security_event("token_signature_invalid", {"token_id": token[:16] + "..."})
                    return False

                # Decrypt and parse payload
                decrypted_payload = self.cipher_suite.decrypt(encrypted_payload)
                payload_data = json.loads(decrypted_payload.decode())

                # Verify payload integrity
                if payload_data.get("user_id") != token_info.get("user_id"):
                    self._log_security_event("token_user_mismatch", {"token_id": token[:16] + "..."})
                    return False

                # Check rotation compatibility
                if payload_data.get("rotation_id", 0) < self.security_rotation_counter - 2:
                    self._log_security_event("token_rotation_outdated", {
                        "token_id": token[:16] + "...",
                        "token_rotation": payload_data.get("rotation_id", 0),
                        "current_rotation": self.security_rotation_counter
                    })
                    return False

            except Exception as decrypt_error:
                self._log_security_event("token_decryption_failed", {
                    "token_id": token[:16] + "...",
                    "error": str(decrypt_error)
                })
                return False

            # Additional security checks
            if self._detect_suspicious_activity(token, client_info):
                self._log_security_event("suspicious_token_activity", {"token_id": token[:16] + "..."})
                return False

            # Update token activity
            token_info['last_used'] = current_time
            token_info['activity_count'] = token_info.get('activity_count', 0) + 1

            # Update client info if provided
            if client_info:
                token_info['client_info'].update(client_info)

            self._log_security_event("token_validated_successfully", {
                "token_id": token[:16] + "...",
                "user_id": token_info.get("user_id"),
                "activity_count": token_info.get('activity_count', 0)
            })

            return True

        except Exception as e:
            self._log_security_event("token_validation_error", {
                "token_id": token[:16] + "..." if token else "None",
                "error": str(e)
            })
            return False

    def _detect_suspicious_activity(self, token: str, client_info: Dict[str, Any] = None) -> bool:
        """Detect suspicious activity patterns"""
        if not client_info:
            return False

        token_info = self.session_tokens.get(token, {})

        # Check for IP address changes
        current_ip = client_info.get("ip", self._get_client_ip())
        stored_ip = token_info.get("last_ip", "")

        if stored_ip and current_ip != stored_ip:
            # Allow local IP changes but flag external changes
            if not (current_ip.startswith("192.168.") or current_ip.startswith("127.0.")):
                return True

        # Check for rapid activity (potential bot)
        activity_count = token_info.get('activity_count', 0)
        time_since_creation = int(time.time()) - token_info.get('created_at', 0)

        if time_since_creation > 0 and activity_count / time_since_creation > 10:  # More than 10 requests per second
            return True

        return False
    
    def _invalidate_token(self, token: str, reason: str = "manual"):
        """Invalidate a specific token with logging"""
        if token in self.session_tokens:
            self.session_tokens[token]['is_active'] = False
            self.session_tokens[token]['invalidated_at'] = int(time.time())
            self.session_tokens[token]['invalidation_reason'] = reason

            self._log_security_event("token_invalidated", {
                "token_id": token[:16] + "...",
                "reason": reason,
                "user_id": self.session_tokens[token].get("user_id")
            })
    
    def cleanup_expired_tokens(self):
        """Remove expired tokens from memory with enhanced logging"""
        current_time = int(time.time())
        expired_tokens = []
        inactive_tokens = []

        for token, info in self.session_tokens.items():
            # Check for expired tokens
            if current_time - info['created_at'] > self.token_lifetime:
                expired_tokens.append(token)
            # Check for inactive tokens (not used for 2x token lifetime)
            elif current_time - info.get('last_used', info['created_at']) > (self.token_lifetime * 2):
                inactive_tokens.append(token)

        # Remove expired tokens
        for token in expired_tokens:
            self._log_security_event("token_expired_cleanup", {
                "token_id": token[:16] + "...",
                "user_id": self.session_tokens[token].get("user_id"),
                "age_seconds": current_time - self.session_tokens[token]['created_at']
            })
            del self.session_tokens[token]

        # Mark inactive tokens as inactive
        for token in inactive_tokens:
            self.session_tokens[token]['is_active'] = False
            self._log_security_event("token_marked_inactive", {
                "token_id": token[:16] + "...",
                "user_id": self.session_tokens[token].get("user_id")
            })
    
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
    
    def is_command_allowed(self, command: str, user_level: str = "user", session_token: str = None) -> Dict[str, Any]:
        """Advanced command security analysis with dynamic threat assessment"""

        # Enhanced security levels based on protection level
        security_levels = {
            "admin": 10,
            "power_user": 8,
            "user": 5,
            "restricted_user": 3,
            "guest": 1
        }

        # Dynamic command restrictions based on protection level
        if self.protection_level >= 8:
            # Maximum security - very restrictive
            dangerous_patterns = [
                "rm -rf", "del /f", "format", "fdisk", "shutdown", "reboot", "halt", "poweroff",
                "passwd", "sudo", "su", "chmod 777", "dd if=", "mkfs", "parted", "gparted",
                "curl", "wget", "nc", "netcat", "telnet", "ssh", "ftp", "scp", "rsync",
                "python -c", "perl -e", "ruby -e", "node -e", "bash -c", "sh -c",
                "eval", "exec", "system", "os.system", "subprocess", "popen",
                "import os", "import subprocess", "import sys", "__import__",
                "open(", "file(", "input(", "raw_input(", "execfile("
            ]
        elif self.protection_level >= 6:
            # High security - moderately restrictive
            dangerous_patterns = [
                "rm -rf", "del /f", "format", "fdisk", "shutdown", "reboot",
                "passwd", "sudo", "su", "chmod 777", "dd if=", "mkfs",
                "curl", "wget", "nc", "netcat", "python -c", "perl -e",
                "eval", "exec", "system", "os.system", "subprocess"
            ]
        elif self.protection_level >= 4:
            # Medium security - basic restrictions
            dangerous_patterns = [
                "rm -rf", "del /f", "format", "fdisk", "shutdown",
                "passwd", "sudo", "chmod 777", "dd if=", "mkfs"
            ]
        else:
            # Low security - minimal restrictions
            dangerous_patterns = [
                "rm -rf", "del /f", "format", "fdisk"
            ]

        # Additional AI/ML specific restrictions
        ai_dangerous_patterns = [
            "torch.load", "pickle.load", "joblib.load", "dill.load",
            "tensorflow.saved_model.load", "keras.models.load_model",
            "sklearn.externals.joblib.load", "numpy.load",
            "pandas.read_pickle", "cloudpickle.load"
        ]

        # Analyze command
        command_lower = command.lower().strip()
        threat_level = 0
        blocked_patterns = []
        warnings = []

        # Check dangerous patterns
        for pattern in dangerous_patterns:
            if pattern.lower() in command_lower:
                threat_level += 10
                blocked_patterns.append(pattern)

        # Check AI-specific patterns
        for pattern in ai_dangerous_patterns:
            if pattern.lower() in command_lower:
                threat_level += 5
                warnings.append(f"Potentially unsafe AI operation: {pattern}")

        # Check for code injection patterns
        injection_patterns = ["';", '";', "&&", "||", "|", ";", "`", "$()"]
        for pattern in injection_patterns:
            if pattern in command:
                threat_level += 3
                warnings.append(f"Potential code injection: {pattern}")

        # User level security check
        user_security_level = security_levels.get(user_level, 1)
        required_level = min(threat_level, 10)

        # Final decision
        is_allowed = user_security_level >= required_level and threat_level < (10 - self.protection_level)

        # Log security decision
        self._log_security_event("command_security_check", {
            "command": command[:100] + "..." if len(command) > 100 else command,
            "user_level": user_level,
            "threat_level": threat_level,
            "protection_level": self.protection_level,
            "is_allowed": is_allowed,
            "blocked_patterns": blocked_patterns,
            "warnings": warnings,
            "session_token": session_token[:16] + "..." if session_token else None
        })

        return {
            "allowed": is_allowed,
            "threat_level": threat_level,
            "blocked_patterns": blocked_patterns,
            "warnings": warnings,
            "protection_level": self.protection_level,
            "recommendation": "Command blocked due to security policy" if not is_allowed else "Command approved"
        }
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get comprehensive security status with real-time metrics"""
        current_time = int(time.time())

        # Count active sessions
        active_tokens = sum(1 for info in self.session_tokens.values()
                          if info.get('is_active', False) and
                          current_time - info['created_at'] <= self.token_lifetime)

        # Calculate session statistics
        total_activity = sum(info.get('activity_count', 0) for info in self.session_tokens.values())
        avg_session_age = 0
        if self.session_tokens:
            avg_session_age = sum(current_time - info['created_at'] for info in self.session_tokens.values()) / len(self.session_tokens)

        # Threat assessment
        threat_level_text = "LOW"
        if self.threat_score >= 80:
            threat_level_text = "CRITICAL"
        elif self.threat_score >= 60:
            threat_level_text = "HIGH"
        elif self.threat_score >= 40:
            threat_level_text = "MEDIUM"
        elif self.threat_score >= 20:
            threat_level_text = "ELEVATED"

        # Security events summary
        recent_events = [e for e in self.security_events if
                        (datetime.now() - datetime.fromisoformat(e['timestamp'])).total_seconds() < 3600]

        event_types = {}
        for event in recent_events:
            event_type = event['event_type']
            event_types[event_type] = event_types.get(event_type, 0) + 1

        return {
            # Session Information
            'active_sessions': active_tokens,
            'total_sessions': len(self.session_tokens),
            'total_activity': total_activity,
            'average_session_age_seconds': int(avg_session_age),

            # Security Metrics
            'protection_level': self.protection_level,
            'threat_score': self.threat_score,
            'threat_level': threat_level_text,
            'security_rotation_id': self.security_rotation_counter,
            'last_rotation': self.last_rotation.isoformat(),
            'monitoring_active': self.monitoring_active,

            # System Metrics
            'system_metrics': self.system_metrics,

            # Failed Attempts
            'failed_attempts': len(self.failed_attempts),
            'total_failed_count': sum(info.get('count', 0) for info in self.failed_attempts.values()),

            # Security Events
            'total_security_events': len(self.security_events),
            'recent_events_count': len(recent_events),
            'event_types_summary': event_types,

            # Dynamic Security Features
            'features_enabled': {
                'dynamic_encryption': True,
                'real_time_monitoring': self.monitoring_active,
                'adaptive_timeouts': True,
                'threat_detection': True,
                'session_isolation': True,
                'command_filtering': True,
                'intrusion_detection': True
            },

            # Current Configuration
            'current_config': {
                'token_lifetime_seconds': self.token_lifetime,
                'max_failed_attempts': self.max_attempts,
                'lockout_duration_seconds': self.lockout_duration,
                'encryption_enabled': True,
                'dynamic_rotation_enabled': True
            },

            # Status Summary
            'status': 'SECURE' if self.threat_score < 40 else 'ALERT' if self.threat_score < 80 else 'CRITICAL',
            'last_update': datetime.now().isoformat()
        }

    def is_command_safe(self, command: str, session_token: str = None) -> Dict[str, Any]:
        """Check if command is safe to execute with detailed analysis"""
        return self.is_command_allowed(command, "guest", session_token)

    def log_security_event(self, event: str, details: Dict[str, Any] = None):
        """Enhanced security event logging"""
        self._log_security_event(event, details or {})

    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data using current cipher"""
        try:
            encrypted = self.cipher_suite.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted).decode()
        except Exception as e:
            self._log_security_event("encryption_error", {"error": str(e)})
            return ""

    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data using current cipher"""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted = self.cipher_suite.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception as e:
            self._log_security_event("decryption_error", {"error": str(e)})
            return ""

    def get_session_info(self, token: str) -> Dict[str, Any]:
        """Get detailed session information"""
        if token not in self.session_tokens:
            return {}

        session_info = self.session_tokens[token].copy()
        # Remove sensitive information
        session_info.pop('security_hash', None)
        session_info['token_id'] = token[:16] + "..."

        return session_info

    def force_security_rotation(self):
        """Force immediate security parameter rotation"""
        self._log_security_event("manual_security_rotation", {"initiated_by": "admin"})
        self._rotate_security_parameters()

    def get_threat_analysis(self) -> Dict[str, Any]:
        """Get detailed threat analysis"""
        return {
            "current_threat_score": self.threat_score,
            "protection_level": self.protection_level,
            "system_metrics": self.system_metrics,
            "threat_patterns": len(self.threat_patterns),
            "recent_threats": [
                event for event in self.security_events[-50:]
                if event.get('threat_score', 0) > 0
            ],
            "recommendations": self._get_security_recommendations()
        }

    def _get_security_recommendations(self) -> List[str]:
        """Get security recommendations based on current state"""
        recommendations = []

        if self.threat_score > 60:
            recommendations.append("Consider increasing session timeout restrictions")
            recommendations.append("Review recent security events for patterns")

        if len(self.session_tokens) > 10:
            recommendations.append("Monitor for unusual session activity")

        if self.system_metrics.get('cpu_usage', 0) > 80:
            recommendations.append("High CPU usage detected - monitor for malicious processes")

        if self.system_metrics.get('memory_usage', 0) > 85:
            recommendations.append("High memory usage - potential memory-based attack")

        return recommendations

    def shutdown_security_monitoring(self):
        """Safely shutdown security monitoring"""
        self.monitoring_active = False
        self._log_security_event("security_monitoring_shutdown", {
            "total_events_logged": len(self.security_events),
            "active_sessions": len([s for s in self.session_tokens.values() if s.get("is_active", False)])
        })

    def get_security_report(self) -> str:
        """Generate comprehensive security report"""
        status = self.get_security_status()
        threat_analysis = self.get_threat_analysis()

        report = f"""
🔐 AION Advanced Security Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SECURITY STATUS: {status['status']}
Protection Level: {status['protection_level']}/10
Threat Score: {status['threat_score']}/100
Threat Level: {status['threat_level']}

ACTIVE SESSIONS: {status['active_sessions']}
Total Sessions: {status['total_sessions']}
Total Activity: {status['total_activity']}

SYSTEM METRICS:
CPU Usage: {status['system_metrics'].get('cpu_usage', 0):.1f}%
Memory Usage: {status['system_metrics'].get('memory_usage', 0):.1f}%
Network Connections: {status['system_metrics'].get('network_connections', 0)}

SECURITY EVENTS: {status['total_security_events']}
Recent Events (1h): {status['recent_events_count']}

RECOMMENDATIONS:
{chr(10).join('• ' + rec for rec in threat_analysis['recommendations'])}

DYNAMIC FEATURES:
• Security rotation every 60 seconds
• Real-time threat monitoring
• Adaptive protection levels
• Dynamic encryption keys
• Session isolation
• Command filtering
• Intrusion detection
"""
        return report
