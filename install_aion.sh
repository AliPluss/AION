#!/bin/bash

# 📦 AION Setup and Cleanup Script
# This script installs AION from GitHub, cleans unnecessary files, and starts the terminal app

echo "🚀 Cloning AION from GitHub..."
git clone https://github.com/YourUsername/AION.git
cd AION || exit

echo "📦 Installing AION as Python package..."
pip install .

echo "🧹 Cleaning up unnecessary files..."
rm -rf test_logs/ chat_logs/ voice_logs/ __pycache__ *.log *.pyc *.zip 2>/dev/null

echo "📝 Creating .gitignore file..."
cat <<EOL > .gitignore
/chat_logs/
/test_logs/
/voice_logs/
__pycache__/
.env
*.log
*.pyc
*.zip
EOL

echo "▶️ Starting AION terminal..."
python aion_cli.py
