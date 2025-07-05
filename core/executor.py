"""
🚀 AION Code Executor
Multi-language code execution with security and sandboxing
"""

import os
import sys
import subprocess
import tempfile
import shutil
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import asyncio
import json

class Language(Enum):
    """Supported programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    RUST = "rust"
    CPP = "cpp"
    JAVA = "java"
    CSHARP = "csharp"

@dataclass
class ExecutionResult:
    """Code execution result"""
    success: bool
    output: str
    error: str
    execution_time: float
    language: str
    exit_code: int = 0

class CodeExecutor:
    """Multi-language code executor"""
    
    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir()) / "aion_execution"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Language configurations
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
