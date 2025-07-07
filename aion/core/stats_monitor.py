#!/usr/bin/env python3
"""
📊 AION Real-Time Statistics Monitor
Advanced system monitoring and performance tracking

This module provides:
- Real-time system resource monitoring (CPU, Memory, Disk, Network)
- AI usage statistics and performance metrics
- Plugin execution statistics and resource usage
- Terminal session analytics and user behavior tracking
- Performance optimization recommendations
"""

import os
import sys
import time
import psutil
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import deque
import json

@dataclass
class SystemStats:
    """System resource statistics"""
    cpu_percent: float
    memory_percent: float
    memory_used: int
    memory_total: int
    disk_percent: float
    disk_used: int
    disk_total: int
    network_sent: int
    network_recv: int
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class AIUsageStats:
    """AI provider usage statistics"""
    provider: str
    requests_count: int
    tokens_used: int
    response_time_avg: float
    success_rate: float
    error_count: int
    last_used: datetime = field(default_factory=datetime.now)

@dataclass
class PluginStats:
    """Plugin execution statistics"""
    plugin_name: str
    executions_count: int
    success_count: int
    failure_count: int
    avg_execution_time: float
    cpu_usage_avg: float
    memory_usage_avg: float
    last_executed: datetime = field(default_factory=datetime.now)

@dataclass
class SessionStats:
    """Terminal session statistics"""
    session_start: datetime
    commands_executed: int
    files_edited: int
    plugins_used: int
    ai_interactions: int
    errors_encountered: int
    uptime: timedelta = field(default_factory=lambda: timedelta(0))

