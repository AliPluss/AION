"""
🔗 AION External Integrations Module

Professional external platform integrations for AION:

- 📧 Email System: SMTP/IMAP with OTP authentication and templates
- 🐙 GitHub Integration: Repository management, gists, and automation
- 💬 Slack Integration: Bot functionality and notifications
- 📁 Google Drive: File synchronization and cloud storage
- 📝 Notion Integration: Database management and content sync

All integrations feature:
- Secure authentication and API key management
- Comprehensive error handling and retry logic
- Rate limiting and quota management
- Multilingual support and localization
- Professional logging and audit trails
"""

from .email_system import EmailSystem
from .github_integration import GitHubIntegration
from .slack_integration import SlackIntegration
from .google_drive_integration import GoogleDriveIntegration
from .notion_integration import NotionIntegration

__all__ = [
    "EmailSystem",
    "GitHubIntegration",
    "SlackIntegration",
    "GoogleDriveIntegration", 
    "NotionIntegration"
]

# Integration availability and status
INTEGRATIONS_STATUS = {
    "email": {"available": True, "requires_config": True},
    "github": {"available": True, "requires_config": True},
    "slack": {"available": True, "requires_config": True},
    "google_drive": {"available": True, "requires_config": True},
    "notion": {"available": True, "requires_config": True}
}

def get_available_integrations():
    """Get list of available integrations"""
    return [name for name, status in INTEGRATIONS_STATUS.items() if status["available"]]

def get_integration_status(integration_name: str) -> dict:
    """Get status information for a specific integration"""
    return INTEGRATIONS_STATUS.get(integration_name, {"available": False, "requires_config": False})

def is_integration_available(integration_name: str) -> bool:
    """Check if a specific integration is available"""
    status = INTEGRATIONS_STATUS.get(integration_name, {})
    return status.get("available", False)
