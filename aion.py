#!/usr/bin/env python3
"""
AION - AI Operating Node
Simple launcher for the interactive TUI
"""

import sys
import os
from pathlib import Path

def main():
    """Main entry point for AION"""
    print("🤖 AION - AI Operating Node")
    print("🚀 Starting Interactive Terminal Assistant...")
    print()
    
    try:
        # Import and start TUI
        from aion_tui import main as tui_main
        tui_main()
        
    except ImportError as e:
        print("❌ Required dependencies not found!")
        print()
        print("📦 Please install required packages:")
        print("   pip install textual rich")
        print()
        print("🔧 Or install AION with dependencies:")
        print("   pip install .")
        print()
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n👋 AION session ended by user")
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Error starting AION: {e}")
        print()
        print("💡 Troubleshooting:")
        print("   • Check your Python version (3.10+ required)")
        print("   • Ensure all dependencies are installed")
        print("   • Try running: python aion_tui.py directly")
        print()
        sys.exit(1)

if __name__ == "__main__":
    main()
