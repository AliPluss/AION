#!/usr/bin/env python3
"""
🐙 AION GitHub Integration Tools

Professional GitHub integration for AION with repository management,
file synchronization, and collaboration features.

Features:
- Personal access token authentication
- Repository cloning and synchronization
- File push/pull operations
- Branch management
- Issue and PR integration
- Comprehensive logging
"""

import os
import subprocess
import json
import requests
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm

console = Console()

@dataclass
class GitHubConfig:
    """GitHub configuration settings"""
    token: str
    username: str
    default_repo: str = ""
    base_url: str = "https://api.github.com"

@dataclass
class RepositoryInfo:
    """Repository information"""
    name: str
    full_name: str
    description: str
    private: bool
    clone_url: str
    ssh_url: str

class GitHubTools:
    """Professional GitHub integration for AION"""
    
    def __init__(self):
        self.config = self._load_config()
        self.log_file = Path("test_logs/github_tools.log")
        self.log_file.parent.mkdir(exist_ok=True)
        
    def _load_config(self) -> Optional[GitHubConfig]:
        """Load GitHub configuration from environment"""
        try:
            token = os.getenv('AION_GITHUB_TOKEN', '')
            if not token:
                return None
                
            # Get username from GitHub API
            headers = {'Authorization': f'token {token}'}
            response = requests.get('https://api.github.com/user', headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                return GitHubConfig(
                    token=token,
                    username=user_data['login'],
                    default_repo=os.getenv('AION_GITHUB_DEFAULT_REPO', '')
                )
            else:
                console.print(f"❌ [red]GitHub token validation failed: {response.status_code}[/red]")
                return None
                
        except Exception as e:
            console.print(f"❌ [red]GitHub config error: {e}[/red]")
            return None
    
    def _log_github_action(self, action: str, details: Dict[str, Any]):
        """Log GitHub actions to test log file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{timestamp} - {action}: {json.dumps(details, indent=2)}\n")
        except Exception as e:
            console.print(f"⚠️ [yellow]Logging error: {e}[/yellow]")
    
    def github_tools_interactive(self) -> bool:
        """Interactive GitHub tools interface"""
        console.print("\n🐙 [bold yellow]GitHub Integration Tools[/bold yellow]")
        
        if not self.config:
            console.print("❌ [red]GitHub not configured. Please set AION_GITHUB_TOKEN in .env file[/red]")
            console.print("💡 [cyan]Get your token from: https://github.com/settings/tokens[/cyan]")
            self._log_github_action("ACCESS_FAILED", {"error": "GitHub not configured"})
            return False
        
        console.print(f"✅ [green]Connected as: {self.config.username}[/green]")
        
        try:
            console.print("\n🔧 [bold yellow]Available GitHub Tools:[/bold yellow]")
            console.print("1. 📋 List repositories")
            console.print("2. 📤 Push files to repository")
            console.print("3. 📥 Pull repository updates")
            console.print("4. 🌿 Create new branch")
            console.print("5. 📊 Repository statistics")
            
            choice = Prompt.ask("Choose tool", choices=["1", "2", "3", "4", "5"], default="1")
            
            if choice == "1":
                return self._list_repositories()
            elif choice == "2":
                return self._push_files_interactive()
            elif choice == "3":
                return self._pull_updates_interactive()
            elif choice == "4":
                return self._create_branch_interactive()
            elif choice == "5":
                return self._show_repository_stats()
                
        except KeyboardInterrupt:
            console.print("\n🐙 [yellow]GitHub tools cancelled by user[/yellow]")
            return False
        except Exception as e:
            console.print(f"❌ [red]GitHub tools error: {e}[/red]")
            self._log_github_action("TOOLS_ERROR", {"error": str(e)})
            return False
    
    def _list_repositories(self) -> bool:
        """List user repositories"""
        try:
            headers = {'Authorization': f'token {self.config.token}'}
            response = requests.get(f'{self.config.base_url}/user/repos', headers=headers)
            
            if response.status_code == 200:
                repos = response.json()
                
                table = Table(title="📋 Your Repositories")
                table.add_column("Name", style="cyan")
                table.add_column("Description", style="white")
                table.add_column("Private", style="yellow")
                table.add_column("Language", style="green")
                
                for repo in repos[:10]:  # Show first 10 repos
                    table.add_row(
                        repo['name'],
                        repo['description'] or "No description",
                        "🔒" if repo['private'] else "🌐",
                        repo['language'] or "N/A"
                    )
                
                console.print(table)
                
                self._log_github_action("LIST_REPOS_SUCCESS", {
                    "repo_count": len(repos),
                    "username": self.config.username
                })
                return True
            else:
                console.print(f"❌ [red]Failed to fetch repositories: {response.status_code}[/red]")
                return False
                
        except Exception as e:
            console.print(f"❌ [red]Repository listing error: {e}[/red]")
            self._log_github_action("LIST_REPOS_ERROR", {"error": str(e)})
            return False
    
    def _push_files_interactive(self) -> bool:
        """Interactive file pushing to repository"""
        try:
            repo_name = Prompt.ask("📁 [bold cyan]Repository name[/bold cyan]", default=self.config.default_repo)
            if not repo_name:
                console.print("❌ [red]Repository name required[/red]")
                return False
            
            file_path = Prompt.ask("📄 [bold cyan]File path to push[/bold cyan]")
            if not Path(file_path).exists():
                console.print(f"❌ [red]File not found: {file_path}[/red]")
                return False
            
            commit_message = Prompt.ask("💬 [bold cyan]Commit message[/bold cyan]", default="Update from AION")
            
            if Confirm.ask(f"📤 Push {file_path} to {repo_name}?"):
                return self._push_file_to_repo(repo_name, file_path, commit_message)
            else:
                console.print("📤 [yellow]Push cancelled[/yellow]")
                return False
                
        except Exception as e:
            console.print(f"❌ [red]Push error: {e}[/red]")
            self._log_github_action("PUSH_ERROR", {"error": str(e)})
            return False
    
    def _push_file_to_repo(self, repo_name: str, file_path: str, commit_message: str) -> bool:
        """Push file to GitHub repository using git commands"""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("📤 Pushing to GitHub...", total=None)
                
                # Use git commands for file push
                result = subprocess.run([
                    'git', 'add', file_path
                ], capture_output=True, text=True, cwd='.')
                
                if result.returncode == 0:
                    result = subprocess.run([
                        'git', 'commit', '-m', commit_message
                    ], capture_output=True, text=True, cwd='.')
                    
                    if result.returncode == 0:
                        result = subprocess.run([
                            'git', 'push'
                        ], capture_output=True, text=True, cwd='.')
                        
                        if result.returncode == 0:
                            console.print("✅ [green]File pushed successfully![/green]")
                            self._log_github_action("PUSH_SUCCESS", {
                                "repo": repo_name,
                                "file": file_path,
                                "commit": commit_message
                            })
                            return True
                
                console.print(f"❌ [red]Git push failed: {result.stderr}[/red]")
                return False
                
        except Exception as e:
            console.print(f"❌ [red]Push failed: {e}[/red]")
            self._log_github_action("PUSH_FAILED", {"error": str(e), "file": file_path})
            return False
    
    def _pull_updates_interactive(self) -> bool:
        """Interactive repository updates pulling"""
        try:
            if Confirm.ask("📥 Pull latest updates from repository?"):
                result = subprocess.run(['git', 'pull'], capture_output=True, text=True, cwd='.')
                
                if result.returncode == 0:
                    console.print("✅ [green]Repository updated successfully![/green]")
                    console.print(f"📄 [cyan]{result.stdout}[/cyan]")
                    self._log_github_action("PULL_SUCCESS", {"output": result.stdout})
                    return True
                else:
                    console.print(f"❌ [red]Pull failed: {result.stderr}[/red]")
                    return False
            else:
                console.print("📥 [yellow]Pull cancelled[/yellow]")
                return False
                
        except Exception as e:
            console.print(f"❌ [red]Pull error: {e}[/red]")
            self._log_github_action("PULL_ERROR", {"error": str(e)})
            return False
    
    def _create_branch_interactive(self) -> bool:
        """Interactive branch creation"""
        try:
            branch_name = Prompt.ask("🌿 [bold cyan]New branch name[/bold cyan]")
            if not branch_name:
                console.print("❌ [red]Branch name required[/red]")
                return False
            
            if Confirm.ask(f"🌿 Create and switch to branch '{branch_name}'?"):
                result = subprocess.run([
                    'git', 'checkout', '-b', branch_name
                ], capture_output=True, text=True, cwd='.')
                
                if result.returncode == 0:
                    console.print(f"✅ [green]Branch '{branch_name}' created and switched![/green]")
                    self._log_github_action("BRANCH_CREATE_SUCCESS", {"branch": branch_name})
                    return True
                else:
                    console.print(f"❌ [red]Branch creation failed: {result.stderr}[/red]")
                    return False
            else:
                console.print("🌿 [yellow]Branch creation cancelled[/yellow]")
                return False
                
        except Exception as e:
            console.print(f"❌ [red]Branch creation error: {e}[/red]")
            self._log_github_action("BRANCH_ERROR", {"error": str(e)})
            return False
    
    def _show_repository_stats(self) -> bool:
        """Show repository statistics"""
        try:
            headers = {'Authorization': f'token {self.config.token}'}
            response = requests.get(f'{self.config.base_url}/user', headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                
                stats_table = Table(title="📊 GitHub Statistics")
                stats_table.add_column("Metric", style="cyan")
                stats_table.add_column("Value", style="green")
                
                stats_table.add_row("Public Repositories", str(user_data.get('public_repos', 0)))
                stats_table.add_row("Followers", str(user_data.get('followers', 0)))
                stats_table.add_row("Following", str(user_data.get('following', 0)))
                stats_table.add_row("Account Created", user_data.get('created_at', 'Unknown'))
                
                console.print(stats_table)
                
                self._log_github_action("STATS_SUCCESS", {
                    "username": self.config.username,
                    "public_repos": user_data.get('public_repos', 0)
                })
                return True
            else:
                console.print(f"❌ [red]Failed to fetch statistics: {response.status_code}[/red]")
                return False
                
        except Exception as e:
            console.print(f"❌ [red]Statistics error: {e}[/red]")
            self._log_github_action("STATS_ERROR", {"error": str(e)})
            return False

# Global GitHub tools instance
github_tools = GitHubTools()
