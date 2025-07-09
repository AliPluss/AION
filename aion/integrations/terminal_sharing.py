"""
Terminal Output Sharing System for AION
Supports uploading terminal output to various sharing platforms
"""

import os
import json
import requests
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

@dataclass
class ShareConfig:
    """Configuration for sharing services"""
    service: str
    api_url: str
    api_key: Optional[str] = None
    expiry_days: int = 30

@dataclass
class ShareResult:
    """Result of sharing operation"""
    success: bool
    url: Optional[str] = None
    delete_url: Optional[str] = None
    expiry: Optional[str] = None
    error: Optional[str] = None

class TerminalSharing:
    """Professional terminal output sharing system for AION"""
    
    def __init__(self):
        self.log_file = Path("test_logs/terminal_sharing.log")
        self.log_file.parent.mkdir(exist_ok=True)
        
        # Available sharing services
        self.services = {
            "pastebin": ShareConfig(
                service="pastebin",
                api_url="https://pastebin.com/api/api_post.php",
                api_key=os.getenv('AION_PASTEBIN_API_KEY'),
                expiry_days=30
            ),
            "privatebin": ShareConfig(
                service="privatebin",
                api_url="https://privatebin.net",
                expiry_days=7
            ),
            "dpaste": ShareConfig(
                service="dpaste",
                api_url="https://dpaste.org/api/",
                expiry_days=7
            ),
            "hastebin": ShareConfig(
                service="hastebin",
                api_url="https://hastebin.com/documents",
                expiry_days=30
            )
        }
        
    def _log_sharing_action(self, action: str, details: Dict[str, Any]):
        """Log sharing activity"""
        try:
            timestamp = datetime.now().isoformat()
            log_entry = {
                "timestamp": timestamp,
                "action": action,
                "details": details
            }
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{timestamp} - {action}: {json.dumps(details, indent=2)}\n")
        except Exception as e:
            console.print(f"⚠️ [yellow]Logging error: {e}[/yellow]")
    
    def share_terminal_output_interactive(self) -> bool:
        """Interactive terminal output sharing"""
        console.print("\n📤 [bold yellow]Terminal Output Sharing[/bold yellow]")
        
        try:
            # Get content to share
            content_choice = Prompt.ask(
                "📋 [bold cyan]What would you like to share?[/bold cyan]",
                choices=["1", "2", "3"],
                default="1"
            )
            
            content = ""
            title = "AION Terminal Output"
            
            if content_choice == "1":
                content = Prompt.ask("💻 [bold cyan]Paste terminal output[/bold cyan]")
                title = "AION Terminal Output"
            elif content_choice == "2":
                file_path = Prompt.ask("📁 [bold cyan]File path to share[/bold cyan]")
                if Path(file_path).exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    title = f"AION File: {Path(file_path).name}"
                else:
                    console.print(f"❌ [red]File not found: {file_path}[/red]")
                    return False
            elif content_choice == "3":
                content = Prompt.ask("✍️ [bold cyan]Enter custom text[/bold cyan]")
                title = Prompt.ask("📝 [bold cyan]Title[/bold cyan]", default="AION Shared Content")
            
            if not content.strip():
                console.print("❌ [red]No content to share[/red]")
                return False
            
            # Choose sharing service
            service_choice = Prompt.ask(
                "🌐 [bold cyan]Choose sharing service[/bold cyan]",
                choices=["1", "2", "3", "4"],
                default="1"
            )
            
            service_map = {
                "1": "dpaste",
                "2": "hastebin", 
                "3": "pastebin",
                "4": "privatebin"
            }
            
            service_name = service_map[service_choice]
            
            console.print(f"\n📤 [yellow]Sharing to {service_name}...[/yellow]")
            
            # Share content
            result = self._share_content(content, title, service_name)
            
            if result.success:
                console.print(f"✅ [green]Content shared successfully![/green]")
                console.print(f"🔗 [cyan]URL: {result.url}[/cyan]")
                if result.delete_url:
                    console.print(f"🗑️ [yellow]Delete URL: {result.delete_url}[/yellow]")
                if result.expiry:
                    console.print(f"⏰ [dim]Expires: {result.expiry}[/dim]")
                
                self._log_sharing_action("SHARE_SUCCESS", {
                    "service": service_name,
                    "url": result.url,
                    "title": title,
                    "content_length": len(content)
                })
                return True
            else:
                console.print(f"❌ [red]Sharing failed: {result.error}[/red]")
                self._log_sharing_action("SHARE_FAILED", {
                    "service": service_name,
                    "error": result.error
                })
                return False
                
        except Exception as e:
            console.print(f"❌ [red]Sharing error: {e}[/red]")
            self._log_sharing_action("SHARE_ERROR", {"error": str(e)})
            return False
    
    def _share_content(self, content: str, title: str, service: str) -> ShareResult:
        """Share content to specified service"""
        try:
            if service == "dpaste":
                return self._share_to_dpaste(content, title)
            elif service == "hastebin":
                return self._share_to_hastebin(content)
            elif service == "pastebin":
                return self._share_to_pastebin(content, title)
            elif service == "privatebin":
                return self._share_to_privatebin(content, title)
            else:
                return ShareResult(success=False, error=f"Unknown service: {service}")
                
        except Exception as e:
            return ShareResult(success=False, error=str(e))
    
    def _share_to_dpaste(self, content: str, title: str) -> ShareResult:
        """Share to dpaste.org"""
        try:
            # dpaste.org API format
            data = {
                'content': content,
                'syntax': 'text',
                'expiry_days': 7
            }

            response = requests.post(
                "https://dpaste.org/api/",
                data=data,
                timeout=10,
                headers={'User-Agent': 'AION Terminal Assistant'}
            )

            if response.status_code in [200, 201]:
                # dpaste returns the URL directly
                url = response.text.strip()
                # Clean up any quotes or extra formatting
                url = url.strip('"').strip("'")

                if url.startswith('http'):
                    return ShareResult(
                        success=True,
                        url=url,
                        expiry="7 days"
                    )
                else:
                    # Try to construct URL from response
                    if url.startswith('/'):
                        url = f"https://dpaste.org{url}"
                    else:
                        url = f"https://dpaste.org/{url}"
                    return ShareResult(
                        success=True,
                        url=url,
                        expiry="7 days"
                    )
            else:
                return ShareResult(success=False, error=f"HTTP {response.status_code}: {response.text}")

        except Exception as e:
            return ShareResult(success=False, error=str(e))
    
    def _share_to_hastebin(self, content: str) -> ShareResult:
        """Share to hastebin.com"""
        try:
            response = requests.post(
                "https://hastebin.com/documents",
                data=content,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                key = result.get('key')
                if key:
                    url = f"https://hastebin.com/{key}"
                    return ShareResult(
                        success=True,
                        url=url,
                        expiry="30 days"
                    )
            
            return ShareResult(success=False, error="Failed to get key from response")
            
        except Exception as e:
            return ShareResult(success=False, error=str(e))
    
    def _share_to_pastebin(self, content: str, title: str) -> ShareResult:
        """Share to pastebin.com"""
        try:
            config = self.services["pastebin"]
            
            if not config.api_key:
                # Use guest posting (limited features)
                return ShareResult(
                    success=False, 
                    error="Pastebin API key not configured. Set AION_PASTEBIN_API_KEY in .env"
                )
            
            data = {
                'api_dev_key': config.api_key,
                'api_option': 'paste',
                'api_paste_code': content,
                'api_paste_name': title,
                'api_paste_expire_date': '1M',
                'api_paste_private': '1'  # Unlisted
            }
            
            response = requests.post(config.api_url, data=data, timeout=10)
            
            if response.status_code == 200 and response.text.startswith('https://'):
                return ShareResult(
                    success=True,
                    url=response.text.strip(),
                    expiry="1 month"
                )
            else:
                return ShareResult(success=False, error=response.text)
                
        except Exception as e:
            return ShareResult(success=False, error=str(e))
    
    def _share_to_privatebin(self, content: str, title: str) -> ShareResult:
        """Share to privatebin.net (simulated - requires complex encryption)"""
        try:
            # PrivateBin requires client-side encryption, so we'll simulate
            # In a real implementation, you'd need to implement the encryption
            return ShareResult(
                success=False,
                error="PrivateBin requires client-side encryption (not implemented)"
            )
            
        except Exception as e:
            return ShareResult(success=False, error=str(e))

# Global instance
terminal_sharing = TerminalSharing()
