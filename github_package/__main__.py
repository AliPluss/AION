#!/usr/bin/env python3
"""
AION - AI Operating Node
Main entry point for direct module execution
"""

import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def main():
    """Main entry point for python -m aion_ai"""
    try:
        # Try to import and run main application
        from main import app
        
        # If no arguments provided, show help
        if len(sys.argv) == 1:
            print("🤖 AION - AI Operating Node")
            print("Usage: python -m aion_ai [command] [options]")
            print("\nCommands:")
            print("  cli     Start CLI interface")
            print("  tui     Start TUI interface") 
            print("  web     Start web interface")
            print("  --help  Show help")
            return
        
        # Run the main application
        app()
        
    except ImportError as e:
        print(f"❌ Failed to import AION: {e}")
        print("Please ensure AION is properly installed.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running AION: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
