"""
🔧 AION Helper Utilities
Common utility functions for file operations, logging, and validation

This module provides essential helper functions including:
- File operations with security validation
- Comprehensive logging setup and management
- Path safety validation and sanitization
- Dependency checking and validation
- System resource monitoring
- Cross-platform compatibility utilities
- Performance optimization helpers
"""

import os
import sys
import hashlib
import logging
import platform
import subprocess
import importlib.util
from pathlib import Path
from typing import Optional, List, Dict, Any, Union, Tuple
from datetime import datetime

def calculate_file_checksum(file_path: Union[str, Path], algorithm: str = "sha256") -> Optional[str]:
    """
    Calculate file checksum using specified algorithm
    
    Args:
        file_path: Path to the file
        algorithm: Hash algorithm (md5, sha1, sha256, sha512)
    
    Returns:
        Hexadecimal checksum string or None if error
    """
    try:
        file_path = Path(file_path)
        
        if not file_path.exists() or not file_path.is_file():
            return None
        
        # Get hash algorithm
        hash_algorithms = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha256': hashlib.sha256,
            'sha512': hashlib.sha512
        }
        
        if algorithm.lower() not in hash_algorithms:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        hash_func = hash_algorithms[algorithm.lower()]()
        
        # Read file in chunks to handle large files
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
        
    except Exception as e:
        logging.error(f"Error calculating checksum for {file_path}: {e}")
        return None

def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[Union[str, Path]] = None,
    log_format: Optional[str] = None,
    include_console: bool = True
) -> logging.Logger:
    """
    Setup comprehensive logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path
        log_format: Custom log format string
        include_console: Whether to include console output
    
    Returns:
        Configured logger instance
    """
    try:
        # Default log format
        if log_format is None:
            log_format = (
                "%(asctime)s - %(name)s - %(levelname)s - "
                "%(filename)s:%(lineno)d - %(message)s"
            )
        
        # Configure root logger
        logger = logging.getLogger("aion")
        logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(log_format)
        
        # Console handler
        if include_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        # File handler
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        logger.info(f"Logging initialized - Level: {log_level}")
        return logger
        
    except Exception as e:
        print(f"Error setting up logging: {e}")
        return logging.getLogger("aion")

def validate_path_safety(path: Union[str, Path], base_path: Optional[Union[str, Path]] = None) -> Tuple[bool, str]:
    """
    Validate path for security and safety
    
    Args:
        path: Path to validate
        base_path: Optional base path for relative path validation
    
    Returns:
        Tuple of (is_safe, reason)
    """
    try:
        path = Path(path).resolve()
        
        # Check for path traversal attempts
        path_str = str(path)
        dangerous_patterns = [
            "..", "~", "$", "`", "|", "&", ";",
            "\\x", "%", "<", ">", "\"", "'", "*", "?"
        ]
        
        for pattern in dangerous_patterns:
            if pattern in path_str:
                return False, f"Dangerous pattern detected: {pattern}"
        
        # Check if path is within base path (if provided)
        if base_path:
            base_path = Path(base_path).resolve()
            try:
                path.relative_to(base_path)
            except ValueError:
                return False, "Path is outside allowed base directory"
        
        # Check for system directories (basic protection)
        system_dirs = [
            "/etc", "/sys", "/proc", "/dev", "/boot",
            "C:\\Windows", "C:\\System32", "C:\\Program Files"
        ]
        
        for sys_dir in system_dirs:
            if path_str.startswith(sys_dir):
                return False, f"Access to system directory not allowed: {sys_dir}"
        
        return True, "Path is safe"
        
    except Exception as e:
        return False, f"Path validation error: {e}"

def check_dependencies(dependencies: List[str]) -> Dict[str, Dict[str, Any]]:
    """
    Check if required dependencies are available
    
    Args:
        dependencies: List of package names to check
    
    Returns:
        Dictionary with dependency status information
    """
    results = {}
    
    for dep in dependencies:
        try:
            # Try to import the module
            spec = importlib.util.find_spec(dep)
            
            if spec is None:
                results[dep] = {
                    "available": False,
                    "version": None,
                    "location": None,
                    "error": "Module not found"
                }
                continue
            
            # Import and get version if possible
            module = importlib.import_module(dep)
            version = getattr(module, '__version__', 'Unknown')
            location = getattr(spec, 'origin', 'Unknown')
            
            results[dep] = {
                "available": True,
                "version": version,
                "location": location,
                "error": None
            }
            
        except Exception as e:
            results[dep] = {
                "available": False,
                "version": None,
                "location": None,
                "error": str(e)
            }
    
    return results

def get_system_info() -> Dict[str, Any]:
    """Get comprehensive system information"""
    try:
        return {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "architecture": platform.architecture(),
            "hostname": platform.node(),
            "current_directory": str(Path.cwd()),
            "home_directory": str(Path.home()),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": f"Failed to get system info: {e}"}

def ensure_directory(path: Union[str, Path]) -> bool:
    """
    Ensure directory exists, create if necessary
    
    Args:
        path: Directory path to ensure
    
    Returns:
        True if directory exists or was created successfully
    """
    try:
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logging.error(f"Failed to create directory {path}: {e}")
        return False

def safe_file_read(file_path: Union[str, Path], encoding: str = 'utf-8') -> Optional[str]:
    """
    Safely read file content with error handling
    
    Args:
        file_path: Path to file
        encoding: File encoding
    
    Returns:
        File content or None if error
    """
    try:
        file_path = Path(file_path)
        
        if not file_path.exists():
            return None
        
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
            
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return None

def safe_file_write(file_path: Union[str, Path], content: str, encoding: str = 'utf-8') -> bool:
    """
    Safely write content to file with error handling
    
    Args:
        file_path: Path to file
        content: Content to write
        encoding: File encoding
    
    Returns:
        True if successful, False otherwise
    """
    try:
        file_path = Path(file_path)
        
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        logging.error(f"Error writing file {file_path}: {e}")
        return False

def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def is_command_available(command: str) -> bool:
    """Check if a command is available in the system PATH"""
    try:
        subprocess.run(
            [command, "--version"],
            capture_output=True,
            check=True,
            timeout=5
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for cross-platform compatibility"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
    
    # Ensure not empty
    if not filename:
        filename = "unnamed_file"
    
    return filename

def get_file_info(file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
    """Get comprehensive file information"""
    try:
        file_path = Path(file_path)
        
        if not file_path.exists():
            return None
        
        stat = file_path.stat()
        
        return {
            "name": file_path.name,
            "path": str(file_path.absolute()),
            "size": stat.st_size,
            "size_formatted": format_file_size(stat.st_size),
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
            "is_file": file_path.is_file(),
            "is_directory": file_path.is_dir(),
            "is_symlink": file_path.is_symlink(),
            "permissions": oct(stat.st_mode)[-3:],
            "checksum_sha256": calculate_file_checksum(file_path, "sha256") if file_path.is_file() else None
        }
        
    except Exception as e:
        logging.error(f"Error getting file info for {file_path}: {e}")
        return None
