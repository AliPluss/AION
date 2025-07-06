#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔒 AION Security Audit
Comprehensive security and vulnerability check
"""

import os
import sys
import ast
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any

class SecurityAuditor:
    """AION Security Auditor"""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.info = []
    
    def log_issue(self, severity: str, message: str, file_path: str = "", line: int = 0):
        """Log security issue"""
        entry = {
            "severity": severity,
            "message": message,
            "file": file_path,
            "line": line
        }
        
        if severity == "HIGH":
            self.issues.append(entry)
        elif severity == "MEDIUM":
            self.warnings.append(entry)
        else:
            self.info.append(entry)
    
    def check_file_permissions(self):
        """Check file permissions for security issues"""
        print("🔐 Checking File Permissions...")
        
        sensitive_files = [
            "config/config.json",
            "main.py",
            "src/utils/code_executor.py",
            "src/plugins/plugin_manager.py"
        ]
        
        for file_path in sensitive_files:
            if os.path.exists(file_path):
                stat_info = os.stat(file_path)
                mode = oct(stat_info.st_mode)[-3:]
                
                # Check for overly permissive permissions
                if mode in ["777", "666"]:
                    if file_path.endswith(".py"):
                        self.log_issue("MEDIUM", f"Executable file has write permissions for all: {mode}", file_path)
                    elif file_path.endswith(".json"):
                        self.log_issue("LOW", f"Config file readable by all: {mode}", file_path)
                
                print(f"  {file_path}: {mode} - {'✅ OK' if mode in ['644', '664', '755'] else '⚠️ Check'}")
    
    def check_code_injection_risks(self):
        """Check for potential code injection vulnerabilities"""
        print("\n💉 Checking Code Injection Risks...")
        
        python_files = list(Path(".").rglob("*.py"))
        dangerous_functions = [
            "eval", "exec", "compile", "__import__",
            "subprocess.call", "os.system", "os.popen"
        ]
        
        for py_file in python_files:
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Parse AST to find function calls
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Call):
                            func_name = ""
                            if isinstance(node.func, ast.Name):
                                func_name = node.func.id
                            elif isinstance(node.func, ast.Attribute):
                                if isinstance(node.func.value, ast.Name):
                                    func_name = f"{node.func.value.id}.{node.func.attr}"
                            
                            if func_name in dangerous_functions:
                                # Check if it's properly sanitized
                                line_num = getattr(node, 'lineno', 0)
                                if func_name in ["eval", "exec"]:
                                    self.log_issue("HIGH", f"Dangerous function {func_name} found", str(py_file), line_num)
                                else:
                                    self.log_issue("MEDIUM", f"Potentially dangerous function {func_name} found", str(py_file), line_num)
                
                except SyntaxError:
                    self.log_issue("LOW", f"Syntax error in file (could indicate tampering)", str(py_file))
                    
            except Exception as e:
                self.log_issue("LOW", f"Could not analyze file: {e}", str(py_file))
    
    def check_input_validation(self):
        """Check input validation in critical functions"""
        print("\n🛡️ Checking Input Validation...")
        
        # Check code_executor.py for input validation
        executor_file = Path("src/utils/code_executor.py")
        if executor_file.exists():
            with open(executor_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Look for input validation patterns
            validation_patterns = [
                "if not", "assert", "raise", "ValueError", "TypeError",
                "sanitize", "validate", "check"
            ]
            
            validation_found = any(pattern in content for pattern in validation_patterns)
            
            if validation_found:
                print("  ✅ Input validation patterns found in code executor")
            else:
                self.log_issue("MEDIUM", "Limited input validation in code executor", str(executor_file))
    
    def check_temp_file_security(self):
        """Check temporary file handling security"""
        print("\n📁 Checking Temporary File Security...")
        
        python_files = list(Path(".").rglob("*.py"))
        
        for py_file in python_files:
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Check for secure temp file usage
                if "tempfile" in content:
                    if "NamedTemporaryFile" in content and "delete=False" in content:
                        self.log_issue("MEDIUM", "Temporary files not auto-deleted", str(py_file))
                    elif "mktemp" in content:
                        self.log_issue("HIGH", "Insecure mktemp usage found", str(py_file))
                    else:
                        print(f"  ✅ Secure tempfile usage in {py_file}")
                        
            except Exception:
                pass
    
    def check_config_security(self):
        """Check configuration file security"""
        print("\n⚙️ Checking Configuration Security...")
        
        config_file = Path("config/config.json")
        if config_file.exists():
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                
                # Check for sensitive data
                def check_sensitive_recursive(obj, path=""):
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            if key.lower() in ["api_key", "password", "secret", "token"]:
                                if value and value.strip():
                                    self.log_issue("HIGH", f"API key/secret found in config: {path}.{key}", "config/config.json")
                                else:
                                    print(f"  ✅ Empty API key field: {path}.{key}")
                            else:
                                check_sensitive_recursive(value, f"{path}.{key}")
                
                check_sensitive_recursive(config)
                
            except Exception as e:
                self.log_issue("MEDIUM", f"Could not parse config file: {e}", "config/config.json")
    
    def check_dependency_security(self):
        """Check dependencies for known vulnerabilities"""
        print("\n📦 Checking Dependencies...")
        
        requirements_file = Path("requirements.txt")
        if requirements_file.exists():
            try:
                with open(requirements_file, "r") as f:
                    requirements = f.read()
                
                # Check for pinned versions
                lines = [line.strip() for line in requirements.split('\n') if line.strip() and not line.startswith('#')]
                
                unpinned = []
                for line in lines:
                    if '>=' in line and '==' not in line:
                        unpinned.append(line)
                
                if unpinned:
                    self.log_issue("MEDIUM", f"Unpinned dependencies found: {', '.join(unpinned)}", "requirements.txt")
                else:
                    print("  ✅ All dependencies properly pinned")
                    
            except Exception as e:
                self.log_issue("LOW", f"Could not check requirements: {e}", "requirements.txt")
    
    def check_path_traversal(self):
        """Check for path traversal vulnerabilities"""
        print("\n🗂️ Checking Path Traversal Risks...")
        
        python_files = list(Path(".").rglob("*.py"))
        
        for py_file in python_files:
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Look for file operations with user input
                risky_patterns = [
                    "open(", "Path(", "os.path.join(",
                    "pathlib", "file_path", "filename"
                ]
                
                if any(pattern in content for pattern in risky_patterns):
                    # Check if there's path validation
                    if "resolve()" in content or "absolute()" in content or ".." not in content:
                        print(f"  ✅ Path operations appear safe in {py_file}")
                    else:
                        self.log_issue("MEDIUM", "Potential path traversal risk", str(py_file))
                        
            except Exception:
                pass
    
    def generate_report(self):
        """Generate security audit report"""
        print("\n" + "="*60)
        print("🔒 AION Security Audit Report")
        print("="*60)
        
        # High severity issues
        if self.issues:
            print(f"\n🚨 HIGH SEVERITY ISSUES ({len(self.issues)}):")
            for issue in self.issues:
                print(f"  ❌ {issue['message']}")
                if issue['file']:
                    print(f"     File: {issue['file']}" + (f" (line {issue['line']})" if issue['line'] else ""))
        
        # Medium severity warnings
        if self.warnings:
            print(f"\n⚠️  MEDIUM SEVERITY WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  ⚠️  {warning['message']}")
                if warning['file']:
                    print(f"     File: {warning['file']}" + (f" (line {warning['line']})" if warning['line'] else ""))
        
        # Info items
        if self.info:
            print(f"\n💡 INFORMATIONAL ({len(self.info)}):")
            for info in self.info:
                print(f"  ℹ️  {info['message']}")
                if info['file']:
                    print(f"     File: {info['file']}")
        
        # Overall assessment
        print(f"\n📊 SECURITY ASSESSMENT:")
        print(f"  High Issues: {len(self.issues)}")
        print(f"  Warnings: {len(self.warnings)}")
        print(f"  Info: {len(self.info)}")
        
        if len(self.issues) == 0 and len(self.warnings) <= 2:
            print("\n🎉 SECURITY STATUS: EXCELLENT")
            print("✅ No critical security issues found")
        elif len(self.issues) == 0 and len(self.warnings) <= 5:
            print("\n✅ SECURITY STATUS: GOOD")
            print("🔧 Minor security improvements recommended")
        else:
            print("\n⚠️  SECURITY STATUS: NEEDS ATTENTION")
            print("🔧 Security issues require immediate attention")
        
        return len(self.issues) == 0

def main():
    """Run comprehensive security audit"""
    auditor = SecurityAuditor()
    
    # Run all security checks
    auditor.check_file_permissions()
    auditor.check_code_injection_risks()
    auditor.check_input_validation()
    auditor.check_temp_file_security()
    auditor.check_config_security()
    auditor.check_dependency_security()
    auditor.check_path_traversal()
    
    # Generate report
    is_secure = auditor.generate_report()
    
    return is_secure

if __name__ == "__main__":
    main()
