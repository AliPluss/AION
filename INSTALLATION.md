# 🚀 AION Installation Guide

## Quick Installation (Recommended)

### Prerequisites
- **Python 3.10+** (Required)
- **Git** (for cloning repository)
- **4GB RAM** minimum (8GB recommended)
- **2GB free storage**

### One-Command Installation

```bash
# Clone and setup AION in one go
git clone https://github.com/AliPluss/AION.git && cd AION && python setup_aion_fixed.py
```

### Step-by-Step Installation

1. **Clone Repository**:
```bash
git clone https://github.com/AliPluss/AION.git
cd AION
```

2. **Run Setup Script**:
```bash
python setup_aion_fixed.py
```

3. **Start AION**:
```bash
cd aion_project
python main.py start
```

## Manual Installation

### 1. Create Virtual Environment
```bash
python -m venv aion_env
source aion_env/bin/activate  # Windows: aion_env\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Settings
```bash
# Copy configuration template
cp config/config_template.json config/config.json

# Edit with your API keys
nano config/config.json  # or use your preferred editor
```

## Platform-Specific Instructions

### Windows
```cmd
# Ensure UTF-8 encoding for Arabic support
chcp 65001

# Clone and setup
git clone https://github.com/AliPluss/AION.git
cd AION
python setup_aion_fixed.py
```

### macOS
```bash
# Install Python 3.10+ if needed
brew install python@3.10

# Clone and setup
git clone https://github.com/AliPluss/AION.git
cd AION
python3 setup_aion_fixed.py
```

### Linux (Ubuntu/Debian)
```bash
# Install Python 3.10+ if needed
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip git

# Clone and setup
git clone https://github.com/AliPluss/AION.git
cd AION
python3 setup_aion_fixed.py
```

## Docker Installation (Optional)

### Using Docker Compose
```bash
# Clone repository
git clone https://github.com/AliPluss/AION.git
cd AION

# Start with Docker
docker-compose up -d
```

### Manual Docker Build
```bash
# Build image
docker build -t aion:latest .

# Run container
docker run -it -p 8000:8000 aion:latest
```

## Configuration

### AI Provider Setup
Add your API keys to `config/config.json`:

```json
{
  "ai": {
    "providers": {
      "openai": {
        "api_key": "your-openai-key-here",
        "model": "gpt-4"
      },
      "deepseek": {
        "api_key": "your-deepseek-key-here",
        "model": "deepseek-chat"
      }
    }
  }
}
```

### Environment Variables
Create `.env` file:
```env
OPENAI_API_KEY=your-openai-key
DEEPSEEK_API_KEY=your-deepseek-key
AION_LANGUAGE=ar
AION_DEBUG=false
```

## Verification

### Test Installation
```bash
cd aion_project

# Test basic functionality
python main.py version

# Test interactive mode
python main.py start

# Test AI functionality (requires API key)
python main.py ai
```

### Test Arabic Support
```bash
# Run Arabic support test
python ../test_arabic.py
```

## Troubleshooting

### Common Issues

1. **Python Version Error**:
   ```bash
   # Check Python version
   python --version
   # Should be 3.10 or higher
   ```

2. **Arabic Text Issues**:
   ```bash
   # Windows: Set UTF-8 encoding
   chcp 65001
   
   # Linux/Mac: Check locale
   locale
   export LANG=en_US.UTF-8
   ```

3. **Permission Errors**:
   ```bash
   # Use virtual environment
   python -m venv aion_env
   source aion_env/bin/activate
   ```

4. **Network Issues**:
   ```bash
   # Use proxy if needed
   pip install --proxy http://proxy:port -r requirements.txt
   ```

### Getting Help

- 📧 **Email**: support@aion-ai.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/AliPluss/AION/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/AliPluss/AION/discussions)

## Next Steps

After installation:

1. **Configure AI Providers**: Add your API keys
2. **Set Language**: Choose your preferred interface language
3. **Explore Features**: Try different commands and interfaces
4. **Install Plugins**: Extend functionality with plugins
5. **Read Documentation**: Check README.md for detailed usage

---

**🎉 Welcome to AION! You're ready to start using your AI assistant.**
