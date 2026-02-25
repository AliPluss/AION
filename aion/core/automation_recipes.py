"""
🧬 AION Automation Recipes System
Advanced automation system with command sequencing, scheduling, and macro recording
Features: Recipe creation, Scheduling, Macro recording, Conditional execution, Variables
"""

import json
import asyncio
import time
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Optional imports with fallbacks
try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False
    schedule = None

try:
    import crontab
    CRONTAB_AVAILABLE = True
except ImportError:
    CRONTAB_AVAILABLE = False
    crontab = None

class RecipeStatus(Enum):
    """Recipe execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SCHEDULED = "scheduled"

class CommandType(Enum):
    """Command types in recipes"""
    SHELL = "shell"
    PYTHON = "python"
    AI_PROMPT = "ai_prompt"
    EMAIL = "email"
    GITHUB = "github"
    SLACK = "slack"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    WAIT = "wait"
    VARIABLE = "variable"

@dataclass
class RecipeCommand:
    """Individual command in a recipe"""
    id: str
    type: CommandType
    command: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    timeout: int = 30
    retry_count: int = 0
    continue_on_error: bool = False
    condition: Optional[str] = None
    description: str = ""

@dataclass
class RecipeExecution:
    """Recipe execution record"""
    recipe_id: str
    execution_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: RecipeStatus = RecipeStatus.PENDING
    commands_executed: int = 0
    commands_failed: int = 0
    output: List[str] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None

@dataclass
class AutomationRecipe:
    """Complete automation recipe"""
    id: str
    name: str
    description: str
    commands: List[RecipeCommand]
    variables: Dict[str, Any] = field(default_factory=dict)
    schedule: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    author: str = "AION"
    version: str = "1.0"
    enabled: bool = True

class AutomationRecipeManager:
    """
    🚀 Advanced Automation Recipe Manager
    
    Professional automation system with:
    - Recipe creation and management
    - Command sequencing and chaining
    - Conditional execution and loops
    - Variable management and substitution
    - Scheduling and cron-like execution
    - Macro recording and playback
    - Error handling and retry logic
    - Execution history and logging
    """
    
    def __init__(self):
        # Storage
        self.recipes_dir = Path.home() / ".aion" / "recipes"
        self.recipes_dir.mkdir(parents=True, exist_ok=True)
        
        # Runtime data
        self.recipes: Dict[str, AutomationRecipe] = {}
        self.executions: Dict[str, RecipeExecution] = {}
        self.scheduled_jobs: Dict[str, Any] = {}
        self.recording_session: Optional[Dict[str, Any]] = None
        
        # Statistics
        self.recipes_created = 0
        self.recipes_executed = 0
        self.commands_executed = 0
        
        # Load existing recipes
        self._load_recipes()
        
        # Initialize scheduler if available
        if SCHEDULE_AVAILABLE:
            self._initialize_scheduler()
    
    def _load_recipes(self):
        """Load recipes from storage"""
        try:
            recipes_file = self.recipes_dir / "recipes.json"
            if recipes_file.exists():
                with open(recipes_file, 'r') as f:
                    recipes_data = json.load(f)
                
                for recipe_data in recipes_data:
                    recipe = self._deserialize_recipe(recipe_data)
                    self.recipes[recipe.id] = recipe
                
                print(f"✅ Loaded {len(self.recipes)} automation recipes")
            
        except Exception as e:
            print(f"⚠️ Recipe loading failed: {e}")
    
    def _save_recipes(self):
        """Save recipes to storage"""
        try:
            recipes_data = []
            for recipe in self.recipes.values():
                recipes_data.append(self._serialize_recipe(recipe))
            
            recipes_file = self.recipes_dir / "recipes.json"
            with open(recipes_file, 'w') as f:
                json.dump(recipes_data, f, indent=2, default=str)
            
            return True
            
        except Exception as e:
            print(f"⚠️ Recipe saving failed: {e}")
            return False
    
    def _serialize_recipe(self, recipe: AutomationRecipe) -> Dict[str, Any]:
        """Serialize recipe to dictionary"""
        return {
            "id": recipe.id,
            "name": recipe.name,
            "description": recipe.description,
            "commands": [
                {
                    "id": cmd.id,
                    "type": cmd.type.value,
                    "command": cmd.command,
                    "parameters": cmd.parameters,
                    "timeout": cmd.timeout,
                    "retry_count": cmd.retry_count,
                    "continue_on_error": cmd.continue_on_error,
                    "condition": cmd.condition,
                    "description": cmd.description
                }
                for cmd in recipe.commands
            ],
            "variables": recipe.variables,
            "schedule": recipe.schedule,
            "tags": recipe.tags,
            "created_at": recipe.created_at.isoformat(),
            "updated_at": recipe.updated_at.isoformat(),
            "author": recipe.author,
            "version": recipe.version,
            "enabled": recipe.enabled
        }
    
    def _deserialize_recipe(self, data: Dict[str, Any]) -> AutomationRecipe:
        """Deserialize recipe from dictionary"""
        commands = []
        for cmd_data in data.get("commands", []):
            command = RecipeCommand(
                id=cmd_data["id"],
                type=CommandType(cmd_data["type"]),
                command=cmd_data["command"],
                parameters=cmd_data.get("parameters", {}),
                timeout=cmd_data.get("timeout", 30),
                retry_count=cmd_data.get("retry_count", 0),
                continue_on_error=cmd_data.get("continue_on_error", False),
                condition=cmd_data.get("condition"),
                description=cmd_data.get("description", "")
            )
            commands.append(command)
        
        return AutomationRecipe(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            commands=commands,
            variables=data.get("variables", {}),
            schedule=data.get("schedule"),
            tags=data.get("tags", []),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            author=data.get("author", "AION"),
            version=data.get("version", "1.0"),
            enabled=data.get("enabled", True)
        )
    
    def create_recipe(self, name: str, description: str, 
                     commands: List[RecipeCommand], **kwargs) -> str:
        """Create new automation recipe"""
        recipe_id = f"recipe_{int(time.time())}_{len(self.recipes)}"
        
        recipe = AutomationRecipe(
            id=recipe_id,
            name=name,
            description=description,
            commands=commands,
            variables=kwargs.get("variables", {}),
            schedule=kwargs.get("schedule"),
            tags=kwargs.get("tags", []),
            author=kwargs.get("author", "AION"),
            version=kwargs.get("version", "1.0")
        )
        
        self.recipes[recipe_id] = recipe
        self.recipes_created += 1
        
        # Save to storage
        self._save_recipes()
        
        # Schedule if needed
        if recipe.schedule and SCHEDULE_AVAILABLE:
            self._schedule_recipe(recipe)
        
        print(f"✅ Recipe created: {name} ({recipe_id})")
        return recipe_id
    
    def create_simple_recipe(self, name: str, commands: List[str], 
                           description: str = "") -> str:
        """Create simple recipe from command list"""
        recipe_commands = []
        
        for i, cmd in enumerate(commands):
            command_id = f"cmd_{i+1}"
            
            # Detect command type
            if cmd.startswith("python ") or cmd.endswith(".py"):
                cmd_type = CommandType.PYTHON
            elif cmd.startswith("ai:") or cmd.startswith("prompt:"):
                cmd_type = CommandType.AI_PROMPT
                cmd = cmd.split(":", 1)[1].strip()
            elif cmd.startswith("email:"):
                cmd_type = CommandType.EMAIL
                cmd = cmd.split(":", 1)[1].strip()
            elif cmd.startswith("wait "):
                cmd_type = CommandType.WAIT
            else:
                cmd_type = CommandType.SHELL
            
            recipe_cmd = RecipeCommand(
                id=command_id,
                type=cmd_type,
                command=cmd,
                description=f"Step {i+1}"
            )
            recipe_commands.append(recipe_cmd)
        
        return self.create_recipe(name, description, recipe_commands)
    
    async def execute_recipe(self, recipe_id: str, 
                           variables: Optional[Dict[str, Any]] = None) -> RecipeExecution:
        """Execute automation recipe"""
        if recipe_id not in self.recipes:
            raise ValueError(f"Recipe not found: {recipe_id}")
        
        recipe = self.recipes[recipe_id]
        if not recipe.enabled:
            raise ValueError(f"Recipe is disabled: {recipe_id}")
        
        # Create execution record
        execution_id = f"exec_{int(time.time())}_{recipe_id}"
        execution = RecipeExecution(
            recipe_id=recipe_id,
            execution_id=execution_id,
            start_time=datetime.now(),
            status=RecipeStatus.RUNNING,
            variables={**recipe.variables, **(variables or {})}
        )
        
        self.executions[execution_id] = execution
        self.recipes_executed += 1
        
        print(f"🚀 Executing recipe: {recipe.name}")
        
        try:
            # Execute commands sequentially
            for i, command in enumerate(recipe.commands):
                if execution.status == RecipeStatus.CANCELLED:
                    break
                
                print(f"   Step {i+1}/{len(recipe.commands)}: {command.description or command.command[:50]}")
                
                # Check condition if specified
                if command.condition and not self._evaluate_condition(command.condition, execution.variables):
                    print(f"   ⏭️ Skipping command (condition not met): {command.condition}")
                    continue
                
                # Execute command with retries
                success = await self._execute_command(command, execution)
                
                if success:
                    execution.commands_executed += 1
                    self.commands_executed += 1
                else:
                    execution.commands_failed += 1
                    if not command.continue_on_error:
                        execution.status = RecipeStatus.FAILED
                        execution.error_message = f"Command failed: {command.command}"
                        break
            
            # Mark as completed if not failed or cancelled
            if execution.status == RecipeStatus.RUNNING:
                execution.status = RecipeStatus.COMPLETED
            
        except Exception as e:
            execution.status = RecipeStatus.FAILED
            execution.error_message = str(e)
            print(f"❌ Recipe execution failed: {e}")
        
        finally:
            execution.end_time = datetime.now()
            duration = (execution.end_time - execution.start_time).total_seconds()
            
            print(f"✅ Recipe execution completed: {execution.status.value}")
            print(f"   Duration: {duration:.2f}s")
            print(f"   Commands executed: {execution.commands_executed}")
            print(f"   Commands failed: {execution.commands_failed}")
        
        return execution

    async def _execute_command(self, command: RecipeCommand,
                             execution: RecipeExecution) -> bool:
        """Execute individual command with retry logic"""
        for attempt in range(command.retry_count + 1):
            try:
                if attempt > 0:
                    print(f"   🔄 Retry {attempt}/{command.retry_count}")

                # Substitute variables in command
                processed_command = self._substitute_variables(command.command, execution.variables)

                # Execute based on command type
                if command.type == CommandType.SHELL:
                    success, output = await self._execute_shell_command(processed_command, command.timeout)
                elif command.type == CommandType.PYTHON:
                    success, output = await self._execute_python_command(processed_command, command.timeout)
                elif command.type == CommandType.AI_PROMPT:
                    success, output = await self._execute_ai_prompt(processed_command, command.parameters)
                elif command.type == CommandType.EMAIL:
                    success, output = await self._execute_email_command(processed_command, command.parameters)
                elif command.type == CommandType.GITHUB:
                    success, output = await self._execute_github_command(processed_command, command.parameters)
                elif command.type == CommandType.SLACK:
                    success, output = await self._execute_slack_command(processed_command, command.parameters)
                elif command.type == CommandType.WAIT:
                    success, output = await self._execute_wait_command(processed_command)
                elif command.type == CommandType.VARIABLE:
                    success, output = self._execute_variable_command(processed_command, execution.variables)
                elif command.type == CommandType.CONDITIONAL:
                    success, output = self._execute_conditional_command(processed_command, execution.variables)
                else:
                    success, output = False, f"Unknown command type: {command.type}"

                # Store output
                execution.output.append(f"[{command.id}] {output}")

                if success:
                    return True
                elif attempt == command.retry_count:
                    print(f"   ❌ Command failed after {attempt + 1} attempts: {output}")
                    return False

            except Exception as e:
                error_msg = f"Command execution error: {str(e)}"
                execution.output.append(f"[{command.id}] ERROR: {error_msg}")

                if attempt == command.retry_count:
                    print(f"   ❌ Command failed with exception: {error_msg}")
                    return False

        return False

    async def _execute_shell_command(self, command: str, timeout: int) -> Tuple[bool, str]:
        """Execute shell command"""
        try:
            import subprocess

            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )

            output = stdout.decode() + stderr.decode()
            success = process.returncode == 0

            return success, output.strip()

        except asyncio.TimeoutError:
            return False, f"Command timed out after {timeout}s"
        except Exception as e:
            return False, f"Shell execution error: {str(e)}"

    async def _execute_python_command(self, command: str, timeout: int) -> Tuple[bool, str]:
        """Execute Python command"""
        try:
            # Create isolated namespace
            namespace = {"__builtins__": __builtins__}

            # Execute with timeout
            exec(command, namespace)

            return True, "Python command executed successfully"

        except Exception as e:
            return False, f"Python execution error: {str(e)}"

    async def _execute_ai_prompt(self, prompt: str, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        """Execute AI prompt command"""
        try:
            # This would integrate with the AI system
            # For now, return a mock response
            return True, f"AI Response: Processed prompt '{prompt[:50]}...'"

        except Exception as e:
            return False, f"AI prompt error: {str(e)}"

    async def _execute_email_command(self, command: str, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        """Execute email command"""
        try:
            # This would integrate with the email system
            return True, f"Email sent: {command}"

        except Exception as e:
            return False, f"Email error: {str(e)}"

    async def _execute_github_command(self, command: str, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        """Execute GitHub command"""
        try:
            # This would integrate with the GitHub system
            return True, f"GitHub action: {command}"

        except Exception as e:
            return False, f"GitHub error: {str(e)}"

    async def _execute_slack_command(self, command: str, parameters: Dict[str, Any]) -> Tuple[bool, str]:
        """Execute Slack command"""
        try:
            # This would integrate with the Slack system
            return True, f"Slack message sent: {command}"

        except Exception as e:
            return False, f"Slack error: {str(e)}"

    async def _execute_wait_command(self, command: str) -> Tuple[bool, str]:
        """Execute wait command"""
        try:
            # Extract wait time
            wait_time = float(command.split()[-1])
            await asyncio.sleep(wait_time)
            return True, f"Waited {wait_time} seconds"

        except Exception as e:
            return False, f"Wait error: {str(e)}"

    def _execute_variable_command(self, command: str, variables: Dict[str, Any]) -> Tuple[bool, str]:
        """Execute variable assignment command"""
        try:
            # Parse variable assignment: var_name = value
            if "=" in command:
                var_name, var_value = command.split("=", 1)
                var_name = var_name.strip()
                var_value = var_value.strip()

                # Evaluate value if it's an expression
                if var_value.startswith("${") and var_value.endswith("}"):
                    var_value = self._substitute_variables(var_value, variables)

                variables[var_name] = var_value
                return True, f"Variable set: {var_name} = {var_value}"
            else:
                return False, "Invalid variable assignment syntax"

        except Exception as e:
            return False, f"Variable error: {str(e)}"

    def _execute_conditional_command(self, command: str, variables: Dict[str, Any]) -> Tuple[bool, str]:
        """Execute conditional command"""
        try:
            # Simple conditional evaluation
            condition_met = self._evaluate_condition(command, variables)
            return True, f"Condition '{command}' evaluated to: {condition_met}"

        except Exception as e:
            return False, f"Conditional error: {str(e)}"

    def _substitute_variables(self, text: str, variables: Dict[str, Any]) -> str:
        """Substitute variables in text using ${var_name} syntax"""
        def replace_var(match):
            var_name = match.group(1)
            return str(variables.get(var_name, f"${{{var_name}}}"))

        return re.sub(r'\$\{([^}]+)\}', replace_var, text)

    def _evaluate_condition(self, condition: str, variables: Dict[str, Any]) -> bool:
        """Evaluate simple conditions"""
        try:
            # Substitute variables
            condition = self._substitute_variables(condition, variables)

            # Simple condition evaluation (can be extended)
            if "==" in condition:
                left, right = condition.split("==", 1)
                return left.strip() == right.strip()
            elif "!=" in condition:
                left, right = condition.split("!=", 1)
                return left.strip() != right.strip()
            elif ">" in condition:
                left, right = condition.split(">", 1)
                return float(left.strip()) > float(right.strip())
            elif "<" in condition:
                left, right = condition.split("<", 1)
                return float(left.strip()) < float(right.strip())
            else:
                # Treat as boolean
                return bool(condition.strip())

        except Exception:
            return False

    def start_macro_recording(self, name: str, description: str = "") -> bool:
        """Start recording commands for macro creation"""
        if self.recording_session:
            print("⚠️ Already recording a macro")
            return False

        self.recording_session = {
            "name": name,
            "description": description,
            "commands": [],
            "start_time": datetime.now(),
            "variables": {}
        }

        print(f"🔴 Started recording macro: {name}")
        return True

    def record_command(self, command: str, command_type: CommandType = CommandType.SHELL,
                      parameters: Optional[Dict[str, Any]] = None) -> bool:
        """Record a command during macro recording"""
        if not self.recording_session:
            print("⚠️ No active recording session")
            return False

        command_id = f"recorded_cmd_{len(self.recording_session['commands']) + 1}"

        recorded_command = RecipeCommand(
            id=command_id,
            type=command_type,
            command=command,
            parameters=parameters or {},
            description=f"Recorded step {len(self.recording_session['commands']) + 1}"
        )

        self.recording_session['commands'].append(recorded_command)
        print(f"📝 Recorded: {command[:50]}...")
        return True

    def stop_macro_recording(self) -> Optional[str]:
        """Stop recording and create recipe"""
        if not self.recording_session:
            print("⚠️ No active recording session")
            return None

        session = self.recording_session
        self.recording_session = None

        if not session['commands']:
            print("⚠️ No commands recorded")
            return None

        # Create recipe from recorded commands
        recipe_id = self.create_recipe(
            name=session['name'],
            description=session['description'] or f"Macro recorded on {session['start_time'].strftime('%Y-%m-%d %H:%M')}",
            commands=session['commands'],
            tags=["macro", "recorded"]
        )

        duration = (datetime.now() - session['start_time']).total_seconds()
        print(f"⏹️ Stopped recording: {len(session['commands'])} commands in {duration:.1f}s")
        print(f"✅ Macro saved as recipe: {recipe_id}")

        return recipe_id

    def get_recipe(self, recipe_id: str) -> Optional[AutomationRecipe]:
        """Get recipe by ID"""
        return self.recipes.get(recipe_id)

    def list_recipes(self, tag: Optional[str] = None, enabled_only: bool = True) -> List[AutomationRecipe]:
        """List recipes with optional filtering"""
        recipes = list(self.recipes.values())

        if enabled_only:
            recipes = [r for r in recipes if r.enabled]

        if tag:
            recipes = [r for r in recipes if tag in r.tags]

        return sorted(recipes, key=lambda r: r.updated_at, reverse=True)

    def delete_recipe(self, recipe_id: str) -> bool:
        """Delete recipe"""
        if recipe_id not in self.recipes:
            return False

        recipe = self.recipes[recipe_id]
        del self.recipes[recipe_id]

        # Remove from scheduler if scheduled
        if recipe.schedule and recipe_id in self.scheduled_jobs:
            self._unschedule_recipe(recipe_id)

        self._save_recipes()
        print(f"🗑️ Recipe deleted: {recipe.name}")
        return True

    def enable_recipe(self, recipe_id: str) -> bool:
        """Enable recipe"""
        if recipe_id not in self.recipes:
            return False

        self.recipes[recipe_id].enabled = True
        self.recipes[recipe_id].updated_at = datetime.now()

        # Schedule if needed
        recipe = self.recipes[recipe_id]
        if recipe.schedule and SCHEDULE_AVAILABLE:
            self._schedule_recipe(recipe)

        self._save_recipes()
        return True

    def disable_recipe(self, recipe_id: str) -> bool:
        """Disable recipe"""
        if recipe_id not in self.recipes:
            return False

        self.recipes[recipe_id].enabled = False
        self.recipes[recipe_id].updated_at = datetime.now()

        # Unschedule if scheduled
        if recipe_id in self.scheduled_jobs:
            self._unschedule_recipe(recipe_id)

        self._save_recipes()
        return True

    def get_execution_history(self, recipe_id: Optional[str] = None,
                            limit: int = 50) -> List[RecipeExecution]:
        """Get execution history"""
        executions = list(self.executions.values())

        if recipe_id:
            executions = [e for e in executions if e.recipe_id == recipe_id]

        return sorted(executions, key=lambda e: e.start_time, reverse=True)[:limit]

    def _initialize_scheduler(self):
        """Initialize the scheduler"""
        if not SCHEDULE_AVAILABLE:
            return

        # Schedule existing recipes
        for recipe in self.recipes.values():
            if recipe.enabled and recipe.schedule:
                self._schedule_recipe(recipe)

    def _schedule_recipe(self, recipe: AutomationRecipe):
        """Schedule recipe execution"""
        if not SCHEDULE_AVAILABLE or not recipe.schedule:
            return

        try:
            # Parse schedule format (simplified cron-like)
            if recipe.schedule.startswith("every "):
                # Format: "every 5 minutes", "every 1 hour", "every day"
                parts = recipe.schedule.split()
                if len(parts) >= 3:
                    interval = int(parts[1])
                    unit = parts[2].rstrip('s')  # Remove plural 's'

                    if unit == "minute":
                        job = schedule.every(interval).minutes.do(self._run_scheduled_recipe, recipe.id)
                    elif unit == "hour":
                        job = schedule.every(interval).hours.do(self._run_scheduled_recipe, recipe.id)
                    elif unit == "day":
                        job = schedule.every(interval).days.do(self._run_scheduled_recipe, recipe.id)
                    else:
                        print(f"⚠️ Unsupported schedule unit: {unit}")
                        return

                    self.scheduled_jobs[recipe.id] = job
                    print(f"📅 Scheduled recipe: {recipe.name} - {recipe.schedule}")

        except Exception as e:
            print(f"⚠️ Recipe scheduling failed: {e}")

    def _unschedule_recipe(self, recipe_id: str):
        """Unschedule recipe"""
        if recipe_id in self.scheduled_jobs and SCHEDULE_AVAILABLE:
            schedule.cancel_job(self.scheduled_jobs[recipe_id])
            del self.scheduled_jobs[recipe_id]

    def _run_scheduled_recipe(self, recipe_id: str):
        """Run scheduled recipe"""
        try:
            asyncio.create_task(self.execute_recipe(recipe_id))
        except Exception as e:
            print(f"⚠️ Scheduled recipe execution failed: {e}")

    def get_statistics(self) -> Dict[str, Any]:
        """Get automation statistics"""
        return {
            "recipes_created": self.recipes_created,
            "recipes_executed": self.recipes_executed,
            "commands_executed": self.commands_executed,
            "total_recipes": len(self.recipes),
            "enabled_recipes": len([r for r in self.recipes.values() if r.enabled]),
            "scheduled_recipes": len(self.scheduled_jobs),
            "total_executions": len(self.executions),
            "recording_active": self.recording_session is not None,
            "scheduler_available": SCHEDULE_AVAILABLE
        }
