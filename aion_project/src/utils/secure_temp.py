#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔒 Secure Temporary File Wrapper
Provides secure temporary file operations for AION
"""

import tempfile
import os
import atexit
from pathlib import Path
from typing import Optional, List

class SecureTempManager:
    """Secure temporary file manager with automatic cleanup"""
    
    def __init__(self):
        self.temp_files: List[Path] = []
        self.temp_dirs: List[Path] = []
        # Register cleanup on exit
        atexit.register(self.cleanup_all)
    
    def create_temp_file(self, suffix: str = "", prefix: str = "aion_", 
                        content: str = "", encoding: str = "utf-8") -> Path:
        """Create a secure temporary file with automatic cleanup"""
        try:
            # Create secure temporary file
            fd, temp_path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
            temp_file = Path(temp_path)
            
            # Write content if provided
            if content:
                with os.fdopen(fd, 'w', encoding=encoding) as f:
                    f.write(content)
            else:
                os.close(fd)
            
            # Set secure permissions (owner read/write only)
            os.chmod(temp_path, 0o600)
            
            # Track for cleanup
            self.temp_files.append(temp_file)
            
            return temp_file
            
        except Exception as e:
            raise RuntimeError(f"Failed to create secure temp file: {e}")
    
    def create_temp_dir(self, prefix: str = "aion_") -> Path:
        """Create a secure temporary directory with automatic cleanup"""
        try:
            temp_dir = Path(tempfile.mkdtemp(prefix=prefix))
            
            # Set secure permissions (owner access only)
            os.chmod(temp_dir, 0o700)
            
            # Track for cleanup
            self.temp_dirs.append(temp_dir)
            
            return temp_dir
            
        except Exception as e:
            raise RuntimeError(f"Failed to create secure temp directory: {e}")
    
    def cleanup_file(self, file_path: Path) -> bool:
        """Securely delete a specific temporary file"""
        try:
            if file_path.exists():
                # Overwrite with random data before deletion (basic secure delete)
                if file_path.is_file():
                    file_size = file_path.stat().st_size
                    with open(file_path, 'wb') as f:
                        f.write(os.urandom(file_size))
                
                file_path.unlink()
                
                if file_path in self.temp_files:
                    self.temp_files.remove(file_path)
                
                return True
                
        except Exception:
            return False
        
        return False
    
    def cleanup_all(self):
        """Clean up all tracked temporary files and directories"""
        # Clean up files
        for temp_file in self.temp_files.copy():
            self.cleanup_file(temp_file)
        
        # Clean up directories
        for temp_dir in self.temp_dirs.copy():
            try:
                if temp_dir.exists():
                    # Remove all files in directory first
                    for file_path in temp_dir.rglob("*"):
                        if file_path.is_file():
                            file_path.unlink()
                    
                    # Remove directory
                    temp_dir.rmdir()
                    
                self.temp_dirs.remove(temp_dir)
                
            except Exception:
                pass

# Global secure temp manager instance
secure_temp = SecureTempManager()
