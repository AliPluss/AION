#!/usr/bin/env python3
"""
📘 AION AI Command Explainer

AI-powered system command explanation with security warnings,
cross-platform support, and comprehensive educational content.

Features:
- Terminal command explanation (Linux, Windows, macOS)
- Security risk analysis
- Usage examples and alternatives
- Educational content with best practices
- Comprehensive logging
"""

import os
import json
import platform
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

console = Console()

@dataclass
class CommandExplanation:
    """Command explanation structure"""
    command: str
    platform: str
    description: str
    purpose: str
    syntax: str
    parameters: List[Dict[str, str]]
    examples: List[Dict[str, str]]
    security_level: str  # 'safe', 'caution', 'dangerous'
    security_warnings: List[str]
    alternatives: List[str]
    best_practices: List[str]
    related_commands: List[str]
    timestamp: datetime

class AICommandExplainer:
    """AI-powered command explanation system"""
    
    def __init__(self):
        self.log_file = Path("test_logs/system_command_explanation.log")
        self.log_file.parent.mkdir(exist_ok=True)
        
        self.current_platform = platform.system().lower()
        self.command_database = self._load_command_database()
        
    def _load_command_database(self) -> Dict[str, Dict]:
        """Load comprehensive command database"""
        return {
            # Linux/Unix Commands
            "ls": {
                "platforms": ["linux", "darwin"],
                "description": "List directory contents",
                "purpose": "Display files and directories in the current or specified directory",
                "syntax": "ls [OPTIONS] [FILE/DIRECTORY]",
                "security_level": "safe",
                "category": "file_management"
            },
            "cd": {
                "platforms": ["linux", "darwin", "windows"],
                "description": "Change directory",
                "purpose": "Navigate to a different directory in the filesystem",
                "syntax": "cd [DIRECTORY]",
                "security_level": "safe",
                "category": "navigation"
            },
            "rm": {
                "platforms": ["linux", "darwin"],
                "description": "Remove files and directories",
                "purpose": "Delete files and directories from the filesystem",
                "syntax": "rm [OPTIONS] FILE/DIRECTORY",
                "security_level": "dangerous",
                "category": "file_management"
            },
            "sudo": {
                "platforms": ["linux", "darwin"],
                "description": "Execute commands as another user",
                "purpose": "Run commands with elevated privileges (typically as root)",
                "syntax": "sudo [OPTIONS] COMMAND",
                "security_level": "dangerous",
                "category": "system_admin"
            },
            "chmod": {
                "platforms": ["linux", "darwin"],
                "description": "Change file permissions",
                "purpose": "Modify read, write, and execute permissions for files and directories",
                "syntax": "chmod [OPTIONS] MODE FILE",
                "security_level": "caution",
                "category": "permissions"
            },
            "ps": {
                "platforms": ["linux", "darwin"],
                "description": "Display running processes",
                "purpose": "Show information about currently running processes",
                "syntax": "ps [OPTIONS]",
                "security_level": "safe",
                "category": "process_management"
            },
            "kill": {
                "platforms": ["linux", "darwin"],
                "description": "Terminate processes",
                "purpose": "Send signals to processes, typically to terminate them",
                "syntax": "kill [OPTIONS] PID",
                "security_level": "caution",
                "category": "process_management"
            },
            
            # Windows Commands
            "dir": {
                "platforms": ["windows"],
                "description": "List directory contents",
                "purpose": "Display files and directories in the current or specified directory",
                "syntax": "dir [PATH] [OPTIONS]",
                "security_level": "safe",
                "category": "file_management"
            },
            "del": {
                "platforms": ["windows"],
                "description": "Delete files",
                "purpose": "Remove files from the filesystem",
                "syntax": "del [OPTIONS] FILE",
                "security_level": "dangerous",
                "category": "file_management"
            },
            "tasklist": {
                "platforms": ["windows"],
                "description": "Display running processes",
                "purpose": "Show information about currently running processes and services",
                "syntax": "tasklist [OPTIONS]",
                "security_level": "safe",
                "category": "process_management"
            },
            "taskkill": {
                "platforms": ["windows"],
                "description": "Terminate processes",
                "purpose": "End running processes by PID or process name",
                "syntax": "taskkill [OPTIONS] /PID processid | /IM imagename",
                "security_level": "caution",
                "category": "process_management"
            },
            
            # Cross-platform commands
            "python": {
                "platforms": ["linux", "darwin", "windows"],
                "description": "Python interpreter",
                "purpose": "Execute Python scripts and start interactive Python sessions",
                "syntax": "python [OPTIONS] [SCRIPT] [ARGUMENTS]",
                "security_level": "caution",
                "category": "programming"
            },
            "git": {
                "platforms": ["linux", "darwin", "windows"],
                "description": "Git version control system",
                "purpose": "Manage source code versions and collaborate on projects",
                "syntax": "git [OPTIONS] COMMAND [ARGS]",
                "security_level": "safe",
                "category": "version_control"
            },
            "curl": {
                "platforms": ["linux", "darwin", "windows"],
                "description": "Transfer data from/to servers",
                "purpose": "Download or upload data using various protocols (HTTP, FTP, etc.)",
                "syntax": "curl [OPTIONS] URL",
                "security_level": "caution",
                "category": "networking"
            }
        }
    
    async def explain_command(self, command: str) -> CommandExplanation:
        """Generate comprehensive command explanation"""
        
        # Parse command (handle command with arguments)
        base_command = command.split()[0] if command else ""
        
        # Get command info from database
        cmd_info = self.command_database.get(base_command, {})
        
        if not cmd_info:
            return await self._generate_unknown_command_explanation(command)
        
        # Generate comprehensive explanation
        explanation = CommandExplanation(
            command=command,
            platform=self.current_platform,
            description=cmd_info.get("description", "Unknown command"),
            purpose=cmd_info.get("purpose", "Purpose not available"),
            syntax=cmd_info.get("syntax", f"{base_command} [OPTIONS]"),
            parameters=await self._generate_parameters(base_command, cmd_info),
            examples=await self._generate_examples(base_command, cmd_info),
            security_level=cmd_info.get("security_level", "caution"),
            security_warnings=await self._generate_security_warnings(base_command, cmd_info),
            alternatives=await self._generate_alternatives(base_command, cmd_info),
            best_practices=await self._generate_best_practices(base_command, cmd_info),
            related_commands=await self._generate_related_commands(base_command, cmd_info),
            timestamp=datetime.now()
        )
        
        # Log explanation
        self._log_explanation(explanation)
        
        return explanation
    
    async def _generate_unknown_command_explanation(self, command: str) -> CommandExplanation:
        """Generate explanation for unknown commands"""
        return CommandExplanation(
            command=command,
            platform=self.current_platform,
            description="Unknown or custom command",
            purpose="This command is not in our database. It might be a custom script, alias, or less common utility.",
            syntax=f"{command} [arguments]",
            parameters=[],
            examples=[
                {"description": "Check if command exists", "command": f"which {command.split()[0]}", "platform": "linux"},
                {"description": "Get command help", "command": f"{command.split()[0]} --help", "platform": "all"},
                {"description": "Check manual page", "command": f"man {command.split()[0]}", "platform": "linux"}
            ],
            security_level="caution",
            security_warnings=[
                "Unknown commands should be researched before execution",
                "Verify the source and purpose of custom commands",
                "Be cautious with commands from untrusted sources"
            ],
            alternatives=[
                "Research the command online",
                "Check system documentation",
                "Ask system administrator"
            ],
            best_practices=[
                "Always verify unknown commands before running",
                "Use --help or man pages for documentation",
                "Test in safe environment first"
            ],
            related_commands=["which", "man", "help"],
            timestamp=datetime.now()
        )
    
    async def _generate_parameters(self, command: str, cmd_info: Dict) -> List[Dict[str, str]]:
        """Generate parameter explanations"""
        parameter_map = {
            "ls": [
                {"param": "-l", "description": "Long format listing with detailed information"},
                {"param": "-a", "description": "Show all files including hidden ones"},
                {"param": "-h", "description": "Human-readable file sizes"},
                {"param": "-R", "description": "Recursive listing of subdirectories"}
            ],
            "rm": [
                {"param": "-r", "description": "Remove directories recursively"},
                {"param": "-f", "description": "Force removal without prompts"},
                {"param": "-i", "description": "Interactive mode - prompt before removal"},
                {"param": "-v", "description": "Verbose mode - show what's being removed"}
            ],
            "chmod": [
                {"param": "755", "description": "Owner: read/write/execute, Group/Others: read/execute"},
                {"param": "644", "description": "Owner: read/write, Group/Others: read only"},
                {"param": "-R", "description": "Apply permissions recursively"}
            ],
            "ps": [
                {"param": "aux", "description": "Show all processes with detailed information"},
                {"param": "-ef", "description": "Full format listing of all processes"},
                {"param": "-u username", "description": "Show processes for specific user"}
            ]
        }
        
        return parameter_map.get(command, [
            {"param": "--help", "description": "Display help information"},
            {"param": "--version", "description": "Show version information"}
        ])
    
    async def _generate_examples(self, command: str, cmd_info: Dict) -> List[Dict[str, str]]:
        """Generate usage examples"""
        example_map = {
            "ls": [
                {"description": "List files in current directory", "command": "ls"},
                {"description": "Detailed listing with permissions", "command": "ls -la"},
                {"description": "List specific directory", "command": "ls /home/user/documents"}
            ],
            "cd": [
                {"description": "Go to home directory", "command": "cd ~"},
                {"description": "Go to parent directory", "command": "cd .."},
                {"description": "Go to specific directory", "command": "cd /path/to/directory"}
            ],
            "rm": [
                {"description": "Remove a file", "command": "rm filename.txt"},
                {"description": "Remove directory and contents", "command": "rm -rf directory/"},
                {"description": "Interactive removal", "command": "rm -i *.tmp"}
            ],
            "chmod": [
                {"description": "Make file executable", "command": "chmod +x script.sh"},
                {"description": "Set specific permissions", "command": "chmod 755 file.txt"},
                {"description": "Recursive permission change", "command": "chmod -R 644 directory/"}
            ]
        }
        
        return example_map.get(command, [
            {"description": f"Basic usage", "command": f"{command}"},
            {"description": f"Get help", "command": f"{command} --help"}
        ])
    
    async def _generate_security_warnings(self, command: str, cmd_info: Dict) -> List[str]:
        """Generate security warnings"""
        security_map = {
            "rm": [
                "⚠️ DANGER: rm permanently deletes files - no recycle bin!",
                "🚨 CRITICAL: 'rm -rf /' can destroy entire system",
                "⚡ WARNING: Always double-check paths before using -f flag",
                "💡 TIP: Use 'rm -i' for interactive confirmation"
            ],
            "sudo": [
                "🔒 ELEVATED PRIVILEGES: Commands run with full system access",
                "⚠️ DANGER: Can modify critical system files",
                "🚨 SECURITY: Only use with trusted commands",
                "💡 PRINCIPLE: Use least privilege - avoid when possible"
            ],
            "chmod": [
                "🔐 PERMISSIONS: Incorrect settings can break system security",
                "⚠️ WARNING: 777 permissions are dangerous (world-writable)",
                "🚨 SECURITY: Be careful with executable permissions",
                "💡 BEST PRACTICE: Use minimal required permissions"
            ],
            "curl": [
                "🌐 NETWORK: Downloads from internet - verify sources",
                "⚠️ SECURITY: Can execute downloaded scripts",
                "🚨 DANGER: Malicious URLs can harm system",
                "💡 SAFETY: Always verify URLs and use HTTPS"
            ]
        }
        
        security_level = cmd_info.get("security_level", "safe")
        
        if security_level == "dangerous":
            base_warnings = ["🚨 HIGH RISK COMMAND - Use with extreme caution"]
        elif security_level == "caution":
            base_warnings = ["⚠️ MODERATE RISK - Verify before execution"]
        else:
            base_warnings = ["✅ Generally safe command"]
        
        return base_warnings + security_map.get(command, [])
    
    async def _generate_alternatives(self, command: str, cmd_info: Dict) -> List[str]:
        """Generate safer alternatives"""
        alternatives_map = {
            "rm": ["trash-cli (safer deletion)", "mv to backup directory", "GUI file manager"],
            "sudo": ["Use specific user permissions", "Configure sudoers properly", "Use su for user switching"],
            "chmod": ["Use symbolic notation (u+x)", "Set umask for defaults", "Use ACLs for complex permissions"],
            "curl": ["wget (alternative downloader)", "Browser download", "Package manager for software"]
        }
        
        return alternatives_map.get(command, ["Check manual pages", "Use GUI alternatives", "Ask system administrator"])
    
    async def _generate_best_practices(self, command: str, cmd_info: Dict) -> List[str]:
        """Generate best practices"""
        return [
            "Always read documentation before using new commands",
            "Test commands in safe environment first",
            "Use version control for important files",
            "Keep regular backups",
            "Follow principle of least privilege",
            "Verify command syntax before execution"
        ]
    
    async def _generate_related_commands(self, command: str, cmd_info: Dict) -> List[str]:
        """Generate related commands"""
        related_map = {
            "ls": ["dir (Windows)", "find", "locate", "tree"],
            "cd": ["pwd", "pushd", "popd", "dirs"],
            "rm": ["rmdir", "trash", "mv", "cp"],
            "chmod": ["chown", "chgrp", "umask", "getfacl"],
            "ps": ["top", "htop", "pgrep", "jobs"],
            "kill": ["killall", "pkill", "jobs", "nohup"]
        }
        
        return related_map.get(command, ["man", "help", "which", "type"])
    
    def _log_explanation(self, explanation: CommandExplanation):
        """Log command explanation"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{timestamp} - COMMAND_EXPLAINED: {json.dumps(asdict(explanation), indent=2, default=str)}\n")
        except Exception as e:
            console.print(f"⚠️ [yellow]Logging error: {e}[/yellow]")
    
    def format_explanation_display(self, explanation: CommandExplanation) -> str:
        """Format explanation for display"""
        
        # Security level colors
        security_colors = {
            "safe": "green",
            "caution": "yellow", 
            "dangerous": "red"
        }
        
        security_color = security_colors.get(explanation.security_level, "yellow")
        
        output = f"""
📘 **Command Explanation: {explanation.command}**

**Platform:** {explanation.platform.title()}
**Security Level:** [{security_color}]{explanation.security_level.upper()}[/{security_color}]

**Description:** {explanation.description}

**Purpose:** {explanation.purpose}

**Syntax:** `{explanation.syntax}`

**Parameters:**"""
        
        for param in explanation.parameters[:5]:  # Limit to 5 parameters
            output += f"\n  • `{param['param']}` - {param['description']}"
        
        output += f"\n\n**Examples:**"
        for example in explanation.examples[:3]:  # Limit to 3 examples
            output += f"\n  • {example['description']}: `{example['command']}`"
        
        output += f"\n\n**Security Warnings:**"
        for warning in explanation.security_warnings:
            output += f"\n  • {warning}"
        
        output += f"\n\n**Alternatives:**"
        for alt in explanation.alternatives:
            output += f"\n  • {alt}"
        
        output += f"\n\n**Related Commands:** {', '.join(explanation.related_commands)}"
        
        return output

# Global command explainer instance
command_explainer = AICommandExplainer()
