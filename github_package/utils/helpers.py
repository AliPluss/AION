#!/usr/bin/env python3
"""
🛠️ AION Helper Utilities
Common utility functions for AION
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List


def create_directories(base_path: str = ".") -> bool:
    """Create necessary directories for AION"""
    try:
        base = Path(base_path)
        
        # Create main directories
        directories = [
            base / "config",
            base / "logs",
            base / "plugins",
            base / "temp",
            base / "data",
            base / "locales",
            base / "templates",
            base / "static",
            base / "uploads"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating directories: {e}")
        return False


def load_config(config_path: str, default_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Load configuration from JSON file"""
    try:
        config_file = Path(config_path)
        
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"✅ Loaded config from: {config_path}")
            return config
        else:
            if default_config:
                save_config(config_path, default_config)
                print(f"✅ Created default config: {config_path}")
                return default_config
            else:
                print(f"⚠️  Config file not found: {config_path}")
                return {}
                
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return default_config or {}


def save_config(config_path: str, config: Dict[str, Any]) -> bool:
    """Save configuration to JSON file"""
    try:
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved config to: {config_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving config: {e}")
        return False


def get_user_config_dir() -> Path:
    """Get user-specific configuration directory"""
    home = Path.home()
    
    # Platform-specific config directories
    if os.name == 'nt':  # Windows
        config_dir = home / "AppData" / "Local" / "AION"
    else:  # Unix-like systems
        config_dir = home / ".config" / "aion"
    
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def copy_template_configs():
    """Copy template configurations to user config directory"""
    try:
        user_config_dir = get_user_config_dir()
        template_dir = Path("config")
        
        if not template_dir.exists():
            print("⚠️  Template config directory not found")
            return False
        
        # Copy template files
        templates = [
            "ai_config_template.json",
            "security_config_template.json"
        ]
        
        for template in templates:
            template_path = template_dir / template
            if template_path.exists():
                # Remove '_template' from filename
                target_name = template.replace('_template', '')
                target_path = user_config_dir / target_name
                
                if not target_path.exists():
                    shutil.copy2(template_path, target_path)
                    print(f"✅ Copied {template} to {target_path}")
                else:
                    print(f"ℹ️  Config already exists: {target_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error copying template configs: {e}")
        return False


def validate_config(config: Dict[str, Any], required_keys: List[str]) -> bool:
    """Validate configuration has required keys"""
    missing_keys = []
    
    for key in required_keys:
        if key not in config:
            missing_keys.append(key)
    
    if missing_keys:
        print(f"❌ Missing required config keys: {missing_keys}")
        return False
    
    return True


def get_system_info() -> Dict[str, Any]:
    """Get system information"""
    import platform
    import sys
    
    return {
        "platform": platform.platform(),
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": sys.version,
        "python_executable": sys.executable
    }


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def clean_temp_files(temp_dir: str = "temp") -> bool:
    """Clean temporary files"""
    try:
        temp_path = Path(temp_dir)
        
        if temp_path.exists():
            for file_path in temp_path.glob("*"):
                if file_path.is_file():
                    file_path.unlink()
                    print(f"🗑️  Deleted temp file: {file_path}")
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
                    print(f"🗑️  Deleted temp directory: {file_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error cleaning temp files: {e}")
        return False


def backup_config(config_path: str, backup_dir: str = "backups") -> bool:
    """Create backup of configuration file"""
    try:
        config_file = Path(config_path)
        
        if not config_file.exists():
            print(f"⚠️  Config file not found: {config_path}")
            return False
        
        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # Create backup with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_path / f"{config_file.stem}_{timestamp}{config_file.suffix}"
        
        shutil.copy2(config_file, backup_file)
        print(f"✅ Created backup: {backup_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return False


def check_dependencies() -> Dict[str, bool]:
    """Check if required dependencies are installed"""
    required_packages = [
        "typer", "rich", "textual", "fastapi", "uvicorn", 
        "httpx", "jinja2", "python_multipart", "openai",
        "requests", "pydantic", "colorama", "click",
        "aiofiles", "cryptography"
    ]
    
    results = {}
    
    for package in required_packages:
        try:
            # Handle special case for python-multipart
            if package == "python_multipart":
                import python_multipart
            else:
                __import__(package)
            results[package] = True
        except ImportError:
            results[package] = False
    
    return results


def setup_logging(log_dir: str = "logs", log_level: str = "INFO") -> bool:
    """Setup logging configuration"""
    try:
        import logging
        from datetime import datetime
        
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = log_path / f"aion_{timestamp}.log"
        
        # Configure logging
        logging.basicConfig(
            level=getattr(logging, log_level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        print(f"✅ Logging setup complete: {log_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up logging: {e}")
        return False
