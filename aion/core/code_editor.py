"""
📝 AION Advanced Code Editor
Professional code editor with syntax highlighting, analysis, and AI assistance
Features: Multi-language support, real-time analysis, code completion, formatting
"""

import os
import sys
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json
import re

# Optional imports with fallbacks
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.formatters import TerminalFormatter, Terminal256Formatter
    from pygments.util import ClassNotFound
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False

class CodeLanguage(Enum):
    """Supported programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    RUST = "rust"
    CPP = "cpp"
    C = "c"
    JAVA = "java"
    GO = "go"
    PHP = "php"
    RUBY = "ruby"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    CSHARP = "csharp"
    HTML = "html"
    CSS = "css"
    SQL = "sql"
    BASH = "bash"
    POWERSHELL = "powershell"
    JSON = "json"
    YAML = "yaml"
    XML = "xml"
    MARKDOWN = "markdown"
    TEXT = "text"

class EditorMode(Enum):
    """Editor operation modes"""
    VIEW = "view"
    EDIT = "edit"
    ANALYZE = "analyze"
    FORMAT = "format"
    DEBUG = "debug"

class CodeAnalysisType(Enum):
    """Code analysis types"""
    SYNTAX = "syntax"
    STYLE = "style"
    SECURITY = "security"
    PERFORMANCE = "performance"
    COMPLEXITY = "complexity"
    DOCUMENTATION = "documentation"

@dataclass
class CodeFile:
    """Code file data structure"""
    file_id: str
    name: str
    path: Path
    language: CodeLanguage
    content: str
    original_content: str
    modified: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)
    line_count: int = 0
    char_count: int = 0
    size_bytes: int = 0
    encoding: str = "utf-8"
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CodeAnalysis:
    """Code analysis results"""
    analysis_id: str
    file_id: str
    analysis_type: CodeAnalysisType
    timestamp: datetime
    results: Dict[str, Any]
    issues: List[Dict[str, Any]] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    score: float = 0.0
    passed: bool = True

@dataclass
class EditorSession:
    """Editor session data"""
    session_id: str
    files: Dict[str, CodeFile] = field(default_factory=dict)
    active_file: Optional[str] = None
    mode: EditorMode = EditorMode.VIEW
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    total_edits: int = 0
    analyses_performed: int = 0

class AdvancedCodeEditor:
    """
    🚀 Advanced Code Editor System
    
    Professional code editor with:
    - Multi-language syntax highlighting
    - Real-time code analysis
    - AI-powered suggestions
    - Code formatting and linting
    - File management and sessions
    - Integration with AION systems
    - Export and sharing capabilities
    """
    
    def __init__(self):
        # Storage
        self.editor_dir = Path.home() / ".aion" / "editor"
        self.editor_dir.mkdir(parents=True, exist_ok=True)
        
        self.sessions_dir = self.editor_dir / "sessions"
        self.sessions_dir.mkdir(exist_ok=True)
        
        self.temp_dir = self.editor_dir / "temp"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Runtime data
        self.active_session: Optional[EditorSession] = None
        self.sessions: Dict[str, EditorSession] = {}
        self.analyses: Dict[str, CodeAnalysis] = {}
        
        # Language configurations
        self.language_configs = self._load_language_configs()
        
        # Statistics
        self.total_files_edited = 0
        self.total_analyses = 0
        self.total_sessions = 0
        
        print("📝 Advanced Code Editor initialized")
        print(f"   Editor directory: {self.editor_dir}")
        print(f"   Syntax highlighting: {PYGMENTS_AVAILABLE}")
        print(f"   Supported languages: {len(CodeLanguage)}")
    
    def _load_language_configs(self) -> Dict[CodeLanguage, Dict[str, Any]]:
        """Load language-specific configurations"""
        return {
            CodeLanguage.PYTHON: {
                "extensions": [".py", ".pyw", ".pyi"],
                "comment_style": "#",
                "formatter": "black",
                "linter": "flake8",
                "keywords": ["def", "class", "import", "from", "if", "else", "for", "while", "try", "except"],
                "file_template": "#!/usr/bin/env python3\n\"\"\"\nPython script\n\"\"\"\n\n"
            },
            CodeLanguage.JAVASCRIPT: {
                "extensions": [".js", ".jsx", ".mjs"],
                "comment_style": "//",
                "formatter": "prettier",
                "linter": "eslint",
                "keywords": ["function", "const", "let", "var", "if", "else", "for", "while", "class"],
                "file_template": "// JavaScript file\n\n"
            },
            CodeLanguage.TYPESCRIPT: {
                "extensions": [".ts", ".tsx"],
                "comment_style": "//",
                "formatter": "prettier",
                "linter": "tslint",
                "keywords": ["function", "const", "let", "var", "interface", "type", "class", "enum"],
                "file_template": "// TypeScript file\n\n"
            },
            CodeLanguage.RUST: {
                "extensions": [".rs"],
                "comment_style": "//",
                "formatter": "rustfmt",
                "linter": "clippy",
                "keywords": ["fn", "let", "mut", "struct", "enum", "impl", "trait", "use", "mod"],
                "file_template": "// Rust file\n\nfn main() {\n    println!(\"Hello, world!\");\n}\n"
            },
            CodeLanguage.CPP: {
                "extensions": [".cpp", ".cxx", ".cc", ".hpp", ".h"],
                "comment_style": "//",
                "formatter": "clang-format",
                "linter": "cppcheck",
                "keywords": ["#include", "int", "void", "class", "struct", "namespace", "using"],
                "file_template": "#include <iostream>\n\nint main() {\n    std::cout << \"Hello, world!\" << std::endl;\n    return 0;\n}\n"
            },
            CodeLanguage.HTML: {
                "extensions": [".html", ".htm"],
                "comment_style": "<!-- -->",
                "formatter": "prettier",
                "linter": "htmlhint",
                "keywords": ["<!DOCTYPE", "<html>", "<head>", "<body>", "<div>", "<span>"],
                "file_template": "<!DOCTYPE html>\n<html>\n<head>\n    <title>Document</title>\n</head>\n<body>\n    \n</body>\n</html>\n"
            },
            CodeLanguage.CSS: {
                "extensions": [".css", ".scss", ".sass"],
                "comment_style": "/* */",
                "formatter": "prettier",
                "linter": "stylelint",
                "keywords": ["body", "div", "class", "id", "color", "background", "margin", "padding"],
                "file_template": "/* CSS Stylesheet */\n\nbody {\n    margin: 0;\n    padding: 0;\n}\n"
            },
            CodeLanguage.JSON: {
                "extensions": [".json"],
                "comment_style": "",
                "formatter": "jq",
                "linter": "jsonlint",
                "keywords": [],
                "file_template": "{\n    \"name\": \"value\"\n}\n"
            },
            CodeLanguage.MARKDOWN: {
                "extensions": [".md", ".markdown"],
                "comment_style": "<!-- -->",
                "formatter": "prettier",
                "linter": "markdownlint",
                "keywords": ["#", "##", "###", "**", "*", "`", "```"],
                "file_template": "# Document Title\n\nContent goes here.\n"
            },
            CodeLanguage.BASH: {
                "extensions": [".sh", ".bash"],
                "comment_style": "#",
                "formatter": "shfmt",
                "linter": "shellcheck",
                "keywords": ["#!/bin/bash", "if", "then", "else", "fi", "for", "while", "function"],
                "file_template": "#!/bin/bash\n\n# Bash script\n\necho \"Hello, world!\"\n"
            }
        }
    
    def create_session(self, session_name: str = None) -> str:
        """Create new editor session"""
        if session_name is None:
            session_name = f"session_{int(datetime.now().timestamp())}"
        
        session_id = f"editor_{session_name}"
        
        session = EditorSession(
            session_id=session_id
        )
        
        self.sessions[session_id] = session
        self.active_session = session
        self.total_sessions += 1
        
        print(f"📝 Editor session created: {session_id}")
        return session_id
    
    def load_session(self, session_id: str) -> bool:
        """Load existing editor session"""
        if session_id in self.sessions:
            self.active_session = self.sessions[session_id]
            print(f"📂 Editor session loaded: {session_id}")
            return True
        else:
            print(f"❌ Editor session not found: {session_id}")
            return False
    
    def create_file(
        self,
        filename: str,
        language: CodeLanguage = CodeLanguage.TEXT,
        content: str = "",
        use_template: bool = True
    ) -> str:
        """Create new code file"""
        if not self.active_session:
            self.create_session()
        
        file_id = f"file_{int(datetime.now().timestamp())}"
        file_path = self.temp_dir / filename
        
        # Use template if requested and content is empty
        if use_template and not content and language in self.language_configs:
            content = self.language_configs[language]["file_template"]
        
        # Create file object
        code_file = CodeFile(
            file_id=file_id,
            name=filename,
            path=file_path,
            language=language,
            content=content,
            original_content=content,
            line_count=len(content.splitlines()),
            char_count=len(content),
            size_bytes=len(content.encode('utf-8'))
        )
        
        # Add to session
        self.active_session.files[file_id] = code_file
        self.active_session.active_file = file_id
        self.active_session.last_activity = datetime.now()
        
        # Save to disk
        self._save_file_to_disk(code_file)
        
        self.total_files_edited += 1
        
        print(f"📄 File created: {filename}")
        print(f"   Language: {language.value}")
        print(f"   File ID: {file_id}")
        print(f"   Lines: {code_file.line_count}")
        
        return file_id
    
    def open_file(self, file_path: str) -> Optional[str]:
        """Open existing file"""
        if not self.active_session:
            self.create_session()
        
        path = Path(file_path)
        
        if not path.exists():
            print(f"❌ File not found: {file_path}")
            return None
        
        try:
            # Read file content
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Detect language
            language = self._detect_language(path)
            
            # Create file object
            file_id = f"file_{int(datetime.now().timestamp())}"
            
            code_file = CodeFile(
                file_id=file_id,
                name=path.name,
                path=path,
                language=language,
                content=content,
                original_content=content,
                line_count=len(content.splitlines()),
                char_count=len(content),
                size_bytes=path.stat().st_size
            )
            
            # Add to session
            self.active_session.files[file_id] = code_file
            self.active_session.active_file = file_id
            self.active_session.last_activity = datetime.now()
            
            self.total_files_edited += 1
            
            print(f"📂 File opened: {path.name}")
            print(f"   Language: {language.value}")
            print(f"   Size: {code_file.size_bytes} bytes")
            print(f"   Lines: {code_file.line_count}")
            
            return file_id
            
        except Exception as e:
            print(f"❌ Error opening file: {e}")
            return None
    
    def _detect_language(self, file_path: Path) -> CodeLanguage:
        """Detect programming language from file extension"""
        extension = file_path.suffix.lower()
        
        for language, config in self.language_configs.items():
            if extension in config["extensions"]:
                return language
        
        return CodeLanguage.TEXT
    
    def _save_file_to_disk(self, code_file: CodeFile) -> bool:
        """Save file content to disk"""
        try:
            with open(code_file.path, 'w', encoding='utf-8') as f:
                f.write(code_file.content)
            
            code_file.last_modified = datetime.now()
            return True
            
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            return False

    def edit_file(self, file_id: str, new_content: str) -> bool:
        """Edit file content"""
        if not self.active_session or file_id not in self.active_session.files:
            print(f"❌ File not found: {file_id}")
            return False

        code_file = self.active_session.files[file_id]

        # Update content
        code_file.content = new_content
        code_file.modified = True
        code_file.line_count = len(new_content.splitlines())
        code_file.char_count = len(new_content)
        code_file.size_bytes = len(new_content.encode('utf-8'))
        code_file.last_modified = datetime.now()

        # Update session
        self.active_session.total_edits += 1
        self.active_session.last_activity = datetime.now()

        # Save to disk
        success = self._save_file_to_disk(code_file)

        if success:
            print(f"✅ File edited: {code_file.name}")
            print(f"   Lines: {code_file.line_count}")
            print(f"   Characters: {code_file.char_count}")

        return success

    def view_file(self, file_id: str, with_syntax: bool = True, line_numbers: bool = True) -> str:
        """View file content with optional syntax highlighting"""
        if not self.active_session or file_id not in self.active_session.files:
            print(f"❌ File not found: {file_id}")
            return ""

        code_file = self.active_session.files[file_id]
        content = code_file.content

        # Add line numbers if requested
        if line_numbers:
            lines = content.splitlines()
            numbered_lines = []
            for i, line in enumerate(lines, 1):
                numbered_lines.append(f"{i:4d} | {line}")
            content = "\n".join(numbered_lines)

        # Apply syntax highlighting if available and requested
        if with_syntax and PYGMENTS_AVAILABLE and code_file.language != CodeLanguage.TEXT:
            try:
                lexer = get_lexer_by_name(code_file.language.value)
                formatter = Terminal256Formatter(style='monokai')
                highlighted = highlight(code_file.content, lexer, formatter)

                if line_numbers:
                    # Re-add line numbers to highlighted content
                    lines = highlighted.splitlines()
                    numbered_lines = []
                    for i, line in enumerate(lines, 1):
                        numbered_lines.append(f"{i:4d} | {line}")
                    content = "\n".join(numbered_lines)
                else:
                    content = highlighted

            except ClassNotFound:
                pass  # Use original content

        print(f"📄 {code_file.name} ({code_file.language.value})")
        print("=" * 60)
        print(content)
        print("=" * 60)

        return content

    def analyze_code(self, file_id: str, analysis_types: List[CodeAnalysisType] = None) -> Dict[str, CodeAnalysis]:
        """Perform code analysis"""
        if not self.active_session or file_id not in self.active_session.files:
            print(f"❌ File not found: {file_id}")
            return {}

        if analysis_types is None:
            analysis_types = [
                CodeAnalysisType.SYNTAX,
                CodeAnalysisType.STYLE,
                CodeAnalysisType.COMPLEXITY
            ]

        code_file = self.active_session.files[file_id]
        analyses = {}

        print(f"🔍 Analyzing {code_file.name}...")

        for analysis_type in analysis_types:
            analysis_id = f"analysis_{int(datetime.now().timestamp())}_{analysis_type.value}"

            analysis = CodeAnalysis(
                analysis_id=analysis_id,
                file_id=file_id,
                analysis_type=analysis_type,
                timestamp=datetime.now(),
                results={}
            )

            # Perform specific analysis
            if analysis_type == CodeAnalysisType.SYNTAX:
                analysis = self._analyze_syntax(code_file, analysis)
            elif analysis_type == CodeAnalysisType.STYLE:
                analysis = self._analyze_style(code_file, analysis)
            elif analysis_type == CodeAnalysisType.COMPLEXITY:
                analysis = self._analyze_complexity(code_file, analysis)
            elif analysis_type == CodeAnalysisType.SECURITY:
                analysis = self._analyze_security(code_file, analysis)
            elif analysis_type == CodeAnalysisType.PERFORMANCE:
                analysis = self._analyze_performance(code_file, analysis)
            elif analysis_type == CodeAnalysisType.DOCUMENTATION:
                analysis = self._analyze_documentation(code_file, analysis)

            analyses[analysis_type.value] = analysis
            self.analyses[analysis_id] = analysis

            # Display results
            status = "✅ PASSED" if analysis.passed else "❌ FAILED"
            print(f"   {analysis_type.value.title()}: {status} (Score: {analysis.score:.1f}/10)")

            if analysis.issues:
                print(f"   Issues found: {len(analysis.issues)}")
                for issue in analysis.issues[:3]:  # Show first 3 issues
                    print(f"     • {issue.get('message', 'Unknown issue')}")
                if len(analysis.issues) > 3:
                    print(f"     ... and {len(analysis.issues) - 3} more")

        self.active_session.analyses_performed += len(analysis_types)
        self.total_analyses += len(analysis_types)

        return analyses

    def _analyze_syntax(self, code_file: CodeFile, analysis: CodeAnalysis) -> CodeAnalysis:
        """Analyze code syntax"""
        issues = []
        score = 10.0

        try:
            # Basic syntax checks
            if code_file.language == CodeLanguage.PYTHON:
                # Try to compile Python code
                try:
                    compile(code_file.content, code_file.name, 'exec')
                    analysis.results["syntax_valid"] = True
                except SyntaxError as e:
                    issues.append({
                        "type": "syntax_error",
                        "message": f"Syntax error at line {e.lineno}: {e.msg}",
                        "line": e.lineno,
                        "severity": "error"
                    })
                    score -= 5.0
                    analysis.results["syntax_valid"] = False

            elif code_file.language == CodeLanguage.JSON:
                # Try to parse JSON
                try:
                    json.loads(code_file.content)
                    analysis.results["json_valid"] = True
                except json.JSONDecodeError as e:
                    issues.append({
                        "type": "json_error",
                        "message": f"JSON error at line {e.lineno}: {e.msg}",
                        "line": e.lineno,
                        "severity": "error"
                    })
                    score -= 5.0
                    analysis.results["json_valid"] = False

            # Check for common issues
            lines = code_file.content.splitlines()

            # Check for very long lines
            long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 120]
            if long_lines:
                issues.append({
                    "type": "long_lines",
                    "message": f"Lines too long (>120 chars): {long_lines[:5]}",
                    "severity": "warning"
                })
                score -= 0.5

            # Check for trailing whitespace
            trailing_ws_lines = [i+1 for i, line in enumerate(lines) if line.rstrip() != line]
            if trailing_ws_lines:
                issues.append({
                    "type": "trailing_whitespace",
                    "message": f"Trailing whitespace on lines: {trailing_ws_lines[:5]}",
                    "severity": "info"
                })
                score -= 0.2

            analysis.results["total_lines"] = len(lines)
            analysis.results["long_lines_count"] = len(long_lines)
            analysis.results["trailing_whitespace_count"] = len(trailing_ws_lines)

        except Exception as e:
            issues.append({
                "type": "analysis_error",
                "message": f"Analysis error: {str(e)}",
                "severity": "error"
            })
            score = 0.0

        analysis.issues = issues
        analysis.score = max(0.0, score)
        analysis.passed = score >= 7.0

        return analysis

    def _analyze_style(self, code_file: CodeFile, analysis: CodeAnalysis) -> CodeAnalysis:
        """Analyze code style"""
        issues = []
        score = 10.0

        content = code_file.content
        lines = content.splitlines()

        # Check indentation consistency
        indentations = []
        for line in lines:
            if line.strip():  # Skip empty lines
                indent = len(line) - len(line.lstrip())
                if indent > 0:
                    indentations.append(indent)

        if indentations:
            # Check if indentation is consistent
            if code_file.language == CodeLanguage.PYTHON:
                # Python should use 4 spaces
                non_four_space = [i for i in indentations if i % 4 != 0]
                if non_four_space:
                    issues.append({
                        "type": "indentation",
                        "message": "Inconsistent indentation (should be 4 spaces)",
                        "severity": "warning"
                    })
                    score -= 1.0

            # Check for mixed tabs and spaces
            has_tabs = '\t' in content
            has_spaces = any(line.startswith(' ') for line in lines)

            if has_tabs and has_spaces:
                issues.append({
                    "type": "mixed_indentation",
                    "message": "Mixed tabs and spaces for indentation",
                    "severity": "warning"
                })
                score -= 1.5

        # Check naming conventions
        if code_file.language == CodeLanguage.PYTHON:
            # Check for snake_case functions and variables
            function_pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            functions = re.findall(function_pattern, content)

            camelCase_functions = [f for f in functions if re.match(r'[a-z]+[A-Z]', f)]
            if camelCase_functions:
                issues.append({
                    "type": "naming_convention",
                    "message": f"Functions should use snake_case: {camelCase_functions[:3]}",
                    "severity": "info"
                })
                score -= 0.5

        # Check for TODO/FIXME comments
        todo_pattern = r'(TODO|FIXME|XXX|HACK)'
        todos = re.findall(todo_pattern, content, re.IGNORECASE)
        if todos:
            issues.append({
                "type": "todo_comments",
                "message": f"Found {len(todos)} TODO/FIXME comments",
                "severity": "info"
            })

        analysis.issues = issues
        analysis.score = max(0.0, score)
        analysis.passed = score >= 7.0
        analysis.results = {
            "indentation_consistent": len([i for i in issues if i["type"] == "indentation"]) == 0,
            "mixed_indentation": len([i for i in issues if i["type"] == "mixed_indentation"]) > 0,
            "todo_count": len(todos)
        }

        return analysis

    def _analyze_complexity(self, code_file: CodeFile, analysis: CodeAnalysis) -> CodeAnalysis:
        """Analyze code complexity"""
        issues = []
        score = 10.0

        content = code_file.content
        lines = content.splitlines()

        # Calculate basic metrics
        total_lines = len(lines)
        code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
        comment_lines = len([line for line in lines if line.strip().startswith('#')])
        blank_lines = total_lines - code_lines - comment_lines

        # Calculate complexity indicators
        if code_file.language == CodeLanguage.PYTHON:
            # Count control structures
            control_structures = len(re.findall(r'\b(if|elif|else|for|while|try|except|finally|with)\b', content))

            # Count function definitions
            functions = len(re.findall(r'def\s+\w+', content))

            # Count class definitions
            classes = len(re.findall(r'class\s+\w+', content))

            # Estimate cyclomatic complexity
            complexity = control_structures + functions + 1

            if complexity > 20:
                issues.append({
                    "type": "high_complexity",
                    "message": f"High cyclomatic complexity: {complexity}",
                    "severity": "warning"
                })
                score -= 2.0
            elif complexity > 10:
                issues.append({
                    "type": "moderate_complexity",
                    "message": f"Moderate cyclomatic complexity: {complexity}",
                    "severity": "info"
                })
                score -= 0.5

        # Check for very long functions
        if code_file.language in [CodeLanguage.PYTHON, CodeLanguage.JAVASCRIPT]:
            function_pattern = r'(def|function)\s+\w+.*?(?=\n(?:def|function|class|\Z))'
            functions = re.findall(function_pattern, content, re.DOTALL)

            long_functions = [f for f in functions if len(f.splitlines()) > 50]
            if long_functions:
                issues.append({
                    "type": "long_functions",
                    "message": f"Found {len(long_functions)} functions longer than 50 lines",
                    "severity": "warning"
                })
                score -= 1.0

        # Comment ratio
        if code_lines > 0:
            comment_ratio = comment_lines / code_lines
            if comment_ratio < 0.1:  # Less than 10% comments
                issues.append({
                    "type": "low_comments",
                    "message": f"Low comment ratio: {comment_ratio:.1%}",
                    "severity": "info"
                })
                score -= 0.5

        analysis.issues = issues
        analysis.score = max(0.0, score)
        analysis.passed = score >= 6.0
        analysis.results = {
            "total_lines": total_lines,
            "code_lines": code_lines,
            "comment_lines": comment_lines,
            "blank_lines": blank_lines,
            "comment_ratio": comment_lines / max(1, code_lines),
            "estimated_complexity": locals().get('complexity', 0)
        }

        return analysis

    def _analyze_security(self, code_file: CodeFile, analysis: CodeAnalysis) -> CodeAnalysis:
        """Analyze code security"""
        issues = []
        score = 10.0

        content = code_file.content.lower()

        # Security patterns to check
        security_patterns = {
            "hardcoded_password": [r'password\s*=\s*["\'][^"\']+["\']', r'pwd\s*=\s*["\'][^"\']+["\']'],
            "sql_injection": [r'execute\s*\(\s*["\'].*%.*["\']', r'query\s*\(\s*["\'].*\+.*["\']'],
            "command_injection": [r'os\.system\s*\(', r'subprocess\.call\s*\(', r'eval\s*\('],
            "hardcoded_secrets": [r'api_key\s*=\s*["\'][^"\']+["\']', r'secret\s*=\s*["\'][^"\']+["\']'],
            "unsafe_functions": [r'pickle\.loads\s*\(', r'yaml\.load\s*\(', r'exec\s*\(']
        }

        for category, patterns in security_patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    issues.append({
                        "type": category,
                        "message": f"Potential {category.replace('_', ' ')}: {len(matches)} occurrences",
                        "severity": "warning" if category in ["hardcoded_password", "hardcoded_secrets"] else "error"
                    })
                    score -= 2.0 if category in ["sql_injection", "command_injection"] else 1.0

        analysis.issues = issues
        analysis.score = max(0.0, score)
        analysis.passed = score >= 8.0
        analysis.results = {"security_issues_found": len(issues)}

        return analysis

    def _analyze_performance(self, code_file: CodeFile, analysis: CodeAnalysis) -> CodeAnalysis:
        """Analyze code performance"""
        issues = []
        score = 10.0

        content = code_file.content

        # Performance anti-patterns
        if code_file.language == CodeLanguage.PYTHON:
            # Check for inefficient loops
            nested_loops = len(re.findall(r'for.*:\s*\n.*for.*:', content, re.MULTILINE))
            if nested_loops > 3:
                issues.append({
                    "type": "nested_loops",
                    "message": f"Multiple nested loops detected: {nested_loops}",
                    "severity": "warning"
                })
                score -= 1.0

            # Check for string concatenation in loops
            string_concat_in_loop = re.search(r'for.*:\s*\n.*\+=.*["\']', content, re.MULTILINE)
            if string_concat_in_loop:
                issues.append({
                    "type": "string_concatenation",
                    "message": "String concatenation in loop (consider using join())",
                    "severity": "info"
                })
                score -= 0.5

        analysis.issues = issues
        analysis.score = max(0.0, score)
        analysis.passed = score >= 7.0
        analysis.results = {"performance_issues": len(issues)}

        return analysis

    def _analyze_documentation(self, code_file: CodeFile, analysis: CodeAnalysis) -> CodeAnalysis:
        """Analyze code documentation"""
        issues = []
        score = 10.0

        content = code_file.content
        lines = content.splitlines()

        # Check for docstrings in Python
        if code_file.language == CodeLanguage.PYTHON:
            functions = re.findall(r'def\s+(\w+)', content)
            classes = re.findall(r'class\s+(\w+)', content)

            # Check for function docstrings
            functions_with_docstrings = len(re.findall(r'def\s+\w+.*?:\s*\n\s*"""', content, re.DOTALL))
            if functions and functions_with_docstrings < len(functions):
                missing_docstrings = len(functions) - functions_with_docstrings
                issues.append({
                    "type": "missing_docstrings",
                    "message": f"{missing_docstrings} functions missing docstrings",
                    "severity": "info"
                })
                score -= 0.5 * missing_docstrings

        # Check for comments
        comment_lines = len([line for line in lines if line.strip().startswith('#')])
        code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])

        if code_lines > 20 and comment_lines == 0:
            issues.append({
                "type": "no_comments",
                "message": "No comments found in code",
                "severity": "info"
            })
            score -= 1.0

        analysis.issues = issues
        analysis.score = max(0.0, score)
        analysis.passed = score >= 6.0
        analysis.results = {
            "comment_lines": comment_lines,
            "documentation_ratio": comment_lines / max(1, code_lines)
        }

        return analysis

    def format_code(self, file_id: str) -> bool:
        """Format code using appropriate formatter"""
        if not self.active_session or file_id not in self.active_session.files:
            print(f"❌ File not found: {file_id}")
            return False

        code_file = self.active_session.files[file_id]
        language_config = self.language_configs.get(code_file.language, {})
        formatter = language_config.get("formatter")

        if not formatter:
            print(f"⚠️ No formatter available for {code_file.language.value}")
            return False

        try:
            # Save current content to temp file
            temp_file = self.temp_dir / f"temp_format_{file_id}.{code_file.language.value}"
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code_file.content)

            # Run formatter
            if formatter == "black" and code_file.language == CodeLanguage.PYTHON:
                result = subprocess.run(
                    ["python", "-m", "black", "--quiet", str(temp_file)],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    # Read formatted content
                    with open(temp_file, 'r', encoding='utf-8') as f:
                        formatted_content = f.read()

                    # Update file
                    self.edit_file(file_id, formatted_content)
                    print(f"✅ Code formatted with {formatter}")
                    return True
                else:
                    print(f"❌ Formatting failed: {result.stderr}")
                    return False

            else:
                # Basic formatting for other languages
                formatted_content = self._basic_format(code_file.content, code_file.language)
                self.edit_file(file_id, formatted_content)
                print(f"✅ Code formatted (basic)")
                return True

        except Exception as e:
            print(f"❌ Formatting error: {e}")
            return False
        finally:
            # Clean up temp file
            if temp_file.exists():
                temp_file.unlink()

    def _basic_format(self, content: str, language: CodeLanguage) -> str:
        """Basic code formatting"""
        lines = content.splitlines()
        formatted_lines = []

        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            formatted_lines.append(line)

        # Ensure file ends with newline
        formatted_content = "\n".join(formatted_lines)
        if formatted_content and not formatted_content.endswith('\n'):
            formatted_content += '\n'

        return formatted_content

    def save_file(self, file_id: str, file_path: str = None) -> bool:
        """Save file to specified path"""
        if not self.active_session or file_id not in self.active_session.files:
            print(f"❌ File not found: {file_id}")
            return False

        code_file = self.active_session.files[file_id]

        if file_path:
            save_path = Path(file_path)
        else:
            save_path = code_file.path

        try:
            # Ensure directory exists
            save_path.parent.mkdir(parents=True, exist_ok=True)

            # Save file
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(code_file.content)

            # Update file object
            code_file.path = save_path
            code_file.name = save_path.name
            code_file.modified = False
            code_file.last_modified = datetime.now()

            print(f"💾 File saved: {save_path}")
            return True

        except Exception as e:
            print(f"❌ Save error: {e}")
            return False

    def get_file_info(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Get file information"""
        if not self.active_session or file_id not in self.active_session.files:
            return None

        code_file = self.active_session.files[file_id]

        return {
            "file_id": code_file.file_id,
            "name": code_file.name,
            "path": str(code_file.path),
            "language": code_file.language.value,
            "modified": code_file.modified,
            "created_at": code_file.created_at.isoformat(),
            "last_modified": code_file.last_modified.isoformat(),
            "line_count": code_file.line_count,
            "char_count": code_file.char_count,
            "size_bytes": code_file.size_bytes,
            "encoding": code_file.encoding
        }

    def list_files(self) -> List[Dict[str, Any]]:
        """List all files in current session"""
        if not self.active_session:
            return []

        files_info = []
        for file_id, code_file in self.active_session.files.items():
            files_info.append({
                "file_id": file_id,
                "name": code_file.name,
                "language": code_file.language.value,
                "modified": code_file.modified,
                "lines": code_file.line_count,
                "size": code_file.size_bytes,
                "active": file_id == self.active_session.active_file
            })

        return files_info

    def get_statistics(self) -> Dict[str, Any]:
        """Get editor statistics"""
        active_files = len(self.active_session.files) if self.active_session else 0

        return {
            "total_files_edited": self.total_files_edited,
            "total_analyses": self.total_analyses,
            "total_sessions": self.total_sessions,
            "active_session": self.active_session.session_id if self.active_session else None,
            "active_files": active_files,
            "supported_languages": len(CodeLanguage),
            "syntax_highlighting": PYGMENTS_AVAILABLE,
            "editor_directory": str(self.editor_dir)
        }
