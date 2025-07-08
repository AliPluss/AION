"""
📘 Command Explainer - AI-Powered Command Analysis with Risk Assessment
======================================================================

Intercepts and explains CLI commands with comprehensive security analysis,
cross-platform support, and educational content.
"""

import asyncio
import logging
import platform
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

class SecurityLevel(Enum):
    SAFE = "safe"
    CAUTION = "caution"
    DANGEROUS = "dangerous"
    CRITICAL = "critical"

@dataclass
class CommandInfo:
    """Comprehensive command information"""
    command: str
    description: str
    security_level: SecurityLevel
    platform: str
    category: str
    parameters: List[str]
    examples: List[str]
    alternatives: List[str]
    warnings: List[str]
    best_practices: List[str]
    related_commands: List[str]

class CommandExplainer:
    """AI-powered command explanation with security assessment"""
    
    def __init__(self, provider_router, ai_logger):
        """Initialize command explainer"""
        self.provider_router = provider_router
        self.ai_logger = ai_logger
        
        # Current platform
        self.current_platform = platform.system().lower()
        
        # Command database
        self.command_database = self._build_command_database()
        
        # Security patterns
        self.dangerous_patterns = {
            'file_deletion': ['rm -rf', 'del /f', 'rmdir /s', 'shred', 'wipe'],
            'system_modification': ['chmod 777', 'chown', 'sudo', 'su', 'runas'],
            'network_access': ['wget', 'curl', 'nc', 'netcat', 'telnet'],
            'process_control': ['kill -9', 'killall', 'taskkill /f', 'pkill'],
            'disk_operations': ['dd', 'fdisk', 'format', 'mkfs', 'parted'],
            'system_control': ['shutdown', 'reboot', 'halt', 'systemctl', 'service']
        }
        
        # Explanation logs
        self.explanation_logs_dir = Path("test_logs")
        self.explanation_logs_dir.mkdir(exist_ok=True)
        
        logging.info("Command Explainer initialized successfully")
    
    async def explain(self, command: str, context: Optional[Dict] = None) -> str:
        """Explain a command with comprehensive analysis"""
        
        try:
            # Parse command
            command_parts = command.strip().split()
            if not command_parts:
                return "⚠️ No command provided"
            
            base_command = command_parts[0]
            
            # Get command info from database
            command_info = self._get_command_info(base_command)
            
            # Perform security analysis
            security_analysis = self._analyze_security(command)
            
            # Generate AI-enhanced explanation
            ai_explanation = await self._generate_ai_explanation(command, command_info, security_analysis, context)
            
            # Format comprehensive response
            response = self._format_explanation(command, command_info, security_analysis, ai_explanation)
            
            # Log explanation
            self._log_explanation(command, response, security_analysis['level'])
            
            return response
            
        except Exception as e:
            error_msg = f"Command explanation error: {e}"
            logging.error(error_msg)
            return f"⚠️ Unable to explain command: {e}"
    
    def _get_command_info(self, command: str) -> CommandInfo:
        """Get command information from database"""
        
        # Check platform-specific commands first
        platform_key = f"{self.current_platform}_{command}"
        if platform_key in self.command_database:
            return self.command_database[platform_key]
        
        # Check generic commands
        if command in self.command_database:
            return self.command_database[command]
        
        # Return unknown command info
        return CommandInfo(
            command=command,
            description=f"Unknown command: {command}",
            security_level=SecurityLevel.CAUTION,
            platform="unknown",
            category="unknown",
            parameters=[],
            examples=[],
            alternatives=[],
            warnings=["Unknown command - verify before execution"],
            best_practices=["Research command documentation", "Test in safe environment"],
            related_commands=[]
        )
    
    def _analyze_security(self, command: str) -> Dict[str, Any]:
        """Analyze command security risks"""
        
        command_lower = command.lower()
        risks = []
        security_level = SecurityLevel.SAFE
        
        # Check dangerous patterns
        for category, patterns in self.dangerous_patterns.items():
            for pattern in patterns:
                if pattern in command_lower:
                    risks.append({
                        "category": category,
                        "pattern": pattern,
                        "description": self._get_risk_description(category, pattern)
                    })
                    
                    # Escalate security level
                    if category in ['file_deletion', 'disk_operations', 'system_control']:
                        security_level = SecurityLevel.CRITICAL
                    elif category in ['system_modification', 'process_control']:
                        security_level = SecurityLevel.DANGEROUS
                    elif security_level == SecurityLevel.SAFE:
                        security_level = SecurityLevel.CAUTION
        
        # Check for privilege escalation
        if any(word in command_lower for word in ['sudo', 'su', 'runas', 'admin']):
            risks.append({
                "category": "privilege_escalation",
                "pattern": "privilege escalation",
                "description": "Command requires elevated privileges"
            })
            if security_level in [SecurityLevel.SAFE, SecurityLevel.CAUTION]:
                security_level = SecurityLevel.DANGEROUS
        
        # Check for wildcards in dangerous contexts
        if '*' in command and any(danger in command_lower for danger in ['rm', 'del', 'move', 'copy']):
            risks.append({
                "category": "wildcard_danger",
                "pattern": "wildcard usage",
                "description": "Wildcard usage in file operations can affect unintended files"
            })
            if security_level == SecurityLevel.SAFE:
                security_level = SecurityLevel.CAUTION
        
        return {
            "level": security_level,
            "risks": risks,
            "safe": security_level == SecurityLevel.SAFE,
            "requires_confirmation": security_level in [SecurityLevel.DANGEROUS, SecurityLevel.CRITICAL]
        }
    
    def _get_risk_description(self, category: str, pattern: str) -> str:
        """Get description for security risk"""
        descriptions = {
            'file_deletion': f"'{pattern}' can permanently delete files or directories",
            'system_modification': f"'{pattern}' modifies system permissions or ownership",
            'network_access': f"'{pattern}' accesses network resources",
            'process_control': f"'{pattern}' forcefully terminates processes",
            'disk_operations': f"'{pattern}' performs low-level disk operations",
            'system_control': f"'{pattern}' controls system power or services"
        }
        return descriptions.get(category, f"'{pattern}' may pose security risks")
    
    async def _generate_ai_explanation(self, command: str, command_info: CommandInfo, security_analysis: Dict, context: Optional[Dict] = None) -> str:
        """Generate AI-enhanced explanation"""
        
        prompt = f"""Explain this command in detail for a user learning terminal commands:

Command: {command}
Platform: {self.current_platform}
Security Level: {security_analysis['level'].value}

Base Information:
- Description: {command_info.description}
- Category: {command_info.category}
- Security Risks: {len(security_analysis['risks'])} identified

Please provide:
1. Clear explanation of what this command does
2. Step-by-step breakdown of parameters
3. Practical usage examples
4. Important warnings or considerations
5. Safer alternatives if applicable

Keep the explanation educational and accessible while being thorough about security implications."""
        
        try:
            ai_response = await self.provider_router.query(prompt, context)
            return ai_response
        except Exception as e:
            return f"AI explanation unavailable: {e}"
    
    def _format_explanation(self, command: str, command_info: CommandInfo, security_analysis: Dict, ai_explanation: str) -> str:
        """Format comprehensive explanation response"""
        
        # Security level emoji
        security_emojis = {
            SecurityLevel.SAFE: "✅",
            SecurityLevel.CAUTION: "⚠️",
            SecurityLevel.DANGEROUS: "🚨",
            SecurityLevel.CRITICAL: "💀"
        }
        
        security_emoji = security_emojis.get(security_analysis['level'], "❓")
        
        # Build response
        response_parts = [
            f"📘 **Command Explanation: `{command}`**",
            f"{security_emoji} **Security Level: {security_analysis['level'].value.upper()}**",
            ""
        ]
        
        # Add security warnings if needed
        if security_analysis['risks']:
            response_parts.extend([
                "🚨 **Security Risks Detected:**",
                ""
            ])
            for risk in security_analysis['risks']:
                response_parts.append(f"• **{risk['category'].replace('_', ' ').title()}**: {risk['description']}")
            response_parts.append("")
        
        # Add AI explanation
        response_parts.extend([
            "🤖 **AI Analysis:**",
            ai_explanation,
            ""
        ])
        
        # Add command database info
        if command_info.examples:
            response_parts.extend([
                "💡 **Examples:**",
                ""
            ])
            for example in command_info.examples[:3]:
                response_parts.append(f"• `{example}`")
            response_parts.append("")
        
        # Add alternatives if available
        if command_info.alternatives:
            response_parts.extend([
                "🔄 **Safer Alternatives:**",
                ""
            ])
            for alt in command_info.alternatives[:3]:
                response_parts.append(f"• `{alt}`")
            response_parts.append("")
        
        # Add best practices
        if command_info.best_practices:
            response_parts.extend([
                "✨ **Best Practices:**",
                ""
            ])
            for practice in command_info.best_practices[:3]:
                response_parts.append(f"• {practice}")
            response_parts.append("")
        
        # Add platform info
        response_parts.extend([
            f"🖥️ **Platform**: {command_info.platform} (Current: {self.current_platform})",
            f"📂 **Category**: {command_info.category}",
            ""
        ])
        
        # Add confirmation requirement
        if security_analysis['requires_confirmation']:
            response_parts.extend([
                "⚠️ **CONFIRMATION REQUIRED**: This command requires careful consideration before execution.",
                "Type 'yes' to confirm or 'no' to cancel.",
                ""
            ])
        
        return "\n".join(response_parts)
    
    def _log_explanation(self, command: str, explanation: str, security_level: SecurityLevel):
        """Log command explanation"""
        try:
            log_file = self.explanation_logs_dir / "system_command_explanation.log"
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "command": command,
                "security_level": security_level.value,
                "explanation_length": len(explanation),
                "platform": self.current_platform
            }
            
            with open(log_file, 'a') as f:
                f.write(f"{json.dumps(log_entry)}\n")
                
            self.ai_logger.log_command_explanation(command, security_level.value, len(explanation))
            
        except Exception as e:
            logging.error(f"Failed to log explanation: {e}")
    
    def _build_command_database(self) -> Dict[str, CommandInfo]:
        """Build comprehensive command database"""
        
        database = {}
        
        # Common Unix/Linux commands
        unix_commands = {
            "ls": CommandInfo(
                command="ls",
                description="List directory contents",
                security_level=SecurityLevel.SAFE,
                platform="unix",
                category="file_system",
                parameters=["-l", "-a", "-h", "-R"],
                examples=["ls -la", "ls -lh /home", "ls -R ."],
                alternatives=["dir (Windows)", "find . -maxdepth 1"],
                warnings=[],
                best_practices=["Use -l for detailed info", "Use -a to show hidden files"],
                related_commands=["find", "tree", "stat"]
            ),
            
            "rm": CommandInfo(
                command="rm",
                description="Remove files and directories",
                security_level=SecurityLevel.DANGEROUS,
                platform="unix",
                category="file_system",
                parameters=["-r", "-f", "-i", "-v"],
                examples=["rm file.txt", "rm -r directory/", "rm -i *.tmp"],
                alternatives=["mv to trash", "trash-put", "safe-rm"],
                warnings=["Permanent deletion", "No recycle bin", "Use -i for confirmation"],
                best_practices=["Always use -i flag", "Double-check paths", "Backup important files"],
                related_commands=["rmdir", "find", "trash"]
            )
        }
        
        # Windows commands
        windows_commands = {
            "dir": CommandInfo(
                command="dir",
                description="Display directory contents",
                security_level=SecurityLevel.SAFE,
                platform="windows",
                category="file_system",
                parameters=["/a", "/s", "/p", "/w"],
                examples=["dir /a", "dir /s C:\\", "dir *.txt"],
                alternatives=["ls (Unix)", "Get-ChildItem (PowerShell)"],
                warnings=[],
                best_practices=["Use /a to show hidden files", "Use /p for paging"],
                related_commands=["tree", "attrib", "find"]
            )
        }
        
        # Add to database
        database.update(unix_commands)
        database.update(windows_commands)
        
        return database
