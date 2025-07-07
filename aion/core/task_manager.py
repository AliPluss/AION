"""
🚀 AION Advanced Task Manager
Professional task management system with scheduling and parallel execution

This module provides comprehensive task management capabilities including:
- Multi-threaded task execution with dependency resolution
- Advanced scheduling with cron-like functionality
- Task persistence and recovery mechanisms
- Priority-based task queuing and execution
- Real-time monitoring and statistics
- Comprehensive error handling and logging
- Resource management and optimization

Features:
- Parallel execution with configurable thread pools
- Task dependencies and execution ordering
- Scheduled tasks with flexible timing options
- Task persistence across system restarts
- Real-time status monitoring and reporting
- Advanced error handling and retry mechanisms
- Resource usage tracking and optimization
- Comprehensive logging and audit trails

مدير المهام المتقدم مع الجدولة والتنفيذ المتوازي
"""

import json
import threading
import time
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from concurrent.futures import ThreadPoolExecutor, Future
import queue

class TaskStatus(Enum):
    """
    Task execution status enumeration

    Defines all possible states a task can be in during its lifecycle:
    - PENDING: Task is queued and waiting for execution
    - RUNNING: Task is currently being executed
    - COMPLETED: Task finished successfully
    - FAILED: Task encountered an error during execution
    - CANCELLED: Task was manually cancelled before completion
    - SCHEDULED: Task is scheduled for future execution
    - PAUSED: Task execution is temporarily suspended

    حالات المهام - Task states in Arabic
    """
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SCHEDULED = "scheduled"
    PAUSED = "paused"

