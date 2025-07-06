#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ AION Input Validation Utilities
Secure input validation and sanitization
"""

import re
import os
from pathlib import Path
from typing import Any, Optional, List

class InputValidator:
    """Secure input validation for AION"""
    
    @staticmethod
    def validate_code_input(code: str, max_length: int = 10000) -> str:
        """Validate and sanitize code input"""
        if not isinstance(code, str):
            raise ValueError("Code input must be a string")
        
        if len(code) > max_length:
            raise ValueError(f"Code input too long (max {max_length} characters)")
        
        # Remove null bytes and other dangerous characters
        code = code.replace('\x00', '').replace('\0', '')
        
        return code
    
    @staticmethod
    def validate_filename(filename: str) -> str:
        """Validate and sanitize filename"""
        if not isinstance(filename, str):
            raise ValueError("Filename must be a string")
        
        # Remove path traversal attempts
        filename = os.path.basename(filename)
        
        # Remove dangerous characters
        dangerous_chars = ['<', '>', ':', '"', '|', '?', '*', '\x00']
        for char in dangerous_chars:
            filename = filename.replace(char, '_')
        
        # Ensure filename is not empty
        if not filename or filename in ['.', '..']:
            filename = 'safe_file'
        
        return filename
    
    @staticmethod
    def validate_path(path: str, allowed_base: Optional[str] = None) -> Path:
        """Validate and resolve path safely"""
        if not isinstance(path, str):
            raise ValueError("Path must be a string")
        
        # Convert to Path object and resolve
        path_obj = Path(path).resolve()
        
        # Check if path is within allowed base directory
        if allowed_base:
            base_path = Path(allowed_base).resolve()
            try:
                path_obj.relative_to(base_path)
            except ValueError:
                raise ValueError(f"Path outside allowed directory: {path}")
        
        return path_obj
    
    @staticmethod
    def sanitize_command_args(args: List[str]) -> List[str]:
        """Sanitize command line arguments"""
        if not isinstance(args, list):
            raise ValueError("Arguments must be a list")
        
        sanitized = []
        for arg in args:
            if not isinstance(arg, str):
                continue
            
            # Remove null bytes and control characters
            arg = ''.join(char for char in arg if ord(char) >= 32 or char in ['\t', '\n'])
            
            # Basic shell injection prevention
            dangerous_patterns = [';', '&&', '||', '|', '`', '$', '>', '<']
            if any(pattern in arg for pattern in dangerous_patterns):
                raise ValueError(f"Dangerous pattern in argument: {arg}")
            
            sanitized.append(arg)
        
        return sanitized
    
    @staticmethod
    def validate_json_config(config: dict) -> dict:
        """Validate JSON configuration"""
        if not isinstance(config, dict):
            raise ValueError("Configuration must be a dictionary")
        
        # Check for dangerous keys
        dangerous_keys = ['__proto__', 'constructor', 'prototype']
        
        def check_recursive(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key in dangerous_keys:
                        raise ValueError(f"Dangerous key found: {path}.{key}")
                    check_recursive(value, f"{path}.{key}")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    check_recursive(item, f"{path}[{i}]")
        
        check_recursive(config)
        return config

# Global validator instance
validator = InputValidator()
