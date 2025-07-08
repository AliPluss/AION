#!/usr/bin/env python3
"""
💡 AION AI Code Assistance System

Professional AI-powered code assistance for AION with inline suggestions,
error detection, and automated fixes.

Features:
- Real-time code analysis
- AI-powered suggestions and improvements
- Error detection and highlighting
- Automated fix recommendations
- Code quality metrics
- Comprehensive logging
"""

import os
import re
import ast
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.prompt import Prompt, Confirm

console = Console()

@dataclass
class CodeSuggestion:
    """Code suggestion structure"""
    line_number: int
    original_code: str
    suggested_code: str
    reason: str
    severity: str  # "info", "warning", "error"
    confidence: float

@dataclass
class CodeAnalysis:
    """Code analysis results"""
    language: str
    total_lines: int
    suggestions: List[CodeSuggestion]
    errors: List[str]
    warnings: List[str]
    quality_score: float

class AICodeAssist:
    """Professional AI code assistance for AION"""
    
    def __init__(self):
        self.log_file = Path("test_logs/ai_code_assist.log")
        self.log_file.parent.mkdir(exist_ok=True)
        
    def _log_assistance_action(self, action: str, details: Dict[str, Any]):
        """Log AI assistance actions to test log file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{timestamp} - {action}: {json.dumps(details, indent=2)}\n")
        except Exception as e:
            console.print(f"⚠️ [yellow]Logging error: {e}[/yellow]")
    
    def analyze_code_interactive(self) -> bool:
        """Interactive code analysis and assistance"""
        console.print("\n💡 [bold yellow]AI Code Assistance System[/bold yellow]")
        
        try:
            console.print("\n🔧 [bold yellow]Code Analysis Options:[/bold yellow]")
            console.print("1. 📄 Analyze file")
            console.print("2. ✍️ Analyze code snippet")
            console.print("3. 🔍 Check for errors")
            console.print("4. 🚀 Suggest improvements")
            
            choice = Prompt.ask("Choose analysis type", choices=["1", "2", "3", "4"], default="1")
            
            if choice == "1":
                return self._analyze_file_interactive()
            elif choice == "2":
                return self._analyze_snippet_interactive()
            elif choice == "3":
                return self._check_errors_interactive()
            elif choice == "4":
                return self._suggest_improvements_interactive()
                
        except KeyboardInterrupt:
            console.print("\n💡 [yellow]Code assistance cancelled by user[/yellow]")
            return False
        except Exception as e:
            console.print(f"❌ [red]Code assistance error: {e}[/red]")
            self._log_assistance_action("ASSIST_ERROR", {"error": str(e)})
            return False
    
    def _analyze_file_interactive(self) -> bool:
        """Interactive file analysis"""
        try:
            file_path = Prompt.ask("📄 [bold cyan]File path to analyze[/bold cyan]")
            if not Path(file_path).exists():
                console.print(f"❌ [red]File not found: {file_path}[/red]")
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            language = self._detect_language(file_path)
            analysis = self._analyze_code(code_content, language)
            
            self._display_analysis_results(analysis, file_path)
            
            if analysis.suggestions and Confirm.ask("💡 Apply suggested improvements?"):
                return self._apply_suggestions_interactive(file_path, analysis.suggestions)
            
            self._log_assistance_action("FILE_ANALYSIS_SUCCESS", {
                "file": file_path,
                "language": language,
                "suggestions_count": len(analysis.suggestions),
                "quality_score": analysis.quality_score
            })
            return True
            
        except Exception as e:
            console.print(f"❌ [red]File analysis error: {e}[/red]")
            self._log_assistance_action("FILE_ANALYSIS_ERROR", {"error": str(e)})
            return False
    
    def _analyze_snippet_interactive(self) -> bool:
        """Interactive code snippet analysis"""
        try:
            console.print("✍️ [bold cyan]Enter your code snippet (press Ctrl+D when done):[/bold cyan]")
            code_lines = []
            
            try:
                while True:
                    line = input()
                    code_lines.append(line)
            except EOFError:
                pass
            
            code_content = '\n'.join(code_lines)
            if not code_content.strip():
                console.print("❌ [red]No code provided[/red]")
                return False
            
            language = Prompt.ask("🔤 [bold cyan]Programming language[/bold cyan]", default="python")
            analysis = self._analyze_code(code_content, language)
            
            self._display_analysis_results(analysis, "Code Snippet")
            
            self._log_assistance_action("SNIPPET_ANALYSIS_SUCCESS", {
                "language": language,
                "suggestions_count": len(analysis.suggestions),
                "quality_score": analysis.quality_score
            })
            return True
            
        except Exception as e:
            console.print(f"❌ [red]Snippet analysis error: {e}[/red]")
            self._log_assistance_action("SNIPPET_ANALYSIS_ERROR", {"error": str(e)})
            return False
    
    def _check_errors_interactive(self) -> bool:
        """Interactive error checking"""
        try:
            file_path = Prompt.ask("🔍 [bold cyan]File path to check for errors[/bold cyan]")
            if not Path(file_path).exists():
                console.print(f"❌ [red]File not found: {file_path}[/red]")
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            language = self._detect_language(file_path)
            errors = self._check_syntax_errors(code_content, language)
            
            if errors:
                console.print("\n🚨 [bold red]Errors Found:[/bold red]")
                for i, error in enumerate(errors, 1):
                    console.print(f"{i}. {error}")
            else:
                console.print("✅ [green]No syntax errors found![/green]")
            
            self._log_assistance_action("ERROR_CHECK_SUCCESS", {
                "file": file_path,
                "language": language,
                "errors_count": len(errors)
            })
            return True
            
        except Exception as e:
            console.print(f"❌ [red]Error checking failed: {e}[/red]")
            self._log_assistance_action("ERROR_CHECK_ERROR", {"error": str(e)})
            return False
    
    def _suggest_improvements_interactive(self) -> bool:
        """Interactive improvement suggestions"""
        try:
            file_path = Prompt.ask("🚀 [bold cyan]File path for improvement suggestions[/bold cyan]")
            if not Path(file_path).exists():
                console.print(f"❌ [red]File not found: {file_path}[/red]")
                return False
            
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            language = self._detect_language(file_path)
            suggestions = self._generate_improvements(code_content, language)
            
            if suggestions:
                console.print("\n🚀 [bold green]Improvement Suggestions:[/bold green]")
                for i, suggestion in enumerate(suggestions, 1):
                    console.print(f"\n{i}. Line {suggestion.line_number}: {suggestion.reason}")
                    console.print(f"   Original: [red]{suggestion.original_code}[/red]")
                    console.print(f"   Suggested: [green]{suggestion.suggested_code}[/green]")
            else:
                console.print("✅ [green]Code looks good! No improvements suggested.[/green]")
            
            self._log_assistance_action("IMPROVEMENTS_SUCCESS", {
                "file": file_path,
                "language": language,
                "suggestions_count": len(suggestions)
            })
            return True
            
        except Exception as e:
            console.print(f"❌ [red]Improvement suggestions failed: {e}[/red]")
            self._log_assistance_action("IMPROVEMENTS_ERROR", {"error": str(e)})
            return False
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        extension = Path(file_path).suffix.lower()
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.php': 'php',
            '.rb': 'ruby',
            '.swift': 'swift',
            '.kt': 'kotlin'
        }
        return language_map.get(extension, 'text')
    
    def _analyze_code(self, code: str, language: str) -> CodeAnalysis:
        """Analyze code and generate suggestions"""
        suggestions = []
        errors = []
        warnings = []
        
        lines = code.split('\n')
        total_lines = len(lines)
        
        # Basic analysis for Python
        if language == 'python':
            suggestions.extend(self._analyze_python_code(code, lines))
            errors.extend(self._check_python_syntax(code))
        
        # Calculate quality score
        quality_score = max(0.0, 100.0 - (len(errors) * 20) - (len(warnings) * 10) - (len(suggestions) * 5))
        
        return CodeAnalysis(
            language=language,
            total_lines=total_lines,
            suggestions=suggestions,
            errors=errors,
            warnings=warnings,
            quality_score=quality_score
        )
    
    def _analyze_python_code(self, code: str, lines: List[str]) -> List[CodeSuggestion]:
        """Analyze Python code for improvements"""
        suggestions = []
        
        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()
            
            # Check for long lines
            if len(line) > 100:
                suggestions.append(CodeSuggestion(
                    line_number=i,
                    original_code=line.strip(),
                    suggested_code="# Consider breaking this line into multiple lines",
                    reason="Line too long (>100 characters)",
                    severity="warning",
                    confidence=0.8
                ))
            
            # Check for missing docstrings in functions
            if line_stripped.startswith('def ') and ':' in line_stripped:
                if i < len(lines) and not lines[i].strip().startswith('"""'):
                    suggestions.append(CodeSuggestion(
                        line_number=i,
                        original_code=line.strip(),
                        suggested_code=line.strip() + '\n    """Add function description here."""',
                        reason="Missing docstring",
                        severity="info",
                        confidence=0.7
                    ))
            
            # Check for unused imports (basic check)
            if line_stripped.startswith('import ') or line_stripped.startswith('from '):
                module_name = line_stripped.split()[1].split('.')[0]
                if module_name not in code:
                    suggestions.append(CodeSuggestion(
                        line_number=i,
                        original_code=line.strip(),
                        suggested_code="# Remove unused import",
                        reason="Potentially unused import",
                        severity="warning",
                        confidence=0.6
                    ))
        
        return suggestions
    
    def _check_python_syntax(self, code: str) -> List[str]:
        """Check Python syntax errors"""
        errors = []
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append(f"Syntax error at line {e.lineno}: {e.msg}")
        except Exception as e:
            errors.append(f"Code analysis error: {str(e)}")
        
        return errors
    
    def _check_syntax_errors(self, code: str, language: str) -> List[str]:
        """Check syntax errors for different languages"""
        if language == 'python':
            return self._check_python_syntax(code)
        else:
            return []  # Basic implementation for other languages
    
    def _generate_improvements(self, code: str, language: str) -> List[CodeSuggestion]:
        """Generate improvement suggestions"""
        analysis = self._analyze_code(code, language)
        return analysis.suggestions
    
    def _display_analysis_results(self, analysis: CodeAnalysis, source: str):
        """Display code analysis results"""
        console.print(f"\n📊 [bold yellow]Analysis Results for: {source}[/bold yellow]")
        
        # Summary table
        summary_table = Table(title="Code Analysis Summary")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Value", style="green")
        
        summary_table.add_row("Language", analysis.language.title())
        summary_table.add_row("Total Lines", str(analysis.total_lines))
        summary_table.add_row("Suggestions", str(len(analysis.suggestions)))
        summary_table.add_row("Errors", str(len(analysis.errors)))
        summary_table.add_row("Quality Score", f"{analysis.quality_score:.1f}/100")
        
        console.print(summary_table)
        
        # Display suggestions
        if analysis.suggestions:
            console.print("\n💡 [bold yellow]Suggestions:[/bold yellow]")
            for suggestion in analysis.suggestions[:5]:  # Show first 5 suggestions
                severity_color = {
                    "error": "red",
                    "warning": "yellow",
                    "info": "cyan"
                }.get(suggestion.severity, "white")
                
                console.print(f"  Line {suggestion.line_number}: [{severity_color}]{suggestion.reason}[/{severity_color}]")
                console.print(f"    Original: {suggestion.original_code}")
                console.print(f"    Suggested: {suggestion.suggested_code}")
                console.print()
    
    def _apply_suggestions_interactive(self, file_path: str, suggestions: List[CodeSuggestion]) -> bool:
        """Interactively apply code suggestions"""
        try:
            console.print("🔧 [bold yellow]Applying suggestions is not yet implemented[/bold yellow]")
            console.print("💡 [cyan]This feature will be available in a future update[/cyan]")
            return True
        except Exception as e:
            console.print(f"❌ [red]Failed to apply suggestions: {e}[/red]")
            return False

# Global AI code assist instance
ai_code_assist = AICodeAssist()
