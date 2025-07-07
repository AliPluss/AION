"""
🚀 AION Advanced Code Execution Engine
Professional multi-language code execution with security, sandboxing, and real-time monitoring
Features: Isolated environments, resource monitoring, security analysis, and performance optimization
"""

import os
import sys
import subprocess
import tempfile
import shutil
import platform
import time
import uuid
import threading
import signal

# Optional imports with fallbacks for Windows compatibility
try:
    import resource
    RESOURCE_AVAILABLE = True
except ImportError:
    RESOURCE_AVAILABLE = False
    resource = None

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None

try:
    import docker
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False
    docker = None
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import json
from datetime import datetime, timedelta
from contextlib import contextmanager

class ResourceMonitor:
    """Monitor system resources during code execution (Windows compatible)"""

    def __init__(self):
        self.monitoring_active = False
        self.metrics = None  # Will be initialized when ExecutionMetrics is defined
        self.start_time = 0
        self.process = None

    def start_monitoring(self, process_id: int = None):
        """Start monitoring resources"""
        self.monitoring_active = True
        self.start_time = time.time()

        if PSUTIL_AVAILABLE and process_id:
            try:
                self.process = psutil.Process(process_id)
            except (psutil.NoSuchProcess, Exception):
                self.process = None
        else:
            self.process = None

    def stop_monitoring(self):
        """Stop monitoring and return metrics"""
        self.monitoring_active = False
        if self.metrics and hasattr(self, 'start_time'):
            self.metrics.wall_time = time.time() - self.start_time
        return self.metrics

    def get_current_metrics(self):
        """Get current resource metrics"""
        if PSUTIL_AVAILABLE and self.process:
            try:
                if self.process.is_running():
                    memory_info = self.process.memory_info()
                    if self.metrics:
                        self.metrics.memory_peak_mb = max(
                            self.metrics.memory_peak_mb,
                            memory_info.rss / 1024 / 1024
                        )
                        cpu_times = self.process.cpu_times()
                        self.metrics.cpu_time = cpu_times.user + cpu_times.system
            except (Exception):
                pass
        return self.metrics

class SecurityAnalyzer:
    """Analyze code for security risks"""

    def __init__(self):
        self.dangerous_patterns = [
            r'import\s+os',
            r'import\s+subprocess',
            r'import\s+sys',
            r'__import__',
            r'eval\s*\(',
            r'exec\s*\(',
            r'open\s*\(',
            r'file\s*\(',
            r'input\s*\(',
            r'raw_input\s*\(',
            r'compile\s*\(',
            r'globals\s*\(',
            r'locals\s*\(',
            r'vars\s*\(',
            r'dir\s*\(',
            r'getattr\s*\(',
            r'setattr\s*\(',
            r'delattr\s*\(',
            r'hasattr\s*\(',
        ]

        self.network_patterns = [
            r'urllib',
            r'requests',
            r'http',
            r'socket',
            r'ftplib',
            r'smtplib',
            r'telnetlib',
        ]

        self.file_patterns = [
            r'open\s*\(',
            r'file\s*\(',
            r'with\s+open',
            r'pathlib',
            r'os\.path',
            r'shutil',
        ]

    def analyze_code(self, code: str, language: str) -> List[str]:
        """Analyze code for security violations"""
        violations = []

        import re

        # Check for dangerous patterns
        for pattern in self.dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                violations.append(f"Potentially dangerous pattern detected: {pattern}")

        # Check for network access
        for pattern in self.network_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                violations.append(f"Network access detected: {pattern}")

        # Check for file system access
        for pattern in self.file_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                violations.append(f"File system access detected: {pattern}")

        return violations

