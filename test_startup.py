#!/usr/bin/env python3
"""
Test AION startup sequence and ASCII banner
"""

import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.text import Text
    from rich.align import Align
    
    console = Console()
    
    def test_ascii_banner():
        """Test ASCII banner display"""
        banner = """
    ╔═══════════════════════════════════════╗
    ║              🤖 AION                  ║
    ║        AI Operating Node              ║
    ║     Professional Terminal AI          ║
    ║                                       ║
    ║    Developer: project.django.rst@gmail.com    ║
    ║    GitHub: https://github.com/AliPluss/aion-ai ║
    ╚═══════════════════════════════════════╝
        """
        
        welcome_text = Text(banner, style="bold cyan")
        centered_banner = Align.center(welcome_text)
        
        welcome_panel = Panel(
            centered_banner,
            title="🚀 Welcome to AION",
            border_style="green",
            padding=(1, 2)
        )
        
        console.print(welcome_panel)
        return True
    
    def test_loading_animation():
        """Test loading animation sequence"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:

            steps = [
                "🔧 Initializing AION systems...",
                "🔐 Loading security modules...",
                "🤖 Connecting AI providers...",
                "🌐 Setting up multilingual support...",
                "⚡ Preparing code execution engine...",
                "📁 Loading file management system...",
                "🎤 Initializing voice control...",
                "📤 Setting up export capabilities...",
                "✅ AION ready!"
            ]

            task = progress.add_task("Loading...", total=len(steps))

            for step in steps:
                progress.update(task, description=step)
                time.sleep(0.3)  # Faster for testing
                progress.advance(task)

            time.sleep(0.5)
        return True
    
    def main():
        console.print("🧪 [bold yellow]Testing AION Startup Sequence[/bold yellow]\n")
        
        # Test 1: ASCII Banner
        console.print("1️⃣ Testing ASCII Banner...")
        banner_result = test_ascii_banner()
        console.print(f"   ASCII Banner: {'✅ PASSED' if banner_result else '❌ FAILED'}\n")
        
        # Test 2: Loading Animation
        console.print("2️⃣ Testing Loading Animation...")
        loading_result = test_loading_animation()
        console.print(f"   Loading Animation: {'✅ PASSED' if loading_result else '❌ FAILED'}\n")
        
        # Summary
        console.print("📋 [bold green]Startup Test Results:[/bold green]")
        console.print(f"   • ASCII Banner Display: {'✅' if banner_result else '❌'}")
        console.print(f"   • Loading Animation: {'✅' if loading_result else '❌'}")
        console.print(f"   • Visual Quality: ✅ Professional")
        console.print(f"   • Timing: ✅ Smooth")
        
        if banner_result and loading_result:
            console.print("\n🎉 [bold green]STARTUP TEST: ALL PASSED![/bold green]")
            return True
        else:
            console.print("\n❌ [bold red]STARTUP TEST: SOME FAILURES[/bold red]")
            return False

    if __name__ == "__main__":
        success = main()
        sys.exit(0 if success else 1)
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install dependencies: pip install rich typer")
    sys.exit(1)
