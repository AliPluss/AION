"""
🚀 AION Code Executor - Enhanced Multi-Language Support
Advanced code execution with optimized Rust and C++ support
"""

import os
import sys
import subprocess
import tempfile
import shutil
import platform
import asyncio
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn


# Security utilities
try:
    from .input_validator import validator
    from .secure_temp import secure_temp
except ImportError:
    # Fallback if security modules not available
    class DummyValidator:
        @staticmethod
        def validate_code_input(code, max_length=10000):
            return code
        @staticmethod
        def validate_filename(filename):
            return filename
    validator = DummyValidator()
    secure_temp = None

console = Console()

class Language(Enum):
    """Supported programming languages with performance optimization"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    RUST = "rust"
    CPP = "cpp"
    C = "c"
    JAVA = "java"
    CSHARP = "csharp"
    GO = "go"

@dataclass
class ExecutionResult:
    """Enhanced code execution result"""
    success: bool
    output: str
    error: str
    execution_time: float
    language: str
    exit_code: int = 0
    memory_usage: Optional[float] = None
    compile_time: Optional[float] = None

@dataclass
class LanguageConfig:
    """Language configuration with optimization settings"""
    extension: str
    command: List[str]
    compile: bool = False
    run_command: Optional[List[str]] = None
    timeout: int = 30
    env: Optional[Dict[str, str]] = None
    optimization_flags: Optional[List[str]] = None
    description_ar: str = ""
    description_en: str = ""
    performance_level: str = "medium"  # low, medium, high, extreme

class CodeExecutor:
    """Enhanced multi-language code executor with performance optimization"""
    
    def __init__(self, temp_dir: Optional[Path] = None):
        self.temp_dir = Path(temp_dir) if temp_dir else Path(tempfile.gettempdir()) / "aion_executor"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Enhanced language configurations with optimization
        self.language_configs = {
            Language.PYTHON: LanguageConfig(
                extension=".py",
                command=[sys.executable, "-u"],
                compile=False,
                timeout=30,
                env={"PYTHONIOENCODING": "utf-8"},
                description_ar="بايثون - لغة سهلة ومرنة للتطوير السريع",
                description_en="Python - Easy and flexible for rapid development",
                performance_level="medium"
            ),
            Language.JAVASCRIPT: LanguageConfig(
                extension=".js",
                command=["node"],
                compile=False,
                timeout=30,
                description_ar="جافا سكريبت - لغة الويب والتطبيقات التفاعلية",
                description_en="JavaScript - Web and interactive applications",
                performance_level="medium"
            ),
            Language.RUST: LanguageConfig(
                extension=".rs",
                command=["rustc"],
                compile=True,
                timeout=120,  # Longer timeout for compilation
                optimization_flags=["-O", "--edition=2021"],  # Optimization flags
                description_ar="رست - أداء عالي مع أمان الذاكرة",
                description_en="Rust - High performance with memory safety",
                performance_level="extreme"
            ),
            Language.CPP: LanguageConfig(
                extension=".cpp",
                command=["g++"],
                compile=True,
                timeout=90,
                optimization_flags=["-O3", "-std=c++20", "-march=native"],  # Maximum optimization
                description_ar="سي++ - أقصى أداء وتحكم كامل",
                description_en="C++ - Maximum performance and full control",
                performance_level="extreme"
            ),
            Language.C: LanguageConfig(
                extension=".c",
                command=["gcc"],
                compile=True,
                timeout=60,
                optimization_flags=["-O3", "-std=c11", "-march=native"],
                description_ar="سي - لغة النظم والأداء العالي",
                description_en="C - Systems programming and high performance",
                performance_level="extreme"
            ),
            Language.GO: LanguageConfig(
                extension=".go",
                command=["go", "run"],
                compile=False,  # go run compiles and runs
                timeout=45,
                description_ar="جو - بساطة وأداء للخوادم",
                description_en="Go - Simplicity and performance for servers",
                performance_level="high"
            ),
            Language.JAVA: LanguageConfig(
                extension=".java",
                command=["javac"],
                compile=True,
                run_command=["java"],
                timeout=60,
                description_ar="جافا - منصة متعددة وموثوقة",
                description_en="Java - Cross-platform and reliable",
                performance_level="high"
            ),
            Language.CSHARP: LanguageConfig(
                extension=".cs",
                command=["csc"],
                compile=True,
                timeout=60,
                description_ar="سي شارب - تطوير تطبيقات ويندوز",
                description_en="C# - Windows application development",
                performance_level="high"
            )
        }
        
        self.available_languages = []
        self._detect_available_languages()
    
    def _detect_available_languages(self):
        """Detect available programming languages with enhanced detection"""
        console.print("🔍 فحص اللغات المتاحة | Detecting available languages...")
        
        detection_commands = {
            Language.PYTHON: [sys.executable, "--version"],
            Language.JAVASCRIPT: ["node", "--version"],
            Language.RUST: ["rustc", "--version"],
            Language.CPP: ["g++", "--version"],
            Language.C: ["gcc", "--version"],
            Language.GO: ["go", "version"],
            Language.JAVA: ["javac", "-version"],
            Language.CSHARP: ["csc", "/help"] if platform.system() == "Windows" else ["mcs", "--version"]
        }
        
        for language, command in detection_commands.items():
            try:
                result = subprocess.run(command, capture_output=True, text=True, timeout=10)
                if result.returncode == 0 or language == Language.CSHARP:  # csc returns non-zero for help
                    self.available_languages.append(language)
                    config = self.language_configs[language]
                    console.print(f"  ✅ {language.value.upper()} - {config.description_ar}")
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                console.print(f"  ❌ {language.value.upper()} - غير متاح | Not available")
    
    def get_available_languages(self) -> List[Dict[str, Any]]:
        """Get detailed list of available programming languages"""
        languages_info = []
        for lang in self.available_languages:
            config = self.language_configs[lang]
            languages_info.append({
                "name": lang.value,
                "display_name": lang.value.upper(),
                "description_ar": config.description_ar,
                "description_en": config.description_en,
                "performance_level": config.performance_level,
                "compiled": config.compile,
                "extension": config.extension,
                "timeout": config.timeout
            })
        return languages_info
    
    def get_performance_languages(self) -> List[Dict[str, Any]]:
        """Get high-performance languages (Rust, C++, C)"""
        high_perf_langs = []
        for lang in self.available_languages:
            config = self.language_configs[lang]
            if config.performance_level in ["high", "extreme"]:
                high_perf_langs.append({
                    "name": lang.value,
                    "display_name": lang.value.upper(),
                    "description_ar": config.description_ar,
                    "description_en": config.description_en,
                    "performance_level": config.performance_level
                })
        return high_perf_langs

    async def execute_code(self, code: str, language: str,
                          input_data: str = "", optimize: bool = True, **kwargs) -> ExecutionResult:
        """Execute code with enhanced optimization support"""
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

            return await self._execute_language(lang_enum, code, input_data, optimize, **kwargs)

        except ValueError:
            return ExecutionResult(
                success=False,
                output="",
                error=f"لغة برمجة غير مدعومة: {language}",
                execution_time=0.0,
                language=language
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=f"خطأ في التنفيذ: {str(e)}",
                execution_time=0.0,
                language=language
            )

    async def _execute_language(self, language: Language, code: str,
                               input_data: str = "", optimize: bool = True, **kwargs) -> ExecutionResult:
        """Execute code for specific language with optimization"""
        config = self.language_configs[language]

        # Create temporary file with unique name
        timestamp = int(time.time() * 1000)
        temp_file = self.temp_dir / f"aion_{timestamp}_{os.getpid()}{config.extension}"

        try:
            # Write code to temporary file
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(code)

            start_time = time.time()

            if config.compile:
                # Compile first
                compile_start = time.time()
                result = await self._compile_code(language, temp_file, optimize, **kwargs)
                compile_time = time.time() - compile_start

                if not result.success:
                    result.compile_time = compile_time
                    return result

                # Then run compiled code
                result = await self._run_compiled_code(language, temp_file, input_data, **kwargs)
                result.compile_time = compile_time
            else:
                # Direct execution for interpreted languages
                result = await self._run_interpreted_code(language, temp_file, input_data, **kwargs)

            result.execution_time = time.time() - start_time
            return result

        finally:
            # Cleanup temporary files
            self._cleanup_temp_files(temp_file)

    async def _compile_code(self, language: Language, source_file: Path,
                           optimize: bool = True, **kwargs) -> ExecutionResult:
        """Compile code with optimization flags"""
        config = self.language_configs[language]

        if language == Language.RUST:
            executable = source_file.with_suffix(".exe" if platform.system() == "Windows" else "")
            command = ["rustc"]

            if optimize and config.optimization_flags:
                command.extend(config.optimization_flags)

            command.extend([str(source_file), "-o", str(executable)])

        elif language == Language.CPP:
            executable = source_file.with_suffix(".exe" if platform.system() == "Windows" else "")
            command = ["g++"]

            if optimize and config.optimization_flags:
                command.extend(config.optimization_flags)

            command.extend([str(source_file), "-o", str(executable)])

        elif language == Language.C:
            executable = source_file.with_suffix(".exe" if platform.system() == "Windows" else "")
            command = ["gcc"]

            if optimize and config.optimization_flags:
                command.extend(config.optimization_flags)

            command.extend([str(source_file), "-o", str(executable)])

        elif language == Language.JAVA:
            command = ["javac", str(source_file)]

        elif language == Language.CSHARP:
            executable = source_file.with_suffix(".exe")
            command = ["csc", f"/out:{executable}", str(source_file)]

        else:
            return ExecutionResult(
                success=False,
                output="",
                error=f"تجميع غير مدعوم للغة {language.value}",
                execution_time=0.0,
                language=language.value
            )

        return await self._run_command(command, "", config.timeout)

    async def _run_compiled_code(self, language: Language, source_file: Path,
                                input_data: str = "", **kwargs) -> ExecutionResult:
        """Run compiled code with performance monitoring"""
        config = self.language_configs[language]

        if language in [Language.RUST, Language.CPP, Language.C]:
            executable = source_file.with_suffix(".exe" if platform.system() == "Windows" else "")
            command = [str(executable)]
        elif language == Language.JAVA:
            class_name = source_file.stem
            command = ["java", "-cp", str(source_file.parent), class_name]
        elif language == Language.CSHARP:
            executable = source_file.with_suffix(".exe")
            command = [str(executable)]
        else:
            return ExecutionResult(
                success=False,
                output="",
                error=f"تشغيل الكود المجمع غير مدعوم للغة {language.value}",
                execution_time=0.0,
                language=language.value
            )

        return await self._run_command(command, input_data, config.timeout)

    async def _run_interpreted_code(self, language: Language, source_file: Path,
                                   input_data: str = "", **kwargs) -> ExecutionResult:
        """Run interpreted code"""
        config = self.language_configs[language]

        if language == Language.GO:
            command = ["go", "run", str(source_file)]
        else:
            command = config.command + [str(source_file)]

        env = config.env or {}
        return await self._run_command(command, input_data, config.timeout, env)

    async def _run_command(self, command: List[str], input_data: str = "",
                          timeout: int = 30, env: Optional[Dict[str, str]] = None) -> ExecutionResult:
        """Run command with enhanced error handling and performance monitoring"""
        try:
            # Prepare environment
            process_env = os.environ.copy()
            if env:
                process_env.update(env)

            # Start process
            process = await asyncio.create_subprocess_exec(
                *command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=process_env,
                cwd=self.temp_dir
            )

            # Run with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(input_data.encode('utf-8') if input_data else None),
                    timeout=timeout
                )

                return ExecutionResult(
                    success=process.returncode == 0,
                    output=stdout.decode('utf-8', errors='replace'),
                    error=stderr.decode('utf-8', errors='replace'),
                    execution_time=0.0,  # Will be set by caller
                    language="",  # Will be set by caller
                    exit_code=process.returncode or 0
                )

            except asyncio.TimeoutError:
                # Kill process if timeout
                try:
                    process.kill()
                    await process.wait()
                except:
                    pass

                return ExecutionResult(
                    success=False,
                    output="",
                    error=f"انتهت مهلة التنفيذ ({timeout} ثانية) | Execution timeout ({timeout} seconds)",
                    execution_time=timeout,
                    language="",
                    exit_code=-1
                )

        except Exception as e:
            return ExecutionResult(
                success=False,
                output="",
                error=f"خطأ في تشغيل الأمر: {str(e)}",
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

            # Remove compiled executable
            executable_extensions = [".exe", ""] if platform.system() == "Windows" else [""]
            for ext in executable_extensions:
                executable = source_file.with_suffix(ext)
                if executable.exists() and executable != source_file:
                    executable.unlink()

            # Remove Java class files
            if source_file.suffix == ".java":
                class_file = source_file.with_suffix(".class")
                if class_file.exists():
                    class_file.unlink()

        except Exception:
            pass  # Ignore cleanup errors

    def get_language_info(self, language: str) -> Dict[str, Any]:
        """Get detailed information about a programming language"""
        try:
            lang_enum = Language(language.lower())
            config = self.language_configs[lang_enum]

            return {
                "name": language,
                "display_name": lang_enum.value.upper(),
                "extension": config.extension,
                "compiled": config.compile,
                "available": lang_enum in self.available_languages,
                "timeout": config.timeout,
                "description_ar": config.description_ar,
                "description_en": config.description_en,
                "performance_level": config.performance_level,
                "optimization_available": bool(config.optimization_flags)
            }
        except ValueError:
            return {
                "name": language,
                "available": False,
                "error": "لغة برمجة غير مدعومة"
            }

    def get_optimization_info(self) -> Dict[str, List[str]]:
        """Get optimization information for compiled languages"""
        optimization_info = {}

        for lang in [Language.RUST, Language.CPP, Language.C]:
            if lang in self.available_languages:
                config = self.language_configs[lang]
                optimization_info[lang.value] = {
                    "flags": config.optimization_flags or [],
                    "description_ar": f"تحسينات {lang.value.upper()} للأداء العالي",
                    "description_en": f"{lang.value.upper()} optimizations for high performance"
                }

        return optimization_info

    async def benchmark_language(self, language: str, test_code: str) -> Dict[str, Any]:
        """Benchmark a language with test code"""
        results = []

        # Run multiple times for average
        for i in range(3):
            result = await self.execute_code(test_code, language, optimize=True)
            if result.success:
                results.append({
                    "execution_time": result.execution_time,
                    "compile_time": result.compile_time or 0
                })

        if not results:
            return {"error": "فشل في تشغيل الاختبار"}

        avg_execution = sum(r["execution_time"] for r in results) / len(results)
        avg_compile = sum(r["compile_time"] for r in results) / len(results)

        return {
            "language": language,
            "average_execution_time": avg_execution,
            "average_compile_time": avg_compile,
            "total_time": avg_execution + avg_compile,
            "runs": len(results)
        }
