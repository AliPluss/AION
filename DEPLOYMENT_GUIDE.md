# 🚀 AION Deployment Guide

## Complete AI Operating Node - Professional Deployment

### 📋 System Requirements

- **Python**: 3.10+ (Recommended: 3.12)
- **Operating System**: Windows 10/11, macOS, Linux
- **Memory**: Minimum 4GB RAM (Recommended: 8GB+)
- **Storage**: 2GB free space
- **Network**: Internet connection for AI providers and integrations

### 🔧 Installation Methods

#### Method 1: Quick Start (Recommended)
```bash
# Clone or download AION
git clone <repository-url>
cd aion_github_clean

# Install core dependencies
pip install -r requirements.txt

# Run AION
python main.py
```

#### Method 2: Virtual Environment (Production)
```bash
# Create virtual environment
python -m venv aion_venv

# Activate environment
# Windows:
aion_venv\Scripts\activate
# macOS/Linux:
source aion_venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run AION
python main.py
```

#### Method 3: With External Integrations
```bash
# Install all integrations
pip install -r requirements-integrations.txt

# Configure integrations (see Configuration section)
# Run AION with full features
python main.py
```

### ⚙️ Configuration

#### 1. AI Providers Configuration
Edit `config/ai_config.json`:
```json
{
  "providers": {
    "openai": {
      "api_key": "your-openai-api-key",
      "enabled": true
    },
    "deepseek": {
      "api_key": "your-deepseek-api-key",
      "enabled": true
    }
  }
}
```

#### 2. External Integrations Configuration
Edit `config/integrations_config.json`:

**Email Integration:**
```json
{
  "email": {
    "enabled": true,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "your-email@gmail.com",
    "password": "your-app-password"
  }
}
```

**GitHub Integration:**
```json
{
  "github": {
    "enabled": true,
    "api_token": "your-github-token",
    "default_username": "your-username"
  }
}
```

**Slack Integration:**
```json
{
  "slack": {
    "enabled": true,
    "bot_token": "xoxb-your-bot-token",
    "app_token": "xapp-your-app-token"
  }
}
```

**Google Drive Integration:**
```json
{
  "google_drive": {
    "enabled": true,
    "credentials_file": "path/to/credentials.json"
  }
}
```

**Notion Integration:**
```json
{
  "notion": {
    "enabled": true,
    "api_token": "your-notion-integration-token"
  }
}
```

### 🧪 Testing Installation

#### Basic System Test
```bash
# Test core functionality
python -c "from main import main; print('✅ AION Core: OK')"

# Test integrations
python test_integrations_simple.py
```

#### Comprehensive Test
```bash
# Run full test suite
python -m pytest tests/ -v

# Test specific components
python test_advanced_ai_system.py
python test_automation_recipes.py
python test_sandbox_system.py
```

### 🔐 Security Setup

#### 1. Dynamic Security System
AION includes a dynamic security system that:
- Changes encryption parameters every minute
- Monitors threats in real-time
- Provides adaptive protection levels
- Logs all security events

#### 2. API Key Security
- Store API keys in environment variables
- Use `.env` files for local development
- Never commit API keys to version control
- Rotate keys regularly

#### 3. Sandbox Execution
- All code execution is sandboxed by default
- Docker integration for isolated execution
- Resource monitoring and limits
- Security threat detection

### 🚀 Production Deployment

#### 1. Environment Variables
```bash
# Set environment variables
export OPENAI_API_KEY="your-key"
export DEEPSEEK_API_KEY="your-key"
export GITHUB_TOKEN="your-token"
export SLACK_BOT_TOKEN="your-token"
export NOTION_API_TOKEN="your-token"
```

#### 2. Service Configuration
Create systemd service (Linux) or Windows Service:
```ini
[Unit]
Description=AION AI Operating Node
After=network.target

[Service]
Type=simple
User=aion
WorkingDirectory=/path/to/aion
ExecStart=/path/to/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

#### 3. Monitoring Setup
- Enable logging: Set `LOG_LEVEL=INFO`
- Configure log rotation
- Set up health checks
- Monitor resource usage

### 📊 Performance Optimization

#### 1. System Optimization
- Use SSD storage for better performance
- Allocate sufficient RAM (8GB+ recommended)
- Enable caching for AI responses
- Use connection pooling for integrations

#### 2. AI Provider Optimization
- Configure rate limiting
- Enable response caching
- Use appropriate model selection
- Monitor usage and costs

#### 3. Integration Optimization
- Enable batch operations
- Use async operations where possible
- Configure connection pooling
- Set appropriate timeouts

### 🔧 Troubleshooting

#### Common Issues

**1. Import Errors**
```bash
# Solution: Install missing dependencies
pip install -r requirements.txt
pip install -r requirements-integrations.txt
```

**2. API Connection Issues**
```bash
# Solution: Check API keys and network
python -c "import requests; print(requests.get('https://api.openai.com/v1/models', headers={'Authorization': 'Bearer YOUR_KEY'}).status_code)"
```

**3. Permission Issues**
```bash
# Solution: Check file permissions
chmod +x main.py
# Or run with appropriate user permissions
```

**4. Port Conflicts**
```bash
# Solution: Change default ports in config
# Edit config files to use different ports
```

### 📞 Support

#### Getting Help
1. Check the troubleshooting section
2. Review log files in `logs/` directory
3. Run diagnostic tests
4. Check GitHub issues

#### Diagnostic Commands
```bash
# System health check
python -c "from core.health_check import run_health_check; run_health_check()"

# Integration status
python test_integrations_simple.py

# Security status
python -c "from core.security import SecurityManager; sm = SecurityManager(); print(sm.get_security_status())"
```

### 🎯 Next Steps

After successful deployment:
1. Configure your preferred AI providers
2. Set up external integrations as needed
3. Customize language preferences
4. Create automation recipes
5. Set up monitoring and logging
6. Train team members on usage

### 📈 Scaling

For enterprise deployment:
- Use load balancers for multiple instances
- Implement database clustering
- Set up distributed caching
- Configure monitoring and alerting
- Implement backup and disaster recovery

---

**🎉 Congratulations! AION is now ready for professional use!**

For advanced configuration and customization, refer to the individual component documentation in the `docs/` directory.
