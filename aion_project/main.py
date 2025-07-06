#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 AION - AI Operating Node
Main Application File
"""

import os
import sys
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
import typer

# Setup encoding for Arabic support
if sys.platform == "win32":
    os.system('chcp 65001 >nul 2>&1')
    os.environ["PYTHONIOENCODING"] = "utf-8"

console = Console()
app = typer.Typer(rich_markup_mode="rich")

class AIONApp:
    def __init__(self):
        self.config_dir = Path("config")
        self.load_config()
        self.load_language()
    
    def load_config(self):
        """Load configuration"""
        try:
            with open(self.config_dir / "config.json", "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {"app": {"language": "ar"}}
    
    def load_language(self):
        """Load language translations"""
        lang = self.config.get("app", {}).get("language", "ar")
        try:
            with open(self.config_dir / f"lang_{lang}.json", "r", encoding="utf-8") as f:
                self.lang = json.load(f)
        except FileNotFoundError:
            self.lang = {"welcome": "Welcome to AION"}
    
    def show_welcome(self):
        """Show welcome screen"""
        welcome_text = f"""
[bold blue]🧠 AION - AI Operating Node[/bold blue]
[green]{self.lang.get('welcome', 'Welcome to AION')}[/green]
[yellow]Enhanced Terminal Assistant v2.0.0[/yellow]
        """
        
        panel = Panel(
            welcome_text.strip(),
            title="🤖 AION",
            border_style="bright_blue"
        )
        
        console.print(panel)
    
    def show_menu(self):
        """Show main menu"""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("🔢", style="cyan", width=4)
        table.add_column("الوظيفة | Function", style="green", width=25)
        table.add_column("الوصف | Description", style="white", width=35)
        
        menu_items = [
            ("1", "🤖 " + self.lang.get("ai_assistant", "AI Assistant"), "محادثة مع الذكاء الاصطناعي"),
            ("2", "⚡ " + self.lang.get("code_execution", "Code Execution"), "تنفيذ الأكواد البرمجية"),
            ("3", "🎤 " + self.lang.get("voice_mode", "Voice Mode"), "التحكم بالأوامر الصوتية"),
            ("4", "⚙️ " + self.lang.get("settings", "Settings"), "الإعدادات والتخصيص"),
            ("5", "❓ " + self.lang.get("help", "Help"), "المساعدة والدليل"),
            ("0", "🚪 " + self.lang.get("exit", "Exit"), "خروج من البرنامج")
        ]
        
        for num, func, desc in menu_items:
            table.add_row(num, func, desc)
        
        menu_panel = Panel(
            table,
            title="[bold blue]🎯 القائمة الرئيسية | Main Menu[/bold blue]",
            border_style="green"
        )
        
        console.print(menu_panel)
    
    def run(self):
        """Run the main application"""
        self.show_welcome()
        
        while True:
            console.print()
            self.show_menu()
            
            choice = Prompt.ask(
                "\n[cyan]اختر رقم الوظيفة | Select function number[/cyan]",
                choices=["0", "1", "2", "3", "4", "5"],
                default="1"
            )
            
            if choice == "0":
                console.print("\n[green]🙏 شكراً لاستخدام AION! | Thank you for using AION![/green]")
                break
            elif choice == "1":
                console.print("\n[yellow]🤖 بدء مساعد الذكاء الاصطناعي...[/yellow]")
                console.print("[dim]⚠️ هذه الميزة قيد التطوير | This feature is under development[/dim]")
            elif choice == "2":
                console.print("\n[yellow]⚡ بدء تنفيذ الكود...[/yellow]")
                console.print("[dim]⚠️ هذه الميزة قيد التطوير | This feature is under development[/dim]")
            elif choice == "3":
                console.print("\n[yellow]🎤 بدء الوضع الصوتي...[/yellow]")
                console.print("[dim]⚠️ هذه الميزة قيد التطوير | This feature is under development[/dim]")
            elif choice == "4":
                console.print("\n[yellow]⚙️ فتح الإعدادات...[/yellow]")
                console.print("[dim]⚠️ هذه الميزة قيد التطوير | This feature is under development[/dim]")
            elif choice == "5":
                self.show_help()
    
    def show_help(self):
        """Show help information"""
        help_text = """
[bold blue]🧠 AION - دليل المساعدة | Help Guide[/bold blue]

[green]الوظائف المتاحة | Available Functions:[/green]
• مساعد الذكاء الاصطناعي - محادثة ذكية مع AI
• تنفيذ الكود - تشغيل أكواد متعددة اللغات  
• الوضع الصوتي - التحكم بالأوامر الصوتية
• الإعدادات - تخصيص النظام حسب احتياجاتك

[yellow]للمزيد من المعلومات، قم بزيارة الوثائق الرسمية[/yellow]
        """
        
        help_panel = Panel(
            help_text.strip(),
            title="[bold blue]❓ المساعدة | Help[/bold blue]",
            border_style="yellow"
        )
        
        console.print(help_panel)

@app.command()
def start():
    """🚀 Start AION interactive mode"""
    aion_app = AIONApp()
    aion_app.run()

@app.command()
def ai():
    """🤖 Quick AI assistant"""
    console.print("\n[yellow]🤖 بدء مساعد الذكاء الاصطناعي...[/yellow]")
    console.print("[dim]⚠️ هذه الميزة قيد التطوير | This feature is under development[/dim]")

@app.command()
def version():
    """📋 Show version information"""
    console.print("[bold blue]🧠 AION v2.0.0[/bold blue]")
    console.print("[green]AI Operating Node - Enhanced Terminal Assistant[/green]")

if __name__ == "__main__":
    app()
