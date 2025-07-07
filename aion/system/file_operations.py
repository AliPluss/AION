"""
🗂️ AION File Operations System
Advanced file operations with comprehensive security and monitoring

This module provides professional-grade file operations including:
- Secure file manipulation with path validation
- Comprehensive file information and metadata
- Operation history and audit logging
- Hash calculation and integrity verification
- MIME type detection and file analysis
- Batch operations with progress tracking
- Error handling and recovery mechanisms

All operations include security validation and comprehensive logging
for enterprise-grade file management capabilities.
"""

import os
import shutil
import mimetypes
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass
from datetime import datetime
import json
import logging

# Import common utilities for consistency
try:
    from ..utils.helpers import validate_path_safety, setup_logging, calculate_file_checksum
except ImportError:
    from utils.helpers import validate_path_safety, setup_logging, calculate_file_checksum

@dataclass
class FileInfo:
    """
    Comprehensive file information structure
    
    Contains all relevant metadata about a file or directory:
    - Basic properties (path, name, size, timestamps)
    - Security information (permissions, hashes)
    - Content analysis (MIME type, encoding)
    """
    path: str
    name: str
    size: int
    created: datetime
    modified: datetime
    accessed: datetime
    is_directory: bool
    permissions: str
    mime_type: Optional[str]
    hash_md5: Optional[str]
    hash_sha256: Optional[str]

@dataclass
class OperationResult:
    """
    Standardized operation result structure
    
    Provides consistent return format for all file operations:
    - Success/failure status
    - Human-readable message
    - Operation data (if applicable)
    - Error details (if failed)
    """
    success: bool
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None

class FileOperations:
    """
    Professional File Operations Manager
    
    This class provides comprehensive file system operations with:
    - Security validation for all file paths
    - Comprehensive logging and audit trails
    - Operation history tracking
    - Error handling and recovery
    - Batch operations with progress tracking
    - Hash calculation and integrity verification
    - MIME type detection and analysis
    
    All operations are designed for enterprise use with proper
    security controls and comprehensive error handling.
    """
    
    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize file operations manager
        
        Args:
            base_path: Base directory for operations (defaults to current directory)
        """
        self.base_path = base_path or Path.cwd()
        self.logger = setup_logging(__name__)
        self.operation_history: List[Dict[str, Any]] = []
        
        # Security settings
        self.max_file_size = 100 * 1024 * 1024  # 100MB default limit
        self.allowed_extensions = set()  # Empty means all allowed
        self.blocked_extensions = {'.exe', '.bat', '.cmd', '.scr', '.com'}
        
        self.logger.info(f"FileOperations initialized with base path: {self.base_path}")
    
    def _log_operation(self, operation: str, path: str, success: bool, 
                      details: Optional[str] = None) -> None:
        """
        Log file operation for audit trail
        
        Args:
            operation: Type of operation performed
            path: File/directory path involved
            success: Whether operation succeeded
            details: Additional operation details
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "path": str(path),
            "success": success,
            "details": details
        }
        
        self.operation_history.append(log_entry)
        
        if success:
            self.logger.info(f"Operation {operation} succeeded on {path}")
        else:
            self.logger.error(f"Operation {operation} failed on {path}: {details}")
    
    def _validate_file_security(self, file_path: Path) -> OperationResult:
        """
        Validate file security constraints
        
        Args:
            file_path: Path to validate
            
        Returns:
            OperationResult indicating if file passes security checks
        """
        try:
            # Path safety validation
            if not validate_path_safety(str(file_path)):
                return OperationResult(
                    success=False,
                    message="Path failed security validation",
                    error="Potentially unsafe path detected"
                )
            
            # Extension validation
            if file_path.suffix.lower() in self.blocked_extensions:
                return OperationResult(
                    success=False,
                    message="File extension blocked for security",
                    error=f"Extension {file_path.suffix} is not allowed"
                )
            
            # Size validation (if file exists)
            if file_path.exists() and file_path.is_file():
                if file_path.stat().st_size > self.max_file_size:
                    return OperationResult(
                        success=False,
                        message="File exceeds maximum size limit",
                        error=f"File size {file_path.stat().st_size} exceeds limit {self.max_file_size}"
                    )
            
            return OperationResult(success=True, message="Security validation passed")
            
        except Exception as e:
            return OperationResult(
                success=False,
                message="Security validation failed",
                error=str(e)
            )
    
    def get_file_info(self, file_path: Union[str, Path]) -> OperationResult:
        """
        Get comprehensive file information
        
        Args:
            file_path: Path to file or directory
            
        Returns:
            OperationResult containing FileInfo object
        """
        try:
            path = Path(file_path)
            
            # Security validation
            security_result = self._validate_file_security(path)
            if not security_result.success:
                return security_result
            
            if not path.exists():
                return OperationResult(
                    success=False,
                    message="File or directory does not exist",
                    error=f"Path not found: {path}"
                )
            
            stat = path.stat()
            
            # Calculate hashes for files
            hash_md5 = None
            hash_sha256 = None
            mime_type = None
            
            if path.is_file():
                hash_md5 = calculate_file_checksum(str(path), 'md5')
                hash_sha256 = calculate_file_checksum(str(path), 'sha256')
                mime_type, _ = mimetypes.guess_type(str(path))
            
            file_info = FileInfo(
                path=str(path),
                name=path.name,
                size=stat.st_size,
                created=datetime.fromtimestamp(stat.st_ctime),
                modified=datetime.fromtimestamp(stat.st_mtime),
                accessed=datetime.fromtimestamp(stat.st_atime),
                is_directory=path.is_dir(),
                permissions=oct(stat.st_mode)[-3:],
                mime_type=mime_type,
                hash_md5=hash_md5,
                hash_sha256=hash_sha256
            )
            
            self._log_operation("get_info", str(path), True)
            
            return OperationResult(
                success=True,
                message="File information retrieved successfully",
                data=file_info
            )
            
        except Exception as e:
            self._log_operation("get_info", str(file_path), False, str(e))
            return OperationResult(
                success=False,
                message="Failed to get file information",
                error=str(e)
            )
    
    def create_file(self, file_path: Union[str, Path], content: str = "", 
                   encoding: str = "utf-8") -> OperationResult:
        """
        Create a new file with specified content
        
        Args:
            file_path: Path for new file
            content: File content (default: empty)
            encoding: Text encoding (default: utf-8)
            
        Returns:
            OperationResult indicating success/failure
        """
        try:
            path = Path(file_path)
            
            # Security validation
            security_result = self._validate_file_security(path)
            if not security_result.success:
                return security_result
            
            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(path, 'w', encoding=encoding) as f:
                f.write(content)
            
            self._log_operation("create_file", str(path), True, f"Size: {len(content)} chars")
            
            return OperationResult(
                success=True,
                message=f"File created successfully: {path.name}",
                data={"path": str(path), "size": len(content)}
            )
            
        except Exception as e:
            self._log_operation("create_file", str(file_path), False, str(e))
            return OperationResult(
                success=False,
                message="Failed to create file",
                error=str(e)
            )
