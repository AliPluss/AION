#!/usr/bin/env python3
"""
🔐 AION OTP (One-Time Password) Manager
Advanced two-factor authentication system

This module provides:
- TOTP (Time-based One-Time Password) generation and verification
- QR code generation for authenticator apps
- Backup codes for account recovery
- Session-based OTP verification
- Integration with AION security system
"""

import os
import time
import hmac
import hashlib
import base64
import secrets
import qrcode
from io import BytesIO
from typing import List, Optional, Tuple, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

@dataclass
class OTPConfig:
    """OTP configuration settings"""
    secret_key: str
    issuer: str = "AION"
    account_name: str = "user@aion"
    digits: int = 6
    period: int = 30
    algorithm: str = "SHA1"

class OTPManager:
    """One-Time Password manager for enhanced security"""
    
    def __init__(self, config_file: str = "aion_otp_config.json"):
        self.config_file = config_file
        self.otp_config: Optional[OTPConfig] = None
        self.backup_codes: List[str] = []
        self.used_backup_codes: List[str] = []
        self.verified_sessions: Dict[str, datetime] = {}
        self.session_timeout = timedelta(hours=24)
        
        self.load_config()
        
    def load_config(self):
        """Load OTP configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                self.otp_config = OTPConfig(
                    secret_key=data.get('secret_key', ''),
                    issuer=data.get('issuer', 'AION'),
                    account_name=data.get('account_name', 'user@aion'),
                    digits=data.get('digits', 6),
                    period=data.get('period', 30),
                    algorithm=data.get('algorithm', 'SHA1')
                )
                
                self.backup_codes = data.get('backup_codes', [])
                self.used_backup_codes = data.get('used_backup_codes', [])
                
        except Exception as e:
            print(f"⚠️ Warning: Could not load OTP config: {e}")
            
    def save_config(self):
        """Save OTP configuration to file"""
        try:
            if not self.otp_config:
                return
                
            data = {
                'secret_key': self.otp_config.secret_key,
                'issuer': self.otp_config.issuer,
                'account_name': self.otp_config.account_name,
                'digits': self.otp_config.digits,
                'period': self.otp_config.period,
                'algorithm': self.otp_config.algorithm,
                'backup_codes': self.backup_codes,
                'used_backup_codes': self.used_backup_codes
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"❌ Error saving OTP config: {e}")
            
    def setup_otp(self, account_name: str = "user@aion") -> Tuple[str, List[str]]:
        """Setup OTP for the first time"""
        # Generate secret key
        secret_key = base64.b32encode(secrets.token_bytes(20)).decode('utf-8')
        
        # Create OTP configuration
        self.otp_config = OTPConfig(
            secret_key=secret_key,
            account_name=account_name
        )
        
        # Generate backup codes
        self.backup_codes = [self._generate_backup_code() for _ in range(10)]
        self.used_backup_codes = []
        
        # Save configuration
        self.save_config()
        
        print("🔐 OTP setup completed successfully!")
        print(f"📱 Secret Key: {secret_key}")
        print("💾 Backup codes generated")
        
        return secret_key, self.backup_codes.copy()
        
    def _generate_backup_code(self) -> str:
        """Generate a backup recovery code"""
        return '-'.join([
            secrets.token_hex(2).upper() for _ in range(4)
        ])
        
    def generate_qr_code(self) -> Optional[str]:
        """Generate QR code for authenticator app setup"""
        if not self.otp_config:
            print("❌ OTP not configured. Run setup_otp() first.")
            return None
            
        try:
            # Create TOTP URI
            uri = (
                f"otpauth://totp/{self.otp_config.issuer}:{self.otp_config.account_name}"
                f"?secret={self.otp_config.secret_key}"
                f"&issuer={self.otp_config.issuer}"
                f"&digits={self.otp_config.digits}"
                f"&period={self.otp_config.period}"
                f"&algorithm={self.otp_config.algorithm}"
            )
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(uri)
            qr.make(fit=True)
            
            # Create ASCII QR code for terminal display
            qr_ascii = qr.get_matrix()
            qr_string = ""
            for row in qr_ascii:
                qr_string += "".join("██" if cell else "  " for cell in row) + "\n"
                
            return qr_string
            
        except Exception as e:
            print(f"❌ Error generating QR code: {e}")
            return None
            
    def generate_totp(self, timestamp: Optional[int] = None) -> str:
        """Generate TOTP code for current time"""
        if not self.otp_config:
            raise ValueError("OTP not configured")
            
        if timestamp is None:
            timestamp = int(time.time())
            
        # Calculate time counter
        counter = timestamp // self.otp_config.period
        
        # Convert counter to bytes
        counter_bytes = counter.to_bytes(8, byteorder='big')
        
        # Decode secret key
        secret_bytes = base64.b32decode(self.otp_config.secret_key)
        
        # Generate HMAC
        if self.otp_config.algorithm == "SHA1":
            hash_func = hashlib.sha1
        elif self.otp_config.algorithm == "SHA256":
            hash_func = hashlib.sha256
        elif self.otp_config.algorithm == "SHA512":
            hash_func = hashlib.sha512
        else:
            hash_func = hashlib.sha1
            
        hmac_hash = hmac.new(secret_bytes, counter_bytes, hash_func).digest()
        
        # Dynamic truncation
        offset = hmac_hash[-1] & 0x0F
        truncated = hmac_hash[offset:offset + 4]
        code = int.from_bytes(truncated, byteorder='big') & 0x7FFFFFFF
        
        # Generate final code
        totp_code = str(code % (10 ** self.otp_config.digits)).zfill(self.otp_config.digits)
        
        return totp_code
        
    def verify_totp(self, user_code: str, window: int = 1) -> bool:
        """Verify TOTP code with time window tolerance"""
        if not self.otp_config:
            return False
            
        current_time = int(time.time())
        
        # Check current time and adjacent time windows
        for i in range(-window, window + 1):
            timestamp = current_time + (i * self.otp_config.period)
            expected_code = self.generate_totp(timestamp)
            
            if hmac.compare_digest(user_code, expected_code):
                return True
                
        return False
        
    def verify_backup_code(self, backup_code: str) -> bool:
        """Verify backup recovery code"""
        backup_code = backup_code.upper().strip()
        
        if backup_code in self.used_backup_codes:
            print("❌ Backup code already used")
            return False
            
        if backup_code in self.backup_codes:
            # Mark backup code as used
            self.used_backup_codes.append(backup_code)
            self.backup_codes.remove(backup_code)
            self.save_config()
            
            print("✅ Backup code verified and consumed")
            return True
            
        return False
        
    def verify_otp(self, user_input: str) -> bool:
        """Verify OTP code (TOTP or backup code)"""
        user_input = user_input.strip()
        
        # Check if it's a backup code format (XX-XX-XX-XX)
        if len(user_input.replace('-', '')) == 8 and '-' in user_input:
            return self.verify_backup_code(user_input)
        
        # Check if it's a TOTP code
        if len(user_input) == self.otp_config.digits if self.otp_config else 6:
            return self.verify_totp(user_input)
            
        return False
        
    def create_session(self, session_id: str):
        """Create verified session"""
        self.verified_sessions[session_id] = datetime.now()
        self._cleanup_expired_sessions()
        
    def is_session_verified(self, session_id: str) -> bool:
        """Check if session is verified and not expired"""
        if session_id not in self.verified_sessions:
            return False
            
        session_time = self.verified_sessions[session_id]
        if datetime.now() - session_time > self.session_timeout:
            del self.verified_sessions[session_id]
            return False
            
        return True
        
    def _cleanup_expired_sessions(self):
        """Remove expired sessions"""
        current_time = datetime.now()
        expired_sessions = [
            session_id for session_id, session_time in self.verified_sessions.items()
            if current_time - session_time > self.session_timeout
        ]
        
        for session_id in expired_sessions:
            del self.verified_sessions[session_id]
            
    def get_remaining_backup_codes(self) -> int:
        """Get number of remaining backup codes"""
        return len(self.backup_codes)
        
    def regenerate_backup_codes(self) -> List[str]:
        """Regenerate backup codes"""
        self.backup_codes = [self._generate_backup_code() for _ in range(10)]
        self.used_backup_codes = []
        self.save_config()
        
        print("🔄 Backup codes regenerated")
        return self.backup_codes.copy()
        
    def disable_otp(self) -> bool:
        """Disable OTP authentication"""
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
                
            self.otp_config = None
            self.backup_codes = []
            self.used_backup_codes = []
            self.verified_sessions = {}
            
            print("🔓 OTP authentication disabled")
            return True
            
        except Exception as e:
            print(f"❌ Error disabling OTP: {e}")
            return False
            
    def is_otp_enabled(self) -> bool:
        """Check if OTP is enabled"""
        return self.otp_config is not None
        
    def get_time_remaining(self) -> int:
        """Get seconds remaining for current TOTP code"""
        if not self.otp_config:
            return 0
            
        current_time = int(time.time())
        return self.otp_config.period - (current_time % self.otp_config.period)

# Global OTP manager instance
otp_manager = OTPManager()

def setup_two_factor_auth(account_name: str = "user@aion") -> bool:
    """Command-line interface for OTP setup"""
    try:
        print("🔐 Setting up Two-Factor Authentication for AION")
        print("=" * 50)
        
        # Setup OTP
        secret_key, backup_codes = otp_manager.setup_otp(account_name)
        
        print("\n📱 Scan this QR code with your authenticator app:")
        print("=" * 50)
        qr_code = otp_manager.generate_qr_code()
        if qr_code:
            print(qr_code)
        else:
            print(f"Manual entry - Secret Key: {secret_key}")
            
        print("\n💾 Backup Recovery Codes (save these safely!):")
        print("=" * 50)
        for i, code in enumerate(backup_codes, 1):
            print(f"{i:2d}. {code}")
            
        print("\n✅ Two-Factor Authentication setup complete!")
        print("🔒 AION will now require OTP codes for secure operations")
        
        return True
        
    except Exception as e:
        print(f"❌ Error setting up 2FA: {e}")
        return False

def verify_otp_command(otp_code: str) -> bool:
    """Command-line interface for OTP verification"""
    if not otp_manager.is_otp_enabled():
        print("❌ OTP not enabled. Run setup-2fa command first.")
        return False
        
    if otp_manager.verify_otp(otp_code):
        print("✅ OTP verification successful")
        return True
    else:
        print("❌ Invalid OTP code")
        return False
