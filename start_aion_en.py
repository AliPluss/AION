#!/usr/bin/env python3
"""
AION (AI Operating Node) - English Startup Script
=================================================

This script provides a simple English-only startup for AION.
It bypasses the language selection and starts directly in English.

Usage:
    python start_aion_en.py
    
Author: AION Development Team
License: MIT
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Main entry point for English AION startup."""

    # Handle command line arguments
    if len(sys.argv) > 1:
        if '--help' in sys.argv or '-h' in sys.argv:
            print("🚀 AION (AI Operating Node) - English Startup")
            print("=" * 45)
            print("Usage: python start_aion_en.py")
            print("")
            print("Options:")
            print("  --help, -h    Show this help message")
            print("  --version     Show version information")
            print("")
            print("Description:")
            print("  Starts AION directly in English mode, bypassing")
            print("  the language selection screen.")
            return

        if '--version' in sys.argv:
            print("AION v2.2.2 - AI Operating Node")
            print("English Direct Startup Script")
            return

    try:
        # Set environment variable for English-only mode
        os.environ['AION_LANGUAGE'] = 'en'
        os.environ['AION_SKIP_LANGUAGE_SELECTION'] = 'true'

        print("🚀 Starting AION in English mode...")
        print("🌐 Language: English (EN)")
        print("🎯 Mode: Direct startup (no language selection)")

        # Import and run AION main
        from aion.main import main as aion_main
        aion_main()

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure AION is properly installed:")
        print("   pip install -e .")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n👋 AION shutdown requested by user")
        sys.exit(0)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("💡 Please check the error logs or report this issue")
        sys.exit(1)

if __name__ == "__main__":
    main()