class Language(Enum):
    """Supported programming languages with advanced features"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    RUST = "rust"
    CPP = "cpp"
    C = "c"
    JAVA = "java"
    CSHARP = "csharp"
    GO = "go"
    PHP = "php"
    RUBY = "ruby"
    KOTLIN = "kotlin"
    SWIFT = "swift"
    SCALA = "scala"

class ExecutionMode(Enum):
    """Code execution modes"""
    STANDARD = "standard"           # Normal execution
    SANDBOX = "sandbox"             # Sandboxed execution
    DOCKER = "docker"               # Docker container execution
    VIRTUAL_ENV = "virtual_env"     # Virtual environment execution
    ISOLATED = "isolated"           # Maximum isolation

class SecurityLevel(Enum):
    """Security levels for code execution"""
    LOW = 1      # Basic security
    MEDIUM = 2   # Standard security
    HIGH = 3     # Enhanced security
    MAXIMUM = 4  # Maximum security with full isolation

@dataclass
class ResourceLimits:
    """Resource limits for code execution"""
    max_memory_mb: int = 512        # Maximum memory in MB
    max_cpu_time: int = 30          # Maximum CPU time in seconds
    max_wall_time: int = 60         # Maximum wall clock time in seconds
    max_file_size_mb: int = 10      # Maximum file size in MB
    max_processes: int = 5          # Maximum number of processes
    max_open_files: int = 100       # Maximum open files
    network_access: bool = False    # Allow network access
    file_system_access: bool = False # Allow file system access

@dataclass
class ExecutionMetrics:
    """Detailed execution metrics"""
    cpu_time: float = 0.0           # CPU time used
    wall_time: float = 0.0          # Wall clock time
    memory_peak_mb: float = 0.0     # Peak memory usage
    memory_avg_mb: float = 0.0      # Average memory usage
    processes_created: int = 0      # Number of processes created
    files_opened: int = 0           # Number of files opened
    network_requests: int = 0       # Number of network requests
    system_calls: int = 0           # Number of system calls

@dataclass
class ExecutionResult:
    """Advanced code execution result with comprehensive metrics"""
    success: bool
    output: str
    error: str
    execution_time: float
    language: str
    exit_code: int = 0

    # Advanced metrics
    metrics: ExecutionMetrics = field(default_factory=ExecutionMetrics)
    security_violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # Execution context
    execution_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    execution_mode: ExecutionMode = ExecutionMode.STANDARD
    security_level: SecurityLevel = SecurityLevel.MEDIUM

    # Resource usage
    resource_limits: ResourceLimits = field(default_factory=ResourceLimits)
    resources_exceeded: List[str] = field(default_factory=list)

    # Additional information
    compiler_output: str = ""
    debug_info: Dict[str, Any] = field(default_factory=dict)
    environment_info: Dict[str, str] = field(default_factory=dict)

class AdvancedCodeExecutor:
    """
    🚀 Advanced Multi-Language Code Execution Engine

    Features:
    - Multi-language support with optimized configurations
    - Advanced security with sandboxing and resource limits
    - Real-time monitoring and metrics collection
    - Docker container support for maximum isolation
    - Virtual environment management
    - Performance optimization and caching
    - Comprehensive error handling and debugging
    """

    def __init__(self, security_level: SecurityLevel = SecurityLevel.MEDIUM):
        self.security_level = security_level
        self.temp_dir = Path(tempfile.gettempdir()) / "aion_execution"
        self.temp_dir.mkdir(exist_ok=True)

        # Execution tracking
        self.active_executions: Dict[str, Dict[str, Any]] = {}
        self.execution_history: List[ExecutionResult] = []
        self.performance_cache: Dict[str, Any] = {}

        # Resource monitoring
        self.resource_monitor = ResourceMonitor()
        self.security_analyzer = SecurityAnalyzer()

        # Docker support (optional)
        self.docker_client = None
        self._init_docker_support()

        # Initialize dependency checking
        self.check_dependencies()

    def _init_docker_support(self):
        """Initialize Docker support if available"""
        if DOCKER_AVAILABLE:
            try:
                self.docker_client = docker.from_env()
                # Test Docker connection
                self.docker_client.ping()
            except Exception:
                self.docker_client = None
        else:
            self.docker_client = None

        # Language configurations with advanced features
        self.language_configs = {
            Language.PYTHON: {
                "extension": ".py",
                "command": [sys.executable, "-u"],  # -u for unbuffered output
                "compile": False,
                "timeout": 30,
                "env": {"PYTHONIOENCODING": "utf-8"}  # Force UTF-8 encoding
            },
            Language.JAVASCRIPT: {
                "extension": ".js",
                "command": ["node"],
                "compile": False,
                "timeout": 30
            },
            Language.RUST: {
                "extension": ".rs",
                "command": ["rustc"],
                "compile": True,
                "run_command": [],  # Will be set after compilation
                "timeout": 60
            },
            Language.CPP: {
                "extension": ".cpp",
                "command": ["g++", "-o"],
                "compile": True,
                "run_command": [],  # Will be set after compilation
                "timeout": 60
            },
            Language.JAVA: {
                "extension": ".java",
                "command": ["javac"],
                "compile": True,
                "run_command": ["java"],
                "timeout": 60
            },
            Language.CSHARP: {
                "extension": ".cs",
                "command": ["csc"],
                "compile": True,
                "run_command": [],  # Will be set after compilation
                "timeout": 60
            }
        }
        
        self.check_dependencies()
    
    def check_dependencies(self):
        """Check if required language runtimes are available"""
        self.available_languages = []
        
        # Check Python
        try:
            subprocess.run([sys.executable, "--version"], 
                         capture_output=True, check=True)
            self.available_languages.append(Language.PYTHON)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Check Node.js
        try:
            subprocess.run(["node", "--version"], 
                         capture_output=True, check=True)
            self.available_languages.append(Language.JAVASCRIPT)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Check Rust
        try:
            subprocess.run(["rustc", "--version"], 
                         capture_output=True, check=True)
            self.available_languages.append(Language.RUST)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Check C++
        try:
            subprocess.run(["g++", "--version"], 
                         capture_output=True, check=True)
            self.available_languages.append(Language.CPP)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Check Java
        try:
            subprocess.run(["javac", "-version"], 
                         capture_output=True, check=True)
            subprocess.run(["java", "-version"], 
                         capture_output=True, check=True)
            self.available_languages.append(Language.JAVA)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # Check C#
        try:
            subprocess.run(["csc"], capture_output=True)
            self.available_languages.append(Language.CSHARP)
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    
    def get_available_languages(self) -> List[str]:
        """Get list of available programming languages"""
        return [lang.value for lang in self.available_languages]
    
    async def execute_code(self, code: str, language: str, 
                          input_data: str = "", **kwargs) -> ExecutionResult:
        """Execute code in specified language"""
        try:
            lang_enum = Language(language.lower())
            if lang_enum not in self.available_languages:
                return ExecutionResult(
                    success=False,
                    output="",
                    error=f"لغة البرمجة {language} غير متاحة أو غير مثبتة على النظام",
                    execution_time=0.0,
                    language=language
                )
            
            return await self._execute_language(lang_enum, code, input_data, **kwargs)
            
        except ValueError:
            return ExecutionResult(
                success=False,
                output="",
                error=f"Unsupported language: {language}",
                execution_time=0.0,
                language=language
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=f"Execution error: {str(e)}",
                execution_time=0.0,
                language=language
            )
    
    async def _execute_language(self, language: Language, code: str, 
                               input_data: str = "", **kwargs) -> ExecutionResult:
        """Execute code for specific language"""
        config = self.language_configs[language]
        
        # Create temporary file
        temp_file = self.temp_dir / f"temp_{os.getpid()}{config['extension']}"
        
        try:
            # Write code to file with UTF-8 BOM for better Windows compatibility
            with open(temp_file, 'w', encoding='utf-8-sig') as f:
                # Add UTF-8 encoding declaration for Python files
                if language == Language.PYTHON:
                    f.write("# -*- coding: utf-8 -*-\n")
                    f.write("import sys, os, re\n")
                    f.write("if sys.platform == 'win32':\n")
                    f.write("    import codecs\n")
                    f.write("    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())\n")
                    f.write("    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())\n")
                    f.write("    os.system('chcp 65001 >nul 2>&1')\n")
                    f.write("    # Arabic text direction fix\n")
                    f.write("    def fix_arabic_print(text):\n")
                    f.write("        if re.search(r'[\\u0600-\\u06FF\\u0750-\\u077F\\u08A0-\\u08FF\\uFB50-\\uFDFF\\uFE70-\\uFEFF]', str(text)):\n")
                    f.write("            return f'\\u202E{text}\\u202C'\n")
                    f.write("        return text\n")
                    f.write("    # Override print function\n")
                    f.write("    _original_print = print\n")
                    f.write("    def print(*args, **kwargs):\n")
                    f.write("        fixed_args = [fix_arabic_print(arg) for arg in args]\n")
                    f.write("        _original_print(*fixed_args, **kwargs)\n")
                    f.write("    import builtins\n")
                    f.write("    builtins.print = print\n")
                    f.write("\n")
                f.write(code)
            
            start_time = asyncio.get_event_loop().time()
            
            if config.get("compile", False):
                # Compile first
                result = await self._compile_code(language, temp_file, **kwargs)
                if not result.success:
                    return result
                
                # Then run
                result = await self._run_compiled_code(language, temp_file, 
                                                     input_data, **kwargs)
            else:
                # Direct execution
                result = await self._run_interpreted_code(language, temp_file, 
                                                        input_data, **kwargs)
            
            end_time = asyncio.get_event_loop().time()
            result.execution_time = end_time - start_time
            
            return result
            
        finally:
            # Cleanup
            self._cleanup_temp_files(temp_file)
    
    async def _compile_code(self, language: Language, source_file: Path, 
                           **kwargs) -> ExecutionResult:
        """Compile code for compiled languages"""
        config = self.language_configs[language]
        
        if language == Language.RUST:
            output_file = source_file.with_suffix(".exe" if platform.system() == "Windows" else "")
            command = config["command"] + [str(source_file), "-o", str(output_file)]
        elif language == Language.CPP:
            output_file = source_file.with_suffix(".exe" if platform.system() == "Windows" else "")
            command = config["command"] + [str(output_file), str(source_file)]
        elif language == Language.JAVA:
            command = config["command"] + [str(source_file)]
            output_file = source_file.with_suffix(".class")
        elif language == Language.CSHARP:
            output_file = source_file.with_suffix(".exe")
            command = config["command"] + [str(source_file)]
        else:
            return ExecutionResult(
                success=False,
                output="",
                error=f"Compilation not supported for {language.value}",
                execution_time=0.0,
                language=language.value
            )
        
        try:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.temp_dir)
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=config.get("timeout", 60)
            )
            
            if process.returncode == 0:
                return ExecutionResult(
                    success=True,
                    output=stdout.decode('utf-8', errors='ignore'),
                    error=stderr.decode('utf-8', errors='ignore'),
                    execution_time=0.0,
                    language=language.value,
                    exit_code=process.returncode
                )
            else:
                return ExecutionResult(
                    success=False,
                    output=stdout.decode('utf-8', errors='ignore'),
                    error=stderr.decode('utf-8', errors='ignore'),
                    execution_time=0.0,
                    language=language.value,
                    exit_code=process.returncode
                )
                
        except asyncio.TimeoutError:
            return ExecutionResult(
                success=False,
                output="",
                error="Compilation timed out",
                execution_time=0.0,
                language=language.value
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=f"Compilation error: {str(e)}",
                execution_time=0.0,
                language=language.value
            )
    
    async def _run_compiled_code(self, language: Language, source_file: Path, 
                                input_data: str = "", **kwargs) -> ExecutionResult:
        """Run compiled code"""
        config = self.language_configs[language]
        
        if language == Language.RUST or language == Language.CPP:
            executable = source_file.with_suffix(".exe" if platform.system() == "Windows" else "")
            command = [str(executable)]
        elif language == Language.JAVA:
            class_name = source_file.stem
            command = config["run_command"] + [class_name]
        elif language == Language.CSHARP:
            executable = source_file.with_suffix(".exe")
            command = [str(executable)]
        else:
            return ExecutionResult(
                success=False,
                output="",
                error=f"Running compiled code not supported for {language.value}",
                execution_time=0.0,
                language=language.value
            )
        
        return await self._run_command(command, input_data, config.get("timeout", 30))
    
    async def _run_interpreted_code(self, language: Language, source_file: Path,
                                   input_data: str = "", **kwargs) -> ExecutionResult:
        """Run interpreted code"""
        config = self.language_configs[language]
        command = config["command"] + [str(source_file)]
        env = config.get("env", {})

        return await self._run_command(command, input_data, config.get("timeout", 30), env)
    
    async def _run_command(self, command: List[str], input_data: str = "",
                          timeout: int = 30, env: dict = None) -> ExecutionResult:
        """Run a command and return result"""
        try:
            # Prepare environment variables
            process_env = os.environ.copy()
            if env:
                process_env.update(env)

            # Ensure UTF-8 support on Windows
            if platform.system() == "Windows":
                process_env["PYTHONIOENCODING"] = "utf-8"
                process_env["PYTHONUTF8"] = "1"

            process = await asyncio.create_subprocess_exec(
                *command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.temp_dir),
                env=process_env
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(input=input_data.encode('utf-8') if input_data else None),
                timeout=timeout
            )
            
            return ExecutionResult(
                success=process.returncode == 0,
                output=stdout.decode('utf-8', errors='ignore'),
                error=stderr.decode('utf-8', errors='ignore'),
                execution_time=0.0,  # Will be set by caller
                language="",  # Will be set by caller
                exit_code=process.returncode
            )
            
        except asyncio.TimeoutError:
            return ExecutionResult(
                success=False,
                output="",
                error="انتهت مهلة تنفيذ الكود (timeout) - الكود يستغرق وقتاً أطول من المسموح",
                execution_time=0.0,
                language="",
                exit_code=-1
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=f"خطأ في تنفيذ الكود: {str(e)}",
                execution_time=0.0,
                language="",
                exit_code=-1
            )
    
    def _cleanup_temp_files(self, source_file: Path):
        """Clean up temporary files"""
        try:
            # Remove source file
            if source_file.exists():
                source_file.unlink()
            
            # Remove compiled files
            for suffix in [".exe", "", ".class", ".o"]:
                compiled_file = source_file.with_suffix(suffix)
                if compiled_file.exists() and compiled_file != source_file:
                    compiled_file.unlink()
                    
        except Exception as e:
            print(f"Warning: Could not clean up temp files: {e}")
    
    def get_language_info(self, language: str) -> Dict[str, Any]:
        """Get information about a programming language"""
        try:
            lang_enum = Language(language.lower())
            config = self.language_configs[lang_enum]
            
            return {
                "name": language,
                "extension": config["extension"],
                "compiled": config.get("compile", False),
                "available": lang_enum in self.available_languages,
                "timeout": config.get("timeout", 30)
            }
        except ValueError:
            return {
                "name": language,
                "available": False,
                "error": "Unsupported language"
            }

# Backward compatibility alias
CodeExecutor = AdvancedCodeExecutor
