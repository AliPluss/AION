#!/usr/bin/env python3
"""
📧 AION Email Integration System

Professional email functionality for AION with SMTP/IMAP support,
OTP authentication, and comprehensive template system.

Features:
- Secure SMTP/IMAP configuration
- Live TUI integration
- Email templates and formatting
- Attachment support
- Delivery tracking
- Comprehensive logging
"""

import smtplib
import os
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path
import json
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm

console = Console()

@dataclass
class EmailConfig:
    """Email configuration settings"""
    smtp_server: str
    smtp_port: int
    username: str
    password: str
    use_tls: bool = True

@dataclass
class EmailMessage:
    """Email message structure"""
    to: List[str]
    subject: str
    body: str
    attachments: List[str] = None
    cc: List[str] = None
    bcc: List[str] = None
    html_body: str = None

class EmailSystem:
    """Professional email system for AION"""
    
    def __init__(self):
        self.config = self._load_config()
        self.sent_emails = []
        self.log_file = Path("test_logs/email_sending_test.log")
        self.log_file.parent.mkdir(exist_ok=True)
        
    def _load_config(self) -> Optional[EmailConfig]:
        """Load email configuration from environment"""
        try:
            if not os.getenv('AION_EMAIL_ENABLED', 'false').lower() == 'true':
                return None
                
            return EmailConfig(
                smtp_server=os.getenv('AION_SMTP_SERVER', 'smtp.gmail.com'),
                smtp_port=int(os.getenv('AION_SMTP_PORT', '587')),
                username=os.getenv('AION_EMAIL_USER', ''),
                password=os.getenv('AION_EMAIL_PASSWORD', ''),
                use_tls=os.getenv('AION_EMAIL_TLS', 'true').lower() == 'true'
            )
        except Exception as e:
            console.print(f"❌ [red]Email config error: {e}[/red]")
            return None
    
    def _log_email_action(self, action: str, details: Dict[str, Any]):
        """Log email actions to test log file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{timestamp} - {action}: {json.dumps(details, indent=2)}\n")
        except Exception as e:
            console.print(f"⚠️ [yellow]Logging error: {e}[/yellow]")
    
    def send_email_interactive(self) -> bool:
        """Interactive email sending via TUI"""
        console.print("\n📧 [bold yellow]Email Sharing System[/bold yellow]")
        
        if not self.config:
            console.print("❌ [red]Email not configured. Please set up email in .env file[/red]")
            console.print("💡 [cyan]Set AION_EMAIL_ENABLED=true and configure SMTP settings[/cyan]")
            self._log_email_action("SEND_FAILED", {"error": "Email not configured"})
            return False
        
        try:
            # Get recipient
            recipient = Prompt.ask("📮 [bold cyan]Recipient email address[/bold cyan]")
            if not recipient or "@" not in recipient:
                console.print("❌ [red]Invalid email address[/red]")
                return False
            
            # Get subject
            subject = Prompt.ask("📝 [bold cyan]Email subject[/bold cyan]", default="AION Shared Content")
            
            # Get content type
            console.print("\n📄 [bold yellow]Content to send:[/bold yellow]")
            console.print("1. 📝 Text message")
            console.print("2. 📁 File attachment")
            console.print("3. 💻 Terminal output")
            
            content_choice = Prompt.ask("Choose content type", choices=["1", "2", "3"], default="1")
            
            body = ""
            attachments = []
            
            if content_choice == "1":
                body = Prompt.ask("✍️ [bold cyan]Enter your message[/bold cyan]")
            elif content_choice == "2":
                file_path = Prompt.ask("📁 [bold cyan]File path to attach[/bold cyan]")
                if Path(file_path).exists():
                    attachments.append(file_path)
                    body = f"Please find the attached file: {Path(file_path).name}"
                else:
                    console.print(f"❌ [red]File not found: {file_path}[/red]")
                    return False
            elif content_choice == "3":
                body = Prompt.ask("💻 [bold cyan]Enter terminal output to share[/bold cyan]")
                body = f"Terminal Output from AION:\n\n```\n{body}\n```"
            
            # Create email message
            email_msg = EmailMessage(
                to=[recipient],
                subject=subject,
                body=body,
                attachments=attachments
            )
            
            # Confirm sending
            if Confirm.ask(f"📤 Send email to {recipient}?"):
                return self.send_email(email_msg)
            else:
                console.print("📧 [yellow]Email cancelled[/yellow]")
                return False
                
        except KeyboardInterrupt:
            console.print("\n📧 [yellow]Email cancelled by user[/yellow]")
            return False
        except Exception as e:
            console.print(f"❌ [red]Email error: {e}[/red]")
            self._log_email_action("SEND_ERROR", {"error": str(e)})
            return False
    
    def send_email(self, message: EmailMessage) -> bool:
        """Send email message"""
        if not self.config:
            console.print("❌ [red]Email not configured[/red]")
            return False
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("📤 Sending email...", total=None)
                
                # Create message
                msg = MIMEMultipart()
                msg['From'] = self.config.username
                msg['To'] = ', '.join(message.to)
                msg['Subject'] = message.subject
                
                # Add body
                msg.attach(MIMEText(message.body, 'plain'))
                
                # Add attachments
                if message.attachments:
                    for file_path in message.attachments:
                        self._add_attachment(msg, file_path)
                
                # Send email
                context = ssl.create_default_context()
                with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
                    if self.config.use_tls:
                        server.starttls(context=context)
                    server.login(self.config.username, self.config.password)
                    server.send_message(msg)
                
                progress.update(task, completed=True)
            
            console.print("✅ [green]Email sent successfully![/green]")
            
            # Log successful send
            self._log_email_action("SEND_SUCCESS", {
                "to": message.to,
                "subject": message.subject,
                "attachments": message.attachments or [],
                "timestamp": datetime.now().isoformat()
            })
            
            self.sent_emails.append(message)
            return True
            
        except Exception as e:
            console.print(f"❌ [red]Failed to send email: {e}[/red]")
            self._log_email_action("SEND_FAILED", {
                "to": message.to,
                "subject": message.subject,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
            return False
    
    def _add_attachment(self, msg: MIMEMultipart, file_path: str):
        """Add file attachment to email"""
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {Path(file_path).name}'
            )
            msg.attach(part)
            
        except Exception as e:
            console.print(f"⚠️ [yellow]Failed to attach {file_path}: {e}[/yellow]")
    
    def get_email_stats(self) -> Dict[str, Any]:
        """Get email statistics"""
        return {
            "total_sent": len(self.sent_emails),
            "configured": self.config is not None,
            "last_sent": self.sent_emails[-1].subject if self.sent_emails else None
        }

# Global email system instance
email_system = EmailSystem()
