"""
🔒 AION Isolated Sandbox System
Advanced sandbox system with Docker integration, security analysis, and code quality metrics
Features: Docker containers, Security scanning, Code quality analysis, Resource monitoring
"""

import os
import json
import asyncio
import tempfile
import subprocess
import time
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Optional imports with fallbacks
try:
    import docker
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False
    docker = None

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None

class SandboxStatus(Enum):
    """Sandbox execution status"""
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    KILLED = "killed"
    SECURITY_VIOLATION = "security_violation"

class SecurityLevel(Enum):
    """Security levels for sandbox execution"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MAXIMUM = "maximum"

@dataclass
class SecurityAnalysis:
    """Security analysis results"""
    level: SecurityLevel
    threats_detected: List[str] = field(default_factory=list)
    suspicious_patterns: List[str] = field(default_factory=list)
    file_operations: List[str] = field(default_factory=list)
    network_operations: List[str] = field(default_factory=list)
    system_calls: List[str] = field(default_factory=list)
    risk_score: float = 0.0
    recommendations: List[str] = field(default_factory=list)

@dataclass
class CodeQualityMetrics:
    """Code quality analysis metrics"""
    lines_of_code: int = 0
    complexity_score: float = 0.0
    maintainability_index: float = 0.0
    code_smells: List[str] = field(default_factory=list)
    security_issues: List[str] = field(default_factory=list)
    performance_issues: List[str] = field(default_factory=list)
    best_practices_violations: List[str] = field(default_factory=list)
    overall_grade: str = "N/A"

@dataclass
class ResourceUsage:
    """Resource usage monitoring"""
    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    disk_io_mb: float = 0.0
    network_io_mb: float = 0.0
    execution_time: float = 0.0
    peak_memory_mb: float = 0.0
    file_descriptors: int = 0
    processes_created: int = 0

@dataclass
class SandboxExecution:
    """Complete sandbox execution record"""
    execution_id: str
    code: str
    language: str
    status: SandboxStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    output: str = ""
    error: str = ""
    exit_code: int = 0
    security_analysis: Optional[SecurityAnalysis] = None
    quality_metrics: Optional[CodeQualityMetrics] = None
    resource_usage: Optional[ResourceUsage] = None
    container_id: Optional[str] = None
    sandbox_path: Optional[Path] = None

class IsolatedSandboxManager:
    """
    🚀 Advanced Isolated Sandbox Manager
    
    Professional sandbox system with:
    - Docker-based isolated execution
    - Multi-language support with security
    - Real-time resource monitoring
    - Advanced security analysis
    - Code quality metrics and analysis
    - Threat detection and prevention
    - Performance profiling
    - Execution history and analytics
    """
    
    def __init__(self):
        # Storage
        self.sandbox_dir = Path.home() / ".aion" / "sandbox"
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)
        
        # Docker client
        self.docker_client = None
        self.docker_available = DOCKER_AVAILABLE
        if self.docker_available:
            try:
                self.docker_client = docker.from_env()
                print("✅ Docker client initialized")
            except Exception as e:
                print(f"⚠️ Docker initialization failed: {e}")
                self.docker_available = False
        
        # Runtime data
        self.executions: Dict[str, SandboxExecution] = {}
        self.active_containers: Dict[str, Any] = {}
        
        # Statistics
        self.executions_count = 0
        self.security_violations = 0
        self.containers_created = 0
        
        # Security patterns
        self.security_patterns = self._load_security_patterns()
        
        # Language configurations
        self.language_configs = self._load_language_configs()
    
    def _load_security_patterns(self) -> Dict[str, List[str]]:
        """Load security threat patterns"""
        return {
            "file_operations": [
                r"open\s*\(['\"]\/",
                r"os\.system",
                r"subprocess\.",
                r"exec\s*\(",
                r"eval\s*\(",
                r"__import__",
                r"file\s*\(",
                r"input\s*\(",
                r"raw_input"
            ],
            "network_operations": [
                r"socket\.",
                r"urllib",
                r"requests\.",
                r"http\.",
                r"ftp\.",
                r"telnet",
                r"ssh"
            ],
            "system_calls": [
                r"os\.",
                r"sys\.",
                r"platform\.",
                r"getpass",
                r"pwd",
                r"grp"
            ],
            "dangerous_imports": [
                r"import\s+os",
                r"import\s+sys",
                r"import\s+subprocess",
                r"import\s+socket",
                r"from\s+os",
                r"from\s+sys"
            ]
        }
    
    def _load_language_configs(self) -> Dict[str, Dict[str, Any]]:
        """Load language-specific configurations"""
        return {
            "python": {
                "docker_image": "python:3.11-slim",
                "file_extension": ".py",
                "run_command": "python",
                "timeout": 30,
                "memory_limit": "128m",
                "security_level": SecurityLevel.MEDIUM
            },
            "javascript": {
                "docker_image": "node:18-slim",
                "file_extension": ".js",
                "run_command": "node",
                "timeout": 30,
                "memory_limit": "128m",
                "security_level": SecurityLevel.MEDIUM
            },
            "rust": {
                "docker_image": "rust:1.70-slim",
                "file_extension": ".rs",
                "run_command": "rustc",
                "timeout": 60,
                "memory_limit": "256m",
                "security_level": SecurityLevel.HIGH
            },
            "cpp": {
                "docker_image": "gcc:11-slim",
                "file_extension": ".cpp",
                "run_command": "g++",
                "timeout": 60,
                "memory_limit": "256m",
                "security_level": SecurityLevel.HIGH
            },
            "bash": {
                "docker_image": "ubuntu:22.04",
                "file_extension": ".sh",
                "run_command": "bash",
                "timeout": 30,
                "memory_limit": "64m",
                "security_level": SecurityLevel.MAXIMUM
            }
        }
    
    async def execute_code(self, code: str, language: str, 
                          security_level: Optional[SecurityLevel] = None,
                          timeout: Optional[int] = None) -> SandboxExecution:
        """Execute code in isolated sandbox"""
        execution_id = f"sandbox_{int(time.time())}_{hashlib.md5(code.encode()).hexdigest()[:8]}"
        
        # Create execution record
        execution = SandboxExecution(
            execution_id=execution_id,
            code=code,
            language=language,
            status=SandboxStatus.CREATED,
            start_time=datetime.now()
        )
        
        self.executions[execution_id] = execution
        self.executions_count += 1
        
        print(f"🔒 Starting sandbox execution: {execution_id}")
        
        try:
            # Security analysis
            execution.security_analysis = await self._analyze_security(code, language)
            
            # Check security level
            config = self.language_configs.get(language, {})
            required_level = security_level or config.get("security_level", SecurityLevel.MEDIUM)
            
            if execution.security_analysis.level.value > required_level.value:
                execution.status = SandboxStatus.SECURITY_VIOLATION
                execution.error = f"Security violation: {execution.security_analysis.level.value} > {required_level.value}"
                self.security_violations += 1
                return execution
            
            # Execute based on availability
            if self.docker_available and self.docker_client:
                await self._execute_in_docker(execution, timeout)
            else:
                await self._execute_locally(execution, timeout)
            
            # Code quality analysis
            execution.quality_metrics = await self._analyze_code_quality(code, language)
            
        except Exception as e:
            execution.status = SandboxStatus.FAILED
            execution.error = f"Execution failed: {str(e)}"
            print(f"❌ Sandbox execution failed: {e}")
        
        finally:
            execution.end_time = datetime.now()
            duration = (execution.end_time - execution.start_time).total_seconds()
            
            print(f"✅ Sandbox execution completed: {execution.status.value}")
            print(f"   Duration: {duration:.2f}s")
            if execution.resource_usage:
                print(f"   Peak memory: {execution.resource_usage.peak_memory_mb:.1f}MB")
        
        return execution

    async def _analyze_security(self, code: str, language: str) -> SecurityAnalysis:
        """Analyze code for security threats"""
        analysis = SecurityAnalysis(level=SecurityLevel.LOW)

        try:
            import re

            # Check for dangerous patterns
            for category, patterns in self.security_patterns.items():
                for pattern in patterns:
                    matches = re.findall(pattern, code, re.IGNORECASE)
                    if matches:
                        if category == "file_operations":
                            analysis.file_operations.extend(matches)
                        elif category == "network_operations":
                            analysis.network_operations.extend(matches)
                        elif category == "system_calls":
                            analysis.system_calls.extend(matches)

                        analysis.threats_detected.append(f"{category}: {pattern}")

            # Calculate risk score
            risk_factors = {
                "file_operations": len(analysis.file_operations) * 2,
                "network_operations": len(analysis.network_operations) * 3,
                "system_calls": len(analysis.system_calls) * 1.5,
                "code_length": len(code) / 1000
            }

            analysis.risk_score = sum(risk_factors.values())

            # Determine security level
            if analysis.risk_score > 10:
                analysis.level = SecurityLevel.MAXIMUM
            elif analysis.risk_score > 5:
                analysis.level = SecurityLevel.HIGH
            elif analysis.risk_score > 2:
                analysis.level = SecurityLevel.MEDIUM
            else:
                analysis.level = SecurityLevel.LOW

            # Generate recommendations
            if analysis.file_operations:
                analysis.recommendations.append("Restrict file system access")
            if analysis.network_operations:
                analysis.recommendations.append("Block network access")
            if analysis.system_calls:
                analysis.recommendations.append("Limit system call access")

            print(f"🔍 Security analysis: {analysis.level.value} (risk: {analysis.risk_score:.1f})")

        except Exception as e:
            print(f"⚠️ Security analysis failed: {e}")
            analysis.level = SecurityLevel.MAXIMUM  # Fail-safe

        return analysis

    async def _execute_in_docker(self, execution: SandboxExecution, timeout: Optional[int]):
        """Execute code in Docker container"""
        if not self.docker_client:
            raise Exception("Docker client not available")

        config = self.language_configs.get(execution.language, {})
        docker_image = config.get("docker_image", "ubuntu:22.04")
        memory_limit = config.get("memory_limit", "128m")
        exec_timeout = timeout or config.get("timeout", 30)

        execution.status = SandboxStatus.RUNNING

        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            execution.sandbox_path = temp_path

            # Write code to file
            file_ext = config.get("file_extension", ".txt")
            code_file = temp_path / f"code{file_ext}"
            code_file.write_text(execution.code)

            try:
                # Create container
                container = self.docker_client.containers.run(
                    docker_image,
                    command="sleep 3600",  # Keep container alive
                    detach=True,
                    mem_limit=memory_limit,
                    network_disabled=True,  # Security: no network access
                    read_only=True,  # Security: read-only filesystem
                    volumes={str(temp_path): {'bind': '/workspace', 'mode': 'ro'}},
                    working_dir='/workspace',
                    remove=True
                )

                execution.container_id = container.id
                self.active_containers[execution.execution_id] = container
                self.containers_created += 1

                print(f"🐳 Docker container created: {container.id[:12]}")

                # Execute code
                run_command = config.get("run_command", "cat")
                exec_command = f"{run_command} code{file_ext}"

                # Monitor resource usage
                resource_monitor = asyncio.create_task(
                    self._monitor_container_resources(container, execution)
                )

                # Execute with timeout
                exec_result = container.exec_run(
                    exec_command,
                    stdout=True,
                    stderr=True
                )

                execution.output = exec_result.output.decode('utf-8', errors='ignore')
                execution.exit_code = exec_result.exit_code

                if execution.exit_code == 0:
                    execution.status = SandboxStatus.COMPLETED
                else:
                    execution.status = SandboxStatus.FAILED
                    execution.error = f"Exit code: {execution.exit_code}"

                # Stop resource monitoring
                resource_monitor.cancel()

                # Clean up container
                container.stop(timeout=1)
                if execution.execution_id in self.active_containers:
                    del self.active_containers[execution.execution_id]

            except Exception as e:
                execution.status = SandboxStatus.FAILED
                execution.error = f"Docker execution error: {str(e)}"

                # Clean up on error
                if execution.execution_id in self.active_containers:
                    try:
                        self.active_containers[execution.execution_id].stop(timeout=1)
                        del self.active_containers[execution.execution_id]
                    except:
                        pass

    async def _execute_locally(self, execution: SandboxExecution, timeout: Optional[int]):
        """Execute code locally with restrictions"""
        config = self.language_configs.get(execution.language, {})
        exec_timeout = timeout or config.get("timeout", 30)

        execution.status = SandboxStatus.RUNNING

        # Create temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            execution.sandbox_path = temp_path

            # Write code to file
            file_ext = config.get("file_extension", ".txt")
            code_file = temp_path / f"code{file_ext}"
            code_file.write_text(execution.code)

            try:
                # Prepare command
                run_command = config.get("run_command", "cat")
                full_command = f"{run_command} {code_file}"

                # Monitor resource usage
                start_time = time.time()

                # Execute with timeout
                process = await asyncio.create_subprocess_shell(
                    full_command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=temp_path
                )

                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(), timeout=exec_timeout
                    )

                    execution.output = stdout.decode('utf-8', errors='ignore')
                    execution.error = stderr.decode('utf-8', errors='ignore')
                    execution.exit_code = process.returncode

                    if execution.exit_code == 0:
                        execution.status = SandboxStatus.COMPLETED
                    else:
                        execution.status = SandboxStatus.FAILED

                except asyncio.TimeoutError:
                    execution.status = SandboxStatus.TIMEOUT
                    execution.error = f"Execution timed out after {exec_timeout}s"
                    process.kill()

                # Record resource usage
                end_time = time.time()
                execution.resource_usage = ResourceUsage(
                    execution_time=end_time - start_time
                )

            except Exception as e:
                execution.status = SandboxStatus.FAILED
                execution.error = f"Local execution error: {str(e)}"

    async def _monitor_container_resources(self, container, execution: SandboxExecution):
        """Monitor container resource usage"""
        if not PSUTIL_AVAILABLE:
            return

        resource_usage = ResourceUsage()
        max_memory = 0

        try:
            while True:
                stats = container.stats(stream=False)

                # CPU usage
                cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                           stats['precpu_stats']['cpu_usage']['total_usage']
                system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                              stats['precpu_stats']['system_cpu_usage']

                if system_delta > 0:
                    resource_usage.cpu_percent = (cpu_delta / system_delta) * 100

                # Memory usage
                memory_usage = stats['memory_stats']['usage']
                resource_usage.memory_mb = memory_usage / (1024 * 1024)
                max_memory = max(max_memory, resource_usage.memory_mb)

                await asyncio.sleep(1)

        except asyncio.CancelledError:
            resource_usage.peak_memory_mb = max_memory
            execution.resource_usage = resource_usage
        except Exception as e:
            print(f"⚠️ Resource monitoring failed: {e}")

    async def _analyze_code_quality(self, code: str, language: str) -> CodeQualityMetrics:
        """Analyze code quality metrics"""
        metrics = CodeQualityMetrics()

        try:
            # Basic metrics
            lines = code.split('\n')
            metrics.lines_of_code = len([line for line in lines if line.strip()])

            # Language-specific analysis
            if language == "python":
                metrics = await self._analyze_python_quality(code, metrics)
            elif language == "javascript":
                metrics = await self._analyze_javascript_quality(code, metrics)
            else:
                metrics = await self._analyze_generic_quality(code, metrics)

            # Calculate overall grade
            if metrics.maintainability_index > 80:
                metrics.overall_grade = "A"
            elif metrics.maintainability_index > 60:
                metrics.overall_grade = "B"
            elif metrics.maintainability_index > 40:
                metrics.overall_grade = "C"
            elif metrics.maintainability_index > 20:
                metrics.overall_grade = "D"
            else:
                metrics.overall_grade = "F"

            print(f"📊 Code quality: {metrics.overall_grade} (maintainability: {metrics.maintainability_index:.1f})")

        except Exception as e:
            print(f"⚠️ Code quality analysis failed: {e}")

        return metrics

    async def _analyze_python_quality(self, code: str, metrics: CodeQualityMetrics) -> CodeQualityMetrics:
        """Analyze Python code quality"""
        import re

        # Check for common Python issues
        if "import *" in code:
            metrics.code_smells.append("Wildcard import detected")

        if re.search(r'except\s*:', code):
            metrics.code_smells.append("Bare except clause")

        if "eval(" in code or "exec(" in code:
            metrics.security_issues.append("Dynamic code execution")

        # Calculate complexity (simplified)
        complexity_indicators = len(re.findall(r'\b(if|for|while|try|except|with)\b', code))
        metrics.complexity_score = complexity_indicators / max(metrics.lines_of_code, 1) * 100

        # Maintainability index (simplified)
        metrics.maintainability_index = max(0, 100 - metrics.complexity_score - len(metrics.code_smells) * 10)

        return metrics

    async def _analyze_javascript_quality(self, code: str, metrics: CodeQualityMetrics) -> CodeQualityMetrics:
        """Analyze JavaScript code quality"""
        import re

        # Check for common JavaScript issues
        if "eval(" in code:
            metrics.security_issues.append("eval() usage detected")

        if re.search(r'var\s+', code):
            metrics.code_smells.append("var usage (prefer let/const)")

        if "==" in code and "===" not in code:
            metrics.code_smells.append("Loose equality operator")

        # Calculate complexity
        complexity_indicators = len(re.findall(r'\b(if|for|while|try|catch|switch)\b', code))
        metrics.complexity_score = complexity_indicators / max(metrics.lines_of_code, 1) * 100

        # Maintainability index
        metrics.maintainability_index = max(0, 100 - metrics.complexity_score - len(metrics.code_smells) * 10)

        return metrics

    async def _analyze_generic_quality(self, code: str, metrics: CodeQualityMetrics) -> CodeQualityMetrics:
        """Analyze generic code quality"""
        import re

        # Basic complexity analysis
        complexity_indicators = len(re.findall(r'\b(if|for|while|loop|switch|case)\b', code, re.IGNORECASE))
        metrics.complexity_score = complexity_indicators / max(metrics.lines_of_code, 1) * 100

        # Check for long lines
        long_lines = [line for line in code.split('\n') if len(line) > 120]
        if long_lines:
            metrics.code_smells.append(f"{len(long_lines)} lines exceed 120 characters")

        # Basic maintainability
        metrics.maintainability_index = max(0, 100 - metrics.complexity_score - len(metrics.code_smells) * 5)

        return metrics

    def get_execution(self, execution_id: str) -> Optional[SandboxExecution]:
        """Get execution by ID"""
        return self.executions.get(execution_id)

    def list_executions(self, language: Optional[str] = None,
                       status: Optional[SandboxStatus] = None,
                       limit: int = 50) -> List[SandboxExecution]:
        """List executions with optional filtering"""
        executions = list(self.executions.values())

        if language:
            executions = [e for e in executions if e.language == language]

        if status:
            executions = [e for e in executions if e.status == status]

        return sorted(executions, key=lambda e: e.start_time, reverse=True)[:limit]

    def kill_execution(self, execution_id: str) -> bool:
        """Kill running execution"""
        if execution_id not in self.active_containers:
            return False

        try:
            container = self.active_containers[execution_id]
            container.kill()
            del self.active_containers[execution_id]

            if execution_id in self.executions:
                self.executions[execution_id].status = SandboxStatus.KILLED

            print(f"💀 Execution killed: {execution_id}")
            return True

        except Exception as e:
            print(f"⚠️ Failed to kill execution: {e}")
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """Get sandbox statistics"""
        status_counts = {}
        for execution in self.executions.values():
            status = execution.status.value
            status_counts[status] = status_counts.get(status, 0) + 1

        return {
            "executions_count": self.executions_count,
            "security_violations": self.security_violations,
            "containers_created": self.containers_created,
            "active_containers": len(self.active_containers),
            "docker_available": self.docker_available,
            "psutil_available": PSUTIL_AVAILABLE,
            "supported_languages": list(self.language_configs.keys()),
            "status_distribution": status_counts,
            "total_executions": len(self.executions)
        }