class StatsMonitor:
    """Real-time statistics monitoring system"""

    def __init__(self, update_interval: float = 1.0):
        self.update_interval = update_interval
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None

        # Statistics storage
        self.system_stats_history: deque = deque(maxlen=300)  # 5 minutes at 1s intervals
        self.ai_usage_stats: Dict[str, AIUsageStats] = {}
        self.plugin_stats: Dict[str, PluginStats] = {}
        self.session_stats = SessionStats(
            session_start=datetime.now(),
            commands_executed=0,
            files_edited=0,
            plugins_used=0,
            ai_interactions=0,
            errors_encountered=0
        )

        # Performance thresholds
        self.cpu_warning_threshold = 80.0
        self.memory_warning_threshold = 85.0
        self.disk_warning_threshold = 90.0

        # Initialize network counters
        self.network_stats = psutil.net_io_counters()
        self.last_network_sent = self.network_stats.bytes_sent
        self.last_network_recv = self.network_stats.bytes_recv

    def start_monitoring(self):
        """Start real-time monitoring"""
        if self.monitoring:
            return

        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("📊 Real-time statistics monitoring started")

    def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
        print("📊 Statistics monitoring stopped")

    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # Collect system statistics
                system_stats = self._collect_system_stats()
                self.system_stats_history.append(system_stats)

                # Update session uptime
                self.session_stats.uptime = datetime.now() - self.session_stats.session_start

                # Check for performance warnings
                self._check_performance_warnings(system_stats)

                time.sleep(self.update_interval)

            except Exception as e:
                print(f"⚠️ Error in monitoring loop: {e}")
                time.sleep(self.update_interval)

    def _collect_system_stats(self) -> SystemStats:
        """Collect current system statistics"""
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=None)

        # Memory usage
        memory = psutil.virtual_memory()

        # Disk usage
        disk = psutil.disk_usage('/')

        # Network usage (delta since last check)
        current_network = psutil.net_io_counters()
        network_sent_delta = current_network.bytes_sent - self.last_network_sent
        network_recv_delta = current_network.bytes_recv - self.last_network_recv

        self.last_network_sent = current_network.bytes_sent
        self.last_network_recv = current_network.bytes_recv

        return SystemStats(
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used=memory.used,
            memory_total=memory.total,
            disk_percent=disk.percent,
            disk_used=disk.used,
            disk_total=disk.total,
            network_sent=network_sent_delta,
            network_recv=network_recv_delta
        )

    def _check_performance_warnings(self, stats: SystemStats):
        """Check for performance warnings and alerts"""
        warnings = []

        if stats.cpu_percent > self.cpu_warning_threshold:
            warnings.append(f"🔥 High CPU usage: {stats.cpu_percent:.1f}%")

        if stats.memory_percent > self.memory_warning_threshold:
            warnings.append(f"🧠 High memory usage: {stats.memory_percent:.1f}%")

        if stats.disk_percent > self.disk_warning_threshold:
            warnings.append(f"💾 High disk usage: {stats.disk_percent:.1f}%")

        if warnings:
            for warning in warnings:
                print(f"⚠️ {warning}")

    def record_ai_usage(self, provider: str, tokens_used: int, response_time: float, success: bool):
        """Record AI provider usage statistics"""
        if provider not in self.ai_usage_stats:
            self.ai_usage_stats[provider] = AIUsageStats(
                provider=provider,
                requests_count=0,
                tokens_used=0,
                response_time_avg=0.0,
                success_rate=0.0,
                error_count=0
            )

        stats = self.ai_usage_stats[provider]
        stats.requests_count += 1
        stats.tokens_used += tokens_used
        stats.last_used = datetime.now()

        # Update average response time
        stats.response_time_avg = (
            (stats.response_time_avg * (stats.requests_count - 1) + response_time) /
            stats.requests_count
        )

        if success:
            stats.success_rate = (
                (stats.success_rate * (stats.requests_count - 1) + 1.0) /
                stats.requests_count
            )
        else:
            stats.error_count += 1
            stats.success_rate = (
                (stats.success_rate * (stats.requests_count - 1) + 0.0) /
                stats.requests_count
            )

        self.session_stats.ai_interactions += 1

    def record_plugin_execution(self, plugin_name: str, execution_time: float,
                              cpu_usage: float, memory_usage: float, success: bool):
        """Record plugin execution statistics"""
        if plugin_name not in self.plugin_stats:
            self.plugin_stats[plugin_name] = PluginStats(
                plugin_name=plugin_name,
                executions_count=0,
                success_count=0,
                failure_count=0,
                avg_execution_time=0.0,
                cpu_usage_avg=0.0,
                memory_usage_avg=0.0
            )

        stats = self.plugin_stats[plugin_name]
        stats.executions_count += 1
        stats.last_executed = datetime.now()

        # Update averages
        stats.avg_execution_time = (
            (stats.avg_execution_time * (stats.executions_count - 1) + execution_time) /
            stats.executions_count
        )
        stats.cpu_usage_avg = (
            (stats.cpu_usage_avg * (stats.executions_count - 1) + cpu_usage) /
            stats.executions_count
        )
        stats.memory_usage_avg = (
            (stats.memory_usage_avg * (stats.executions_count - 1) + memory_usage) /
            stats.executions_count
        )

        if success:
            stats.success_count += 1
        else:
            stats.failure_count += 1

        self.session_stats.plugins_used += 1

    def record_command_execution(self):
        """Record command execution"""
        self.session_stats.commands_executed += 1

    def record_file_edit(self):
        """Record file editing activity"""
        self.session_stats.files_edited += 1

    def record_error(self):
        """Record error occurrence"""
        self.session_stats.errors_encountered += 1

    def get_current_system_stats(self) -> Optional[SystemStats]:
        """Get the most recent system statistics"""
        return self.system_stats_history[-1] if self.system_stats_history else None

    def get_system_stats_history(self, minutes: int = 5) -> List[SystemStats]:
        """Get system statistics history for specified minutes"""
        target_count = minutes * 60 // int(self.update_interval)
        return list(self.system_stats_history)[-target_count:]

    def get_ai_usage_summary(self) -> Dict[str, AIUsageStats]:
        """Get AI usage statistics summary"""
        return self.ai_usage_stats.copy()

    def get_plugin_stats_summary(self) -> Dict[str, PluginStats]:
        """Get plugin statistics summary"""
        return self.plugin_stats.copy()

    def get_session_summary(self) -> SessionStats:
        """Get current session statistics"""
        return self.session_stats

    def get_performance_recommendations(self) -> List[str]:
        """Get performance optimization recommendations"""
        recommendations = []
        current_stats = self.get_current_system_stats()

        if not current_stats:
            return recommendations

        # CPU recommendations
        if current_stats.cpu_percent > 70:
            recommendations.append("🔥 Consider closing unused applications to reduce CPU usage")

        # Memory recommendations
        if current_stats.memory_percent > 80:
            recommendations.append("🧠 Consider closing memory-intensive applications")

        # Disk recommendations
        if current_stats.disk_percent > 85:
            recommendations.append("💾 Consider cleaning up disk space or moving files")

        # AI usage recommendations
        ai_stats = self.get_ai_usage_summary()
        for provider, stats in ai_stats.items():
            if stats.success_rate < 0.8:
                recommendations.append(f"🤖 {provider} has low success rate ({stats.success_rate:.1%})")

        # Plugin recommendations
        plugin_stats = self.get_plugin_stats_summary()
        for plugin_name, stats in plugin_stats.items():
            if stats.failure_count > stats.success_count:
                recommendations.append(f"🧩 Plugin '{plugin_name}' has high failure rate")

        return recommendations

    def export_stats(self, filepath: str):
        """Export statistics to JSON file"""
        try:
            data = {
                'session_stats': {
                    'session_start': self.session_stats.session_start.isoformat(),
                    'commands_executed': self.session_stats.commands_executed,
                    'files_edited': self.session_stats.files_edited,
                    'plugins_used': self.session_stats.plugins_used,
                    'ai_interactions': self.session_stats.ai_interactions,
                    'errors_encountered': self.session_stats.errors_encountered,
                    'uptime_seconds': self.session_stats.uptime.total_seconds()
                },
                'ai_usage_stats': {
                    provider: {
                        'requests_count': stats.requests_count,
                        'tokens_used': stats.tokens_used,
                        'response_time_avg': stats.response_time_avg,
                        'success_rate': stats.success_rate,
                        'error_count': stats.error_count,
                        'last_used': stats.last_used.isoformat()
                    }
                    for provider, stats in self.ai_usage_stats.items()
                },
                'plugin_stats': {
                    plugin: {
                        'executions_count': stats.executions_count,
                        'success_count': stats.success_count,
                        'failure_count': stats.failure_count,
                        'avg_execution_time': stats.avg_execution_time,
                        'cpu_usage_avg': stats.cpu_usage_avg,
                        'memory_usage_avg': stats.memory_usage_avg,
                        'last_executed': stats.last_executed.isoformat()
                    }
                    for plugin, stats in self.plugin_stats.items()
                },
                'system_stats_recent': [
                    {
                        'cpu_percent': stats.cpu_percent,
                        'memory_percent': stats.memory_percent,
                        'disk_percent': stats.disk_percent,
                        'timestamp': stats.timestamp.isoformat()
                    }
                    for stats in list(self.system_stats_history)[-60:]  # Last minute
                ]
            }

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"📊 Statistics exported to: {filepath}")

        except Exception as e:
            print(f"❌ Error exporting statistics: {e}")

# Global statistics monitor instance
stats_monitor = StatsMonitor()

def format_bytes(bytes_value: int) -> str:
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def format_duration(seconds: float) -> str:
    """Format duration to human readable format"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"