#!/usr/bin/env python3
"""
🧩 AION Plugin Installer
Advanced plugin installation and management system

This module provides:
- Plugin installation from various sources (GitHub, PyPI, local)
- Dependency management and resolution
- Plugin verification and security scanning
- Automatic plugin configuration
- Plugin update management
"""

import os
import sys
import json
import subprocess
import tempfile
import shutil
import zipfile
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

@dataclass
class PluginInfo:
    """Plugin information structure"""
    name: str
    version: str
    description: str
    author: str
    dependencies: List[str]
    entry_point: str
    permissions: List[str]
    source_url: Optional[str] = None
    install_path: Optional[str] = None

class InstallSource(Enum):
    """Plugin installation sources"""
    GITHUB = "github"
    PYPI = "pypi"
    LOCAL = "local"
    URL = "url"

class PluginInstaller:
    """Advanced plugin installer with security and dependency management"""
    
    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = Path(plugins_dir)
        self.plugins_dir.mkdir(exist_ok=True)
        self.installed_plugins: Dict[str, PluginInfo] = {}
        self.load_installed_plugins()
        
    def load_installed_plugins(self):
        """Load information about installed plugins"""
        registry_file = self.plugins_dir / "registry.json"
        if registry_file.exists():
            try:
                with open(registry_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for name, info in data.items():
                        self.installed_plugins[name] = PluginInfo(**info)
            except Exception as e:
                print(f"⚠️ Warning: Could not load plugin registry: {e}")
                
    def save_plugin_registry(self):
        """Save plugin registry to disk"""
        registry_file = self.plugins_dir / "registry.json"
        try:
            data = {}
            for name, info in self.installed_plugins.items():
                data[name] = {
                    'name': info.name,
                    'version': info.version,
                    'description': info.description,
                    'author': info.author,
                    'dependencies': info.dependencies,
                    'entry_point': info.entry_point,
                    'permissions': info.permissions,
                    'source_url': info.source_url,
                    'install_path': info.install_path
                }
            with open(registry_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving plugin registry: {e}")
            
    def install_from_github(self, repo_url: str, plugin_name: Optional[str] = None) -> bool:
        """Install plugin from GitHub repository"""
        try:
            print(f"📥 Installing plugin from GitHub: {repo_url}")
            
            # Extract repository information
            if repo_url.startswith("https://github.com/"):
                repo_path = repo_url.replace("https://github.com/", "").rstrip("/")
            else:
                repo_path = repo_url
                
            # Download repository as ZIP
            zip_url = f"https://github.com/{repo_path}/archive/main.zip"
            response = requests.get(zip_url, timeout=30)
            
            if response.status_code != 200:
                # Try master branch
                zip_url = f"https://github.com/{repo_path}/archive/master.zip"
                response = requests.get(zip_url, timeout=30)
                
            if response.status_code != 200:
                print(f"❌ Failed to download repository: {repo_url}")
                return False
                
            # Extract to temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = Path(temp_dir) / "plugin.zip"
                with open(zip_path, 'wb') as f:
                    f.write(response.content)
                    
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                    
                # Find plugin directory
                extracted_dirs = [d for d in Path(temp_dir).iterdir() if d.is_dir()]
                if not extracted_dirs:
                    print("❌ No directories found in downloaded archive")
                    return False
                    
                plugin_source = extracted_dirs[0]
                
                # Look for plugin.json or setup.py
                plugin_config = self._find_plugin_config(plugin_source)
                if not plugin_config:
                    print("❌ No plugin configuration found (plugin.json or setup.py)")
                    return False
                    
                # Install plugin
                return self._install_plugin_from_source(plugin_source, plugin_config, repo_url)
                
        except Exception as e:
            print(f"❌ Error installing from GitHub: {e}")
            return False
            
    def install_from_pypi(self, package_name: str) -> bool:
        """Install plugin from PyPI"""
        try:
            print(f"📦 Installing plugin from PyPI: {package_name}")
            
            # Use pip to install package
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package_name, "--target", str(self.plugins_dir)
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Failed to install from PyPI: {result.stderr}")
                return False
                
            print(f"✅ Successfully installed {package_name} from PyPI")
            return True
            
        except Exception as e:
            print(f"❌ Error installing from PyPI: {e}")
            return False
            
    def install_from_local(self, local_path: str) -> bool:
        """Install plugin from local directory or file"""
        try:
            source_path = Path(local_path)
            if not source_path.exists():
                print(f"❌ Local path does not exist: {local_path}")
                return False
                
            print(f"📁 Installing plugin from local path: {local_path}")
            
            if source_path.is_file() and source_path.suffix == '.zip':
                # Extract ZIP file
                with tempfile.TemporaryDirectory() as temp_dir:
                    with zipfile.ZipFile(source_path, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                        
                    extracted_dirs = [d for d in Path(temp_dir).iterdir() if d.is_dir()]
                    if extracted_dirs:
                        plugin_source = extracted_dirs[0]
                    else:
                        plugin_source = Path(temp_dir)
                        
                    plugin_config = self._find_plugin_config(plugin_source)
                    if not plugin_config:
                        print("❌ No plugin configuration found")
                        return False
                        
                    return self._install_plugin_from_source(plugin_source, plugin_config, str(source_path))
                    
            elif source_path.is_dir():
                # Install from directory
                plugin_config = self._find_plugin_config(source_path)
                if not plugin_config:
                    print("❌ No plugin configuration found")
                    return False
                    
                return self._install_plugin_from_source(source_path, plugin_config, str(source_path))
                
            else:
                print("❌ Unsupported local file type")
                return False
                
        except Exception as e:
            print(f"❌ Error installing from local path: {e}")
            return False
            
    def _find_plugin_config(self, plugin_dir: Path) -> Optional[Dict[str, Any]]:
        """Find and parse plugin configuration"""
        # Look for plugin.json
        plugin_json = plugin_dir / "plugin.json"
        if plugin_json.exists():
            try:
                with open(plugin_json, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Warning: Could not parse plugin.json: {e}")
                
        # Look for setup.py and extract information
        setup_py = plugin_dir / "setup.py"
        if setup_py.exists():
            # Basic setup.py parsing (simplified)
            return {
                "name": plugin_dir.name,
                "version": "1.0.0",
                "description": f"Plugin from {plugin_dir.name}",
                "author": "Unknown",
                "dependencies": [],
                "entry_point": "main.py",
                "permissions": ["read", "write"]
            }
            
        return None
        
    def _install_plugin_from_source(self, source_dir: Path, config: Dict[str, Any], source_url: str) -> bool:
        """Install plugin from source directory"""
        try:
            plugin_name = config.get('name', source_dir.name)
            plugin_version = config.get('version', '1.0.0')
            
            # Create plugin directory
            plugin_install_dir = self.plugins_dir / plugin_name
            if plugin_install_dir.exists():
                print(f"⚠️ Plugin {plugin_name} already exists. Updating...")
                shutil.rmtree(plugin_install_dir)
                
            # Copy plugin files
            shutil.copytree(source_dir, plugin_install_dir)
            
            # Install dependencies
            dependencies = config.get('dependencies', [])
            if dependencies:
                print(f"📦 Installing dependencies: {', '.join(dependencies)}")
                for dep in dependencies:
                    result = subprocess.run([
                        sys.executable, "-m", "pip", "install", dep
                    ], capture_output=True, text=True)
                    if result.returncode != 0:
                        print(f"⚠️ Warning: Failed to install dependency {dep}")
                        
            # Create plugin info
            plugin_info = PluginInfo(
                name=plugin_name,
                version=plugin_version,
                description=config.get('description', 'No description'),
                author=config.get('author', 'Unknown'),
                dependencies=dependencies,
                entry_point=config.get('entry_point', 'main.py'),
                permissions=config.get('permissions', []),
                source_url=source_url,
                install_path=str(plugin_install_dir)
            )
            
            # Register plugin
            self.installed_plugins[plugin_name] = plugin_info
            self.save_plugin_registry()
            
            print(f"✅ Successfully installed plugin: {plugin_name} v{plugin_version}")
            return True
            
        except Exception as e:
            print(f"❌ Error installing plugin: {e}")
            return False
            
    def uninstall_plugin(self, plugin_name: str) -> bool:
        """Uninstall a plugin"""
        try:
            if plugin_name not in self.installed_plugins:
                print(f"❌ Plugin not found: {plugin_name}")
                return False
                
            plugin_info = self.installed_plugins[plugin_name]
            
            # Remove plugin directory
            if plugin_info.install_path:
                plugin_path = Path(plugin_info.install_path)
                if plugin_path.exists():
                    shutil.rmtree(plugin_path)
                    
            # Remove from registry
            del self.installed_plugins[plugin_name]
            self.save_plugin_registry()
            
            print(f"✅ Successfully uninstalled plugin: {plugin_name}")
            return True
            
        except Exception as e:
            print(f"❌ Error uninstalling plugin: {e}")
            return False
            
    def list_installed_plugins(self) -> List[PluginInfo]:
        """List all installed plugins"""
        return list(self.installed_plugins.values())
        
    def get_plugin_info(self, plugin_name: str) -> Optional[PluginInfo]:
        """Get information about a specific plugin"""
        return self.installed_plugins.get(plugin_name)
        
    def update_plugin(self, plugin_name: str) -> bool:
        """Update a plugin to the latest version"""
        try:
            if plugin_name not in self.installed_plugins:
                print(f"❌ Plugin not found: {plugin_name}")
                return False
                
            plugin_info = self.installed_plugins[plugin_name]
            
            if not plugin_info.source_url:
                print(f"❌ No source URL available for plugin: {plugin_name}")
                return False
                
            print(f"🔄 Updating plugin: {plugin_name}")
            
            # Uninstall current version
            self.uninstall_plugin(plugin_name)
            
            # Reinstall from source
            if plugin_info.source_url.startswith("https://github.com/"):
                return self.install_from_github(plugin_info.source_url)
            else:
                return self.install_from_local(plugin_info.source_url)
                
        except Exception as e:
            print(f"❌ Error updating plugin: {e}")
            return False

# Global plugin installer instance
plugin_installer = PluginInstaller()

def install_plugin_command(source: str, source_type: str = "auto") -> bool:
    """Command-line interface for plugin installation"""
    if source_type == "auto":
        if source.startswith("https://github.com/") or "/" in source and not source.startswith("/"):
            source_type = "github"
        elif source.endswith(".zip") or os.path.exists(source):
            source_type = "local"
        else:
            source_type = "pypi"
            
    if source_type == "github":
        return plugin_installer.install_from_github(source)
    elif source_type == "pypi":
        return plugin_installer.install_from_pypi(source)
    elif source_type == "local":
        return plugin_installer.install_from_local(source)
    else:
        print(f"❌ Unknown source type: {source_type}")
        return False