class TaskPriority(Enum):
    """أولويات المهام"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4

class TaskType(Enum):
    """أنواع المهام"""
    FUNCTION = "function"
    COMMAND = "command"
    SCRIPT = "script"
    HTTP_REQUEST = "http_request"
    FILE_OPERATION = "file_operation"

@dataclass
class TaskResult:
    """نتيجة تنفيذ مهمة"""
    task_id: str
    status: TaskStatus
    result: Any = None
    error: Optional[str] = None
    output: Optional[str] = None
    execution_time: Optional[float] = None
    memory_usage: Optional[int] = None
    cpu_usage: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

@dataclass
class Task:
    """مهمة"""
    id: str
    name: str
    description: str
    task_type: TaskType
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    scheduled_time: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    timeout: Optional[float] = None
    max_retries: int = 0
    retry_count: int = 0
    dependencies: List[str] = None
    tags: List[str] = None
    metadata: Dict[str, Any] = None

    # معاملات التنفيذ
    function: Optional[Callable] = None
    command: Optional[str] = None
    script_path: Optional[str] = None
    http_url: Optional[str] = None
    file_path: Optional[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}

class AdvancedTaskManager:
    """مدير المهام المتقدم"""

    def __init__(self, data_dir: Optional[Path] = None, max_workers: int = 4):
        self.data_dir = data_dir or Path.cwd() / "task_data"
        self.data_dir.mkdir(exist_ok=True)

        self.logger = logging.getLogger(__name__)

        # ملفات البيانات
        self.tasks_file = self.data_dir / "tasks.json"
        self.results_file = self.data_dir / "results.json"
        self.config_file = self.data_dir / "task_config.json"

        # بيانات المهام
        self.tasks: Dict[str, Task] = {}
        self.results: Dict[str, TaskResult] = {}
        self.running_tasks: Dict[str, Future] = {}

        # إعدادات التنفيذ
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.scheduler_thread = None
        self.scheduler_running = False

        # قوائم انتظار المهام
        self.task_queue = queue.PriorityQueue()
        self.completed_queue = queue.Queue()

        # إعدادات النظام
        self.lock = threading.RLock()
        self.auto_save = True
        self.cleanup_completed = True
        self.max_completed_tasks = 1000

        # تحميل البيانات
        self._load_data()

        # بدء المجدول
        self._start_scheduler()
    
    def _load_config(self) -> Dict[str, Any]:
        """تحميل إعدادات المدير"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # إعدادات افتراضية
            default_config = {
                "auto_save": True,
                "save_interval": 60,  # ثواني
                "max_results_history": 1000,
                "default_timeout": 300,  # 5 دقائق
                "retry_delay": 5,  # ثواني
                "cleanup_completed_after_days": 7,
                "enable_logging": True,
                "log_level": "INFO"
            }
            
            self._save_config(default_config)
            return default_config
            
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return {}
    
    def _save_config(self, config: Dict[str, Any]):
        """حفظ إعدادات المدير"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
    
    def _load_data(self):
        """تحميل بيانات المهام"""
        try:
            # تحميل المهام
            if self.tasks_file.exists():
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    tasks_data = json.load(f)

                for task_id, task_data in tasks_data.items():
                    # تحويل التواريخ والenums
                    task_data["created_at"] = datetime.fromisoformat(task_data["created_at"])
                    if task_data.get("scheduled_time"):
                        task_data["scheduled_time"] = datetime.fromisoformat(task_data["scheduled_time"])
                    if task_data.get("started_at"):
                        task_data["started_at"] = datetime.fromisoformat(task_data["started_at"])
                    if task_data.get("completed_at"):
                        task_data["completed_at"] = datetime.fromisoformat(task_data["completed_at"])

                    # تحويل enums بأمان
                    try:
                        if isinstance(task_data["task_type"], str):
                            task_data["task_type"] = TaskType[task_data["task_type"].split('.')[-1]]
                        else:
                            task_data["task_type"] = TaskType(task_data["task_type"])

                        if isinstance(task_data["status"], str):
                            task_data["status"] = TaskStatus[task_data["status"].split('.')[-1]]
                        else:
                            task_data["status"] = TaskStatus(task_data["status"])

                        if isinstance(task_data["priority"], str):
                            task_data["priority"] = TaskPriority[task_data["priority"].split('.')[-1]]
                        else:
                            task_data["priority"] = TaskPriority(task_data["priority"])
                    except (KeyError, ValueError) as e:
                        self.logger.warning(f"Error converting enums for task {task_id}: {e}")
                        continue

                    # إزالة الدوال (لا يمكن تسلسلها)
                    task_data.pop("function", None)

                    task = Task(**task_data)
                    self.tasks[task_id] = task
            
            # تحميل النتائج
            if self.results_file.exists():
                with open(self.results_file, 'r', encoding='utf-8') as f:
                    results_data = json.load(f)

                for result_id, result_data in results_data.items():
                    # تحويل التواريخ والenums
                    if result_data.get("started_at"):
                        result_data["started_at"] = datetime.fromisoformat(result_data["started_at"])
                    if result_data.get("completed_at"):
                        result_data["completed_at"] = datetime.fromisoformat(result_data["completed_at"])

                    result_data["status"] = TaskStatus(result_data["status"])

                    result = TaskResult(**result_data)
                    self.results[result_id] = result
                    
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
    
    def _save_data(self):
        """حفظ بيانات المهام"""
        try:
            with self.lock:
                # حفظ المهام
                tasks_data = {}
                for task_id, task in self.tasks.items():
                    task_dict = asdict(task)
                    # إزالة الدوال
                    task_dict.pop("function", None)
                    tasks_data[task_id] = task_dict

                with open(self.tasks_file, 'w', encoding='utf-8') as f:
                    json.dump(tasks_data, f, indent=2, ensure_ascii=False, default=str)

                # حفظ النتائج
                results_data = {}
                for result_id, result in self.results.items():
                    results_data[result_id] = asdict(result)

                with open(self.results_file, 'w', encoding='utf-8') as f:
                    json.dump(results_data, f, indent=2, ensure_ascii=False, default=str)

        except Exception as e:
            self.logger.error(f"Error saving task data: {e}")
    
    def _start_scheduler(self):
        """بدء مجدول المهام"""
        try:
            if not self.scheduler_running:
                self.scheduler_running = True
                self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
                self.scheduler_thread.start()

        except Exception as e:
            self.logger.error(f"Error starting scheduler: {e}")

    def _scheduler_loop(self):
        """حلقة المجدول الرئيسية"""
        while self.scheduler_running:
            try:
                current_time = datetime.now()

                # فحص المهام المجدولة
                for task_id, task in list(self.tasks.items()):
                    if (task.status == TaskStatus.SCHEDULED and
                        task.scheduled_time and
                        task.scheduled_time <= current_time):

                        # تحويل المهمة إلى pending
                        task.status = TaskStatus.PENDING
                        self._add_to_queue(task)

                # تنفيذ المهام من القائمة
                self._process_task_queue()

                # تنظيف المهام المكتملة
                if self.cleanup_completed:
                    self._cleanup_completed_tasks()

                # حفظ البيانات
                if self.auto_save:
                    self._save_data()

                # انتظار قبل التكرار
                time.sleep(1)

            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {e}")
                time.sleep(5)

    def create_task(self, name: str, description: str, task_type: TaskType,
                   priority: TaskPriority = TaskPriority.NORMAL,
                   scheduled_time: Optional[datetime] = None,
                   function: Optional[Callable] = None,
                   command: Optional[str] = None,
                   script_path: Optional[str] = None,
                   timeout: Optional[float] = None,
                   max_retries: int = 0,
                   dependencies: Optional[List[str]] = None,
                   tags: Optional[List[str]] = None,
                   metadata: Optional[Dict[str, Any]] = None) -> str:
        """إنشاء مهمة جديدة"""
        
        task_id = str(uuid.uuid4())
        
        # تحديد الحالة الأولية
        status = TaskStatus.SCHEDULED if scheduled_time else TaskStatus.PENDING
        
        task = Task(
            id=task_id,
            name=name,
            description=description,
            task_type=task_type,
            priority=priority,
            status=status,
            created_at=datetime.now(),
            scheduled_time=scheduled_time,
            max_retries=max_retries,
            timeout=timeout,
            dependencies=dependencies or [],
            tags=tags or [],
            metadata=metadata or {},
            function=function,
            command=command,
            script_path=script_path
        )
        
        self.tasks[task_id] = task
        
        self.tasks[task_id] = task

        # إضافة إلى القائمة إذا كانت جاهزة للتنفيذ
        if status == TaskStatus.PENDING:
            self._add_to_queue(task)

        # حفظ تلقائي
        if self.auto_save:
            self._save_data()

        self.logger.info(f"Task created: {name} ({task_id})")
        return task_id
    
    def execute_task(self, task_id: str) -> bool:
        """تنفيذ مهمة"""
        try:
            if task_id not in self.tasks:
                self.logger.error(f"Task {task_id} not found")
                return False
            
            task = self.tasks[task_id]
            
            # فحص التبعيات
            if not self._check_dependencies(task):
                self.logger.warning(f"Dependencies not met for task {task_id}")
                return False
            
            # فحص إذا كانت المهمة قيد التنفيذ
            if task_id in self.running_tasks:
                self.logger.warning(f"Task {task_id} is already running")
                return False
            
            # تحديث حالة المهمة
            task.status = TaskStatus.RUNNING
            
            # تنفيذ المهمة في thread منفصل
            future = self.executor.submit(self._execute_task_worker, task)
            self.running_tasks[task_id] = future
            
            # إضافة callback للتنظيف
            future.add_done_callback(lambda f: self._task_completed(task_id, f))
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error executing task {task_id}: {e}")
            return False
    
    def _check_dependencies(self, task: Task) -> bool:
        """فحص تبعيات المهمة"""
        for dep_id in task.dependencies:
            if dep_id not in self.results:
                return False
            
            dep_result = self.results[dep_id]
            if dep_result.status != TaskStatus.COMPLETED:
                return False
        
        return True
    
    def _execute_task_worker(self, task: Task) -> TaskResult:
        """تنفيذ المهمة في worker thread"""
        start_time = datetime.now()
        result = TaskResult(
            task_id=task.id,
            status=TaskStatus.RUNNING,
            started_at=start_time
        )
        
        try:
            # تنفيذ حسب نوع المهمة
            if task.task_type == TaskType.FUNCTION and task.function:
                output = task.function()
                result.result = output
                result.status = TaskStatus.COMPLETED
                
            elif task.task_type == TaskType.COMMAND and task.command:
                import subprocess
                process = subprocess.run(
                    task.command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=task.timeout
                )
                result.result = process.returncode
                result.output = process.stdout
                if process.stderr:
                    result.error = process.stderr
                
                result.status = TaskStatus.COMPLETED if process.returncode == 0 else TaskStatus.FAILED
                
            elif task.task_type == TaskType.SCRIPT and task.script_path:
                import subprocess
                process = subprocess.run(
                    ["python", task.script_path],
                    capture_output=True,
                    text=True,
                    timeout=task.timeout
                )
                result.result = process.returncode
                result.output = process.stdout
                if process.stderr:
                    result.error = process.stderr
                
                result.status = TaskStatus.COMPLETED if process.returncode == 0 else TaskStatus.FAILED
                
            else:
                result.status = TaskStatus.FAILED
                result.error = f"Unsupported task type: {task.task_type}"
            
        except Exception as e:
            result.status = TaskStatus.FAILED
            result.error = str(e)
            self.logger.error(f"Task {task.id} failed: {e}")
        
        finally:
            result.completed_at = datetime.now()
            result.execution_time = (result.completed_at - result.started_at).total_seconds()
        
        return result
    
    def _task_completed(self, task_id: str, future: Future):
        """معالجة اكتمال المهمة"""
        try:
            # الحصول على النتيجة
            result = future.result()
            
            # تحديث حالة المهمة
            if task_id in self.tasks:
                self.tasks[task_id].status = result.status
            
            # حفظ النتيجة
            self.results[task_id] = result
            
            # إزالة من المهام قيد التنفيذ
            if task_id in self.running_tasks:
                del self.running_tasks[task_id]
            
            # إعادة المحاولة في حالة الفشل
            if result.status == TaskStatus.FAILED and task_id in self.tasks:
                task = self.tasks[task_id]
                if task.retry_count < task.max_retries:
                    task.retry_count += 1
                    task.status = TaskStatus.PENDING
                    
                    # إعادة جدولة المهمة
                    retry_delay = self.config.get("retry_delay", 5)
                    retry_time = datetime.now() + timedelta(seconds=retry_delay)
                    task.scheduled_time = retry_time
                    
                    self.logger.info(f"Retrying task {task_id} (attempt {task.retry_count}/{task.max_retries})")
            
            # حفظ تلقائي
            if self.config.get("auto_save", True):
                self._save_data()
            
            self.logger.info(f"Task {task_id} completed with status: {result.status}")
            
        except Exception as e:
            self.logger.error(f"Error handling task completion {task_id}: {e}")
    
    def start_scheduler(self):
        """بدء جدولة المهام"""
        if self.scheduler_running:
            return

        self.scheduler_running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()

        self.logger.info("Task scheduler started")

    def stop_scheduler(self):
        """إيقاف جدولة المهام"""
        self.scheduler_running = False

        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5.0)

        self.logger.info("Task scheduler stopped")

    def _scheduler_loop(self):
        """حلقة جدولة المهام"""
        while self.scheduler_running:
            try:
                current_time = datetime.now()
                
                # البحث عن المهام المجدولة
                for task_id, task in self.tasks.items():
                    if (task.status == TaskStatus.SCHEDULED and 
                        task.scheduled_time and 
                        task.scheduled_time <= current_time):
                        
                        # تنفيذ المهمة
                        self.execute_task(task_id)
                
                # البحث عن المهام المعلقة بأولوية عالية
                pending_tasks = [
                    (task_id, task) for task_id, task in self.tasks.items()
                    if task.status == TaskStatus.PENDING
                ]
                
                # ترتيب حسب الأولوية
                pending_tasks.sort(key=lambda x: x[1].priority.value, reverse=True)
                
                # تنفيذ المهام المعلقة إذا كان هناك مساحة
                available_workers = self.max_workers - len(self.running_tasks)
                for i in range(min(available_workers, len(pending_tasks))):
                    task_id, task = pending_tasks[i]
                    self.execute_task(task_id)
                
                time.sleep(1)  # فحص كل ثانية
                
            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {e}")
                time.sleep(5)
    
    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """الحصول على حالة المهمة"""
        if task_id in self.tasks:
            return self.tasks[task_id].status
        return None
    
    def get_task_result(self, task_id: str) -> Optional[TaskResult]:
        """الحصول على نتيجة المهمة"""
        return self.results.get(task_id)
    
    def cancel_task(self, task_id: str) -> bool:
        """إلغاء مهمة"""
        try:
            if task_id in self.running_tasks:
                # إلغاء المهمة قيد التنفيذ
                future = self.running_tasks[task_id]
                future.cancel()
                del self.running_tasks[task_id]
            
            if task_id in self.tasks:
                self.tasks[task_id].status = TaskStatus.CANCELLED
            
            self.logger.info(f"Task {task_id} cancelled")
            return True
            
        except Exception as e:
            self.logger.error(f"Error cancelling task {task_id}: {e}")
            return False

    def pause_task(self, task_id: str) -> bool:
        """إيقاف مهمة مؤقتاً"""
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                if task.status in [TaskStatus.PENDING, TaskStatus.SCHEDULED]:
                    task.status = TaskStatus.PAUSED
                    self.logger.info(f"Task {task_id} paused")
                    return True
                else:
                    self.logger.warning(f"Cannot pause task {task_id} with status {task.status}")
                    return False

            return False

        except Exception as e:
            self.logger.error(f"Error pausing task {task_id}: {e}")
            return False

    def resume_task(self, task_id: str) -> bool:
        """استئناف مهمة متوقفة"""
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                if task.status == TaskStatus.PAUSED:
                    task.status = TaskStatus.PENDING
                    self.logger.info(f"Task {task_id} resumed")
                    return True
                else:
                    self.logger.warning(f"Cannot resume task {task_id} with status {task.status}")
                    return False

            return False

        except Exception as e:
            self.logger.error(f"Error resuming task {task_id}: {e}")
            return False

    def list_tasks(self, status_filter: Optional[TaskStatus] = None,
                   priority_filter: Optional[TaskPriority] = None,
                   tag_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """عرض قائمة المهام مع فلترة"""
        try:
            filtered_tasks = []

            for task_id, task in self.tasks.items():
                # تطبيق الفلاتر
                if status_filter and task.status != status_filter:
                    continue

                if priority_filter and task.priority != priority_filter:
                    continue

                if tag_filter and tag_filter not in task.tags:
                    continue

                # إضافة معلومات إضافية
                task_info = asdict(task)
                task_info["id"] = task_id

                # إضافة معلومات النتيجة إذا كانت متوفرة
                if task_id in self.results:
                    result = self.results[task_id]
                    task_info["execution_time"] = result.execution_time
                    task_info["last_error"] = result.error

                # إزالة الحقول غير القابلة للتسلسل
                task_info.pop("function", None)

                filtered_tasks.append(task_info)

            # ترتيب حسب الأولوية ثم تاريخ الإنشاء
            filtered_tasks.sort(key=lambda x: (x["priority"], x["created_date"]), reverse=True)

            return filtered_tasks

        except Exception as e:
            self.logger.error(f"Error listing tasks: {e}")
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات المهام"""
        try:
            stats = {
                "total_tasks": len(self.tasks),
                "running_tasks": len(self.running_tasks),
                "by_status": {},
                "by_priority": {},
                "by_type": {},
                "execution_stats": {
                    "total_executions": len(self.results),
                    "successful_executions": 0,
                    "failed_executions": 0,
                    "average_execution_time": 0.0,
                    "total_execution_time": 0.0
                }
            }

            # إحصائيات حسب الحالة
            for task in self.tasks.values():
                status = task.status.value
                stats["by_status"][status] = stats["by_status"].get(status, 0) + 1

                priority = task.priority.name
                stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1

                task_type = task.task_type.value
                stats["by_type"][task_type] = stats["by_type"].get(task_type, 0) + 1

            # إحصائيات التنفيذ
            execution_times = []
            for result in self.results.values():
                if result.status == TaskStatus.COMPLETED:
                    stats["execution_stats"]["successful_executions"] += 1
                    if result.execution_time is not None:
                        execution_times.append(result.execution_time)
                elif result.status == TaskStatus.FAILED:
                    stats["execution_stats"]["failed_executions"] += 1

                if result.execution_time is not None:
                    stats["execution_stats"]["total_execution_time"] += result.execution_time

            if execution_times:
                stats["execution_stats"]["average_execution_time"] = sum(execution_times) / len(execution_times)

            # إضافة إحصائيات مفصلة
            stats.update({
                "completed_tasks": stats["by_status"].get("completed", 0),
                "failed_tasks": stats["by_status"].get("failed", 0),
                "pending_tasks": stats["by_status"].get("pending", 0),
                "scheduled_tasks": stats["by_status"].get("scheduled", 0)
            })

            return stats

        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
            return {}

    def get_tasks_by_priority(self, priority: TaskPriority) -> List[Task]:
        """الحصول على المهام حسب الأولوية"""
        try:
            return [task for task in self.tasks.values() if task.priority == priority]
        except Exception as e:
            self.logger.error(f"Error getting tasks by priority: {e}")
            return []

    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """الحصول على المهام حسب الحالة"""
        try:
            return [task for task in self.tasks.values() if task.status == status]
        except Exception as e:
            self.logger.error(f"Error getting tasks by status: {e}")
            return []

    def pause_task(self, task_id: str) -> bool:
        """إيقاف مؤقت لمهمة"""
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                if task.status == TaskStatus.RUNNING:
                    # في التطبيق الحقيقي، نحتاج لإيقاف thread
                    # هنا نغير الحالة فقط للاختبار
                    task.status = TaskStatus.PENDING
                    self.logger.info(f"Task {task_id} paused")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Error pausing task: {e}")
            return False

    def cleanup_completed_tasks(self, days: int = None) -> int:
        """تنظيف المهام المكتملة القديمة"""
        try:
            days = days or self.config.get("cleanup_completed_after_days", 7)
            cutoff_date = datetime.now() - timedelta(days=days)

            tasks_to_remove = []
            for task_id, task in self.tasks.items():
                if (task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED] and
                    task.created_date < cutoff_date):
                    tasks_to_remove.append(task_id)

            # إزالة المهام
            for task_id in tasks_to_remove:
                del self.tasks[task_id]
                if task_id in self.results:
                    del self.results[task_id]

            # حفظ البيانات
            if self.config.get("auto_save", True):
                self._save_data()

            self.logger.info(f"Cleaned up {len(tasks_to_remove)} completed tasks")
            return len(tasks_to_remove)

        except Exception as e:
            self.logger.error(f"Error cleaning up tasks: {e}")
            return 0

    def export_tasks(self, export_path: Path, include_results: bool = True) -> bool:
        """تصدير المهام والنتائج"""
        try:
            export_data = {
                "tasks": {},
                "results": {} if include_results else {},
                "statistics": self.get_statistics(),
                "export_timestamp": datetime.now().isoformat(),
                "config": self.config
            }

            # تصدير المهام
            for task_id, task in self.tasks.items():
                task_dict = asdict(task)
                task_dict.pop("function", None)  # إزالة الدوال غير القابلة للتسلسل
                export_data["tasks"][task_id] = task_dict

            # تصدير النتائج
            if include_results:
                for result_id, result in self.results.items():
                    export_data["results"][result_id] = asdict(result)

            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)

            self.logger.info(f"Tasks exported to {export_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error exporting tasks: {e}")
            return False

    def import_tasks(self, import_path: Path) -> bool:
        """استيراد المهام من ملف"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)

            # استيراد المهام
            if "tasks" in import_data:
                for task_id, task_data in import_data["tasks"].items():
                    # تحويل التواريخ
                    task_data["created_date"] = datetime.fromisoformat(task_data["created_date"])
                    if task_data.get("scheduled_time"):
                        task_data["scheduled_time"] = datetime.fromisoformat(task_data["scheduled_time"])

                    # تحويل enums
                    task_data["task_type"] = TaskType(task_data["task_type"])
                    task_data["priority"] = TaskPriority(task_data["priority"])
                    task_data["status"] = TaskStatus(task_data["status"])

                    task = Task(**task_data)
                    self.tasks[task_id] = task

            # استيراد النتائج
            if "results" in import_data:
                for result_id, result_data in import_data["results"].items():
                    # تحويل التواريخ
                    if result_data.get("started_at"):
                        result_data["started_at"] = datetime.fromisoformat(result_data["started_at"])
                    if result_data.get("completed_at"):
                        result_data["completed_at"] = datetime.fromisoformat(result_data["completed_at"])

                    # تحويل enums
                    result_data["status"] = TaskStatus(result_data["status"])

                    result = TaskResult(**result_data)
                    self.results[result_id] = result

            # حفظ البيانات
            if self.config.get("auto_save", True):
                self._save_data()

            self.logger.info(f"Tasks imported from {import_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error importing tasks: {e}")
            return False

    def create_recurring_task(self, name: str, description: str, task_type: TaskType,
                             schedule_pattern: str, **kwargs) -> str:
        """إنشاء مهمة متكررة"""
        try:
            # إنشاء المهمة الأساسية
            task_id = self.create_task(name, description, task_type, **kwargs)

            # إضافة معلومات التكرار
            if task_id in self.tasks:
                task = self.tasks[task_id]
                task.metadata["recurring"] = True
                task.metadata["schedule_pattern"] = schedule_pattern

                # جدولة المهمة الأولى
                next_run = self._calculate_next_run(schedule_pattern)
                if next_run:
                    task.scheduled_time = next_run
                    task.status = TaskStatus.SCHEDULED

            return task_id

        except Exception as e:
            self.logger.error(f"Error creating recurring task: {e}")
            return ""

    def _calculate_next_run(self, schedule_pattern: str) -> Optional[datetime]:
        """حساب موعد التنفيذ التالي للمهمة المتكررة"""
        try:
            now = datetime.now()

            if schedule_pattern == "daily":
                return now + timedelta(days=1)
            elif schedule_pattern == "hourly":
                return now + timedelta(hours=1)
            elif schedule_pattern == "weekly":
                return now + timedelta(weeks=1)
            elif schedule_pattern.startswith("every_"):
                # مثال: every_30_minutes
                parts = schedule_pattern.split("_")
                if len(parts) == 3:
                    interval = int(parts[1])
                    unit = parts[2]

                    if unit == "minutes":
                        return now + timedelta(minutes=interval)
                    elif unit == "hours":
                        return now + timedelta(hours=interval)
                    elif unit == "days":
                        return now + timedelta(days=interval)

            return None

        except Exception as e:
            self.logger.error(f"Error calculating next run: {e}")
            return None

    def shutdown(self):
        """إغلاق مدير المهام"""
        try:
            # إيقاف الجدولة
            self.stop_scheduler()

            # إلغاء المهام قيد التنفيذ
            for task_id in list(self.running_tasks.keys()):
                self.cancel_task(task_id)

            # إغلاق executor
            self.executor.shutdown(wait=True)

            # حفظ البيانات النهائية
            self._save_data()

            self.logger.info("Task manager shutdown completed")

        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.shutdown()
        return False

    def _add_to_queue(self, task: Task):
        """إضافة مهمة إلى قائمة الانتظار"""
        try:
            # فحص التبعيات
            if self._check_dependencies(task):
                priority_value = -task.priority.value  # أولوية عكسية للقائمة
                self.task_queue.put((priority_value, task.created_at, task.id))

        except Exception as e:
            self.logger.error(f"Error adding task to queue: {e}")

    def _check_dependencies(self, task: Task) -> bool:
        """فحص تبعيات المهمة"""
        try:
            for dep_id in task.dependencies:
                if dep_id in self.tasks:
                    dep_task = self.tasks[dep_id]
                    if dep_task.status != TaskStatus.COMPLETED:
                        return False
                else:
                    # تبعية غير موجودة
                    return False

            return True

        except Exception as e:
            self.logger.error(f"Error checking dependencies: {e}")
            return False

    def _process_task_queue(self):
        """معالجة قائمة انتظار المهام"""
        try:
            while not self.task_queue.empty() and len(self.running_tasks) < self.max_workers:
                try:
                    _, _, task_id = self.task_queue.get_nowait()

                    if task_id in self.tasks and task_id not in self.running_tasks:
                        task = self.tasks[task_id]
                        if task.status == TaskStatus.PENDING:
                            self._execute_task_async(task)

                except queue.Empty:
                    break

        except Exception as e:
            self.logger.error(f"Error processing task queue: {e}")

    def _execute_task_async(self, task: Task):
        """تنفيذ مهمة بشكل غير متزامن"""
        try:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()

            # إرسال المهمة للتنفيذ
            future = self.executor.submit(self._execute_task, task)
            self.running_tasks[task.id] = future

            # إضافة callback للتعامل مع النتيجة
            future.add_done_callback(lambda f: self._task_completed(task.id, f))

        except Exception as e:
            self.logger.error(f"Error executing task async: {e}")
            task.status = TaskStatus.FAILED

    def _execute_task(self, task: Task) -> TaskResult:
        """تنفيذ مهمة"""
        start_time = time.time()
        result = TaskResult(
            task_id=task.id,
            status=TaskStatus.RUNNING,
            started_at=datetime.now()
        )

        try:
            # تنفيذ حسب نوع المهمة
            if task.task_type == TaskType.FUNCTION and task.function:
                result.result = task.function()
                result.status = TaskStatus.COMPLETED

            elif task.task_type == TaskType.COMMAND and task.command:
                import subprocess
                process_result = subprocess.run(
                    task.command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=task.timeout
                )

                result.output = process_result.stdout
                result.result = process_result.returncode

                if process_result.returncode == 0:
                    result.status = TaskStatus.COMPLETED
                else:
                    result.status = TaskStatus.FAILED
                    result.error = process_result.stderr

            elif task.task_type == TaskType.SCRIPT and task.script_path:
                with open(task.script_path, 'r', encoding='utf-8') as f:
                    script_content = f.read()

                # تنفيذ السكريبت (Python فقط للأمان)
                if task.script_path.endswith('.py'):
                    exec_globals = {}
                    exec(script_content, exec_globals)
                    result.result = exec_globals.get('result', 'Script executed')
                    result.status = TaskStatus.COMPLETED
                else:
                    raise ValueError(f"Unsupported script type: {task.script_path}")

            else:
                raise ValueError(f"Unsupported task type: {task.task_type}")

        except Exception as e:
            result.status = TaskStatus.FAILED
            result.error = str(e)

        finally:
            result.execution_time = time.time() - start_time
            result.completed_at = datetime.now()

        return result

    def _task_completed(self, task_id: str, future: Future):
        """معالجة اكتمال المهمة"""
        try:
            with self.lock:
                # إزالة من المهام الجارية
                if task_id in self.running_tasks:
                    del self.running_tasks[task_id]

                # الحصول على النتيجة
                try:
                    result = future.result()
                except Exception as e:
                    result = TaskResult(
                        task_id=task_id,
                        status=TaskStatus.FAILED,
                        error=str(e),
                        completed_at=datetime.now()
                    )

                # تحديث المهمة
                if task_id in self.tasks:
                    task = self.tasks[task_id]
                    task.status = result.status
                    task.completed_at = result.completed_at

                    # إعادة المحاولة في حالة الفشل
                    if (result.status == TaskStatus.FAILED and
                        task.retry_count < task.max_retries):

                        task.retry_count += 1
                        task.status = TaskStatus.PENDING
                        self._add_to_queue(task)

                # حفظ النتيجة
                self.results[task_id] = result

                # إضافة المهام التابعة إلى القائمة
                if result.status == TaskStatus.COMPLETED:
                    self._check_dependent_tasks(task_id)

        except Exception as e:
            self.logger.error(f"Error handling task completion: {e}")

    def _check_dependent_tasks(self, completed_task_id: str):
        """فحص المهام التي تعتمد على المهمة المكتملة"""
        try:
            for task_id, task in self.tasks.items():
                if (completed_task_id in task.dependencies and
                    task.status == TaskStatus.PENDING):

                    if self._check_dependencies(task):
                        self._add_to_queue(task)

        except Exception as e:
            self.logger.error(f"Error checking dependent tasks: {e}")

    def _cleanup_completed_tasks(self):
        """تنظيف المهام المكتملة"""
        try:
            completed_tasks = [
                (task_id, task) for task_id, task in self.tasks.items()
                if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]
            ]

            if len(completed_tasks) > self.max_completed_tasks:
                # ترتيب حسب تاريخ الاكتمال
                completed_tasks.sort(key=lambda x: x[1].completed_at or datetime.min)

                # حذف الأقدم
                tasks_to_remove = completed_tasks[:-self.max_completed_tasks]
                for task_id, _ in tasks_to_remove:
                    del self.tasks[task_id]
                    if task_id in self.results:
                        del self.results[task_id]

        except Exception as e:
            self.logger.error(f"Error cleaning up completed tasks: {e}")
