#!/bin/bash
# AION - AI Operating Node Unix/Linux/macOS Launcher
# Quick launcher for Unix-based systems

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    if ! command_exists python3; then
        print_color $RED "❌ Python 3 is not installed"
        print_color $YELLOW "Please install Python 3.10 or higher"
        exit 1
    fi
    
    local python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_color $BLUE "🐍 Python version: $python_version"
    
    # Check if version is 3.10 or higher
    local major=$(echo $python_version | cut -d'.' -f1)
    local minor=$(echo $python_version | cut -d'.' -f2)
    
    if [ "$major" -lt 3 ] || ([ "$major" -eq 3 ] && [ "$minor" -lt 10 ]); then
        print_color $RED "❌ Python 3.10 or higher is required"
        print_color $YELLOW "Current version: $python_version"
        exit 1
    fi
}

# Function to show help
show_help() {
    echo
    print_color $CYAN "🤖 AION - AI Operating Node"
    print_color $CYAN "============================"
    echo
    echo "Usage: ./aion.sh [command]"
    echo
    echo "Commands:"
    echo "  setup     - Setup AION (create directories, install dependencies)"
    echo "  install   - Install dependencies only"
    echo "  config    - Setup configuration files"
    echo "  run       - Run AION (default)"
    echo "  web       - Start web interface"
    echo "  help      - Show this help"
    echo
    echo "Examples:"
    echo "  ./aion.sh setup    # First time setup"
    echo "  ./aion.sh          # Run AION"
    echo "  ./aion.sh web      # Start web interface"
    echo
}

# Function to setup AION
setup_aion() {
    print_color $YELLOW "🔧 Setting up AION..."
    
    if python3 run.py setup; then
        print_color $GREEN "✅ Setup completed successfully!"
        echo
        print_color $YELLOW "📝 Next steps:"
        echo "1. Edit ~/.aion/config/ai_config.json to add your API keys"
        echo "2. Run './aion.sh' to start AION"
        echo
    else
        print_color $RED "❌ Setup failed"
        exit 1
    fi
}

# Function to install dependencies
install_dependencies() {
    print_color $YELLOW "📦 Installing dependencies..."
    
    if python3 run.py install; then
        print_color $GREEN "✅ Dependencies installed successfully!"
    else
        print_color $RED "❌ Installation failed"
        exit 1
    fi
}

# Function to setup configuration
setup_config() {
    print_color $YELLOW "📋 Setting up configuration..."
    
    if python3 run.py config; then
        print_color $GREEN "✅ Configuration setup completed!"
    else
        print_color $RED "❌ Configuration setup failed"
        exit 1
    fi
}

# Function to start web interface
start_web() {
    print_color $CYAN "🌐 Starting AION Web Interface..."
    
    if ! [ -f "interfaces/web.py" ]; then
        print_color $RED "❌ Web interface not found"
        exit 1
    fi
    
    python3 -c "
import sys
sys.path.append('.')
from interfaces.web import WebInterface
from utils.translator import Translator

translator = Translator()
web = WebInterface(translator)
web.start()
" || {
        print_color $RED "❌ Failed to start web interface"
        exit 1
    }
}

# Function to run AION
run_aion() {
    print_color $CYAN "🚀 Starting AION..."
    
    if ! [ -f "main.py" ]; then
        print_color $RED "❌ main.py not found"
        print_color $YELLOW "Please make sure you're in the AION directory"
        exit 1
    fi
    
    python3 main.py || {
        print_color $RED "❌ AION exited with error"
        exit 1
    }
}

# Main function
main() {
    # Print header
    echo
    print_color $PURPLE "🤖 AION - AI Operating Node"
    print_color $PURPLE "============================"
    echo
    
    # Check Python version
    check_python_version
    
    # Get script directory
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    cd "$SCRIPT_DIR"
    
    # Parse command line arguments
    COMMAND=${1:-run}
    
    case $COMMAND in
        "help")
            show_help
            ;;
        "setup")
            setup_aion
            ;;
        "install")
            install_dependencies
            ;;
        "config")
            setup_config
            ;;
        "web")
            start_web
            ;;
        "run")
            run_aion
            ;;
        *)
            print_color $RED "❌ Unknown command: $COMMAND"
            show_help
            exit 1
            ;;
    esac
}

# Make sure script is executable
if [ ! -x "$0" ]; then
    print_color $YELLOW "⚠️  Making script executable..."
    chmod +x "$0"
fi

# Run main function
main "$@"
