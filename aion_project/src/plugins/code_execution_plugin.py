"""
🚀 AION Code Execution Plugin
Enhanced multi-language code execution with optimized Rust and C++ support
"""

import asyncio
import sys
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from plugins.base_plugin import BasePlugin
from utils.code_executor import CodeExecutor, Language

console = Console()

class CodeExecutionPlugin(BasePlugin):
    """Enhanced code execution plugin with performance optimization"""
    
    def __init__(self):
        super().__init__()
        self.name = "code_execution"
        self.version = "2.0.0"
        self.description_ar = "تنفيذ الكود متعدد اللغات مع تحسينات الأداء"
        self.description_en = "Multi-language code execution with performance optimization"
        self.author = "AION Team"
        
        self.executor = CodeExecutor()
        
        # Sample codes for different languages
        self.sample_codes = {
            "rust": '''fn main() {
    println!("🦀 مرحباً من Rust!");
    
    // حساب الأرقام الأولية بكفاءة عالية
    let primes = sieve_of_eratosthenes(100);
    println!("الأرقام الأولية حتى 100: {:?}", primes);
}

fn sieve_of_eratosthenes(limit: usize) -> Vec<usize> {
    let mut is_prime = vec![true; limit + 1];
    is_prime[0] = false;
    if limit > 0 { is_prime[1] = false; }
    
    for i in 2..=((limit as f64).sqrt() as usize) {
        if is_prime[i] {
            for j in ((i * i)..=limit).step_by(i) {
                is_prime[j] = false;
            }
        }
    }
    
    (2..=limit).filter(|&i| is_prime[i]).collect()
}''',
            
            "cpp": '''#include <iostream>
#include <vector>
#include <chrono>
#include <algorithm>

int main() {
    std::cout << "⚡ مرحباً من C++!" << std::endl;
    
    // حساب فيبوناتشي بأداء عالي
    auto start = std::chrono::high_resolution_clock::now();
    
    std::vector<long long> fib = fibonacci_sequence(40);
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    std::cout << "متسلسلة فيبوناتشي (40 رقم): ";
    for (size_t i = 0; i < std::min(fib.size(), size_t(10)); ++i) {
        std::cout << fib[i] << " ";
    }
    std::cout << "..." << std::endl;
    std::cout << "وقت التنفيذ: " << duration.count() << " مايكروثانية" << std::endl;
    
    return 0;
}

std::vector<long long> fibonacci_sequence(int n) {
    std::vector<long long> fib(n);
    if (n > 0) fib[0] = 0;
    if (n > 1) fib[1] = 1;
    
    for (int i = 2; i < n; ++i) {
        fib[i] = fib[i-1] + fib[i-2];
    }
    
    return fib;
}''',
            
            "python": '''import time
import math

def main():
    print("🐍 مرحباً من Python!")
    
    # حساب العوامل الأولية
    start_time = time.time()
    number = 1234567
    factors = prime_factors(number)
    end_time = time.time()
    
    print(f"العوامل الأولية لـ {number}: {factors}")
    print(f"وقت التنفيذ: {(end_time - start_time)*1000:.2f} ميلي ثانية")

def prime_factors(n):
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

if __name__ == "__main__":
    main()''',
            
            "javascript": '''console.log("🌟 مرحباً من JavaScript!");

// حساب مضروب الرقم بطريقة تكرارية
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// قياس الأداء
const start = performance.now();
const result = factorial(20);
const end = performance.now();

console.log(`مضروب 20 = ${result}`);
console.log(`وقت التنفيذ: ${(end - start).toFixed(2)} ميلي ثانية`);

// مثال على المصفوفات
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
const squares = numbers.map(n => n * n);
console.log(`مربعات الأرقام: ${squares.join(', ')}`);'''
        }
    
    def initialize(self) -> bool:
        """Initialize the code execution plugin"""
        try:
            console.print("🚀 تهيئة مشغل الكود | Initializing Code Executor...")
            
            # Display available languages
            available_langs = self.executor.get_available_languages()
            if available_langs:
                console.print("✅ اللغات المتاحة | Available Languages:")
                for lang in available_langs:
                    perf_icon = {"extreme": "🔥", "high": "⚡", "medium": "⭐"}.get(lang["performance_level"], "📝")
                    console.print(f"  {perf_icon} {lang['display_name']} - {lang['description_ar']}")
                return True
            else:
                console.print("❌ لم يتم العثور على أي لغة برمجة متاحة")
                return False
                
        except Exception as e:
            console.print(f"❌ خطأ في تهيئة مشغل الكود: {str(e)}")
            return False
    
    def get_commands(self) -> Dict[str, str]:
        """Get available commands"""
        return {
            "run": "تشغيل كود | Run code",
            "languages": "عرض اللغات المتاحة | Show available languages",
            "sample": "عرض أمثلة الكود | Show code samples",
            "benchmark": "قياس الأداء | Performance benchmark",
            "optimize": "معلومات التحسين | Optimization info"
        }
    
    async def execute_command(self, command: str, args: List[str] = None) -> bool:
        """Execute plugin command"""
        args = args or []
        
        try:
            if command == "run":
                await self._run_code_interactive()
            elif command == "languages":
                self._show_available_languages()
            elif command == "sample":
                await self._show_code_samples()
            elif command == "benchmark":
                await self._run_benchmark()
            elif command == "optimize":
                self._show_optimization_info()
            else:
                console.print(f"❌ أمر غير معروف: {command}")
                return False
            
            return True
            
        except Exception as e:
            console.print(f"❌ خطأ في تنفيذ الأمر: {str(e)}")
            return False

    def _show_available_languages(self):
        """Display available programming languages with details"""
        console.print("\n🌐 اللغات المتاحة | Available Programming Languages")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("اللغة | Language", style="cyan")
        table.add_column("الأداء | Performance", justify="center")
        table.add_column("النوع | Type", justify="center")
        table.add_column("الوصف | Description", style="dim")

        available_langs = self.executor.get_available_languages()

        for lang in available_langs:
            perf_icons = {
                "extreme": "🔥 عالي جداً",
                "high": "⚡ عالي",
                "medium": "⭐ متوسط",
                "low": "📝 منخفض"
            }

            perf_display = perf_icons.get(lang["performance_level"], "❓ غير محدد")
            type_display = "مجمع | Compiled" if lang["compiled"] else "مفسر | Interpreted"

            table.add_row(
                lang["display_name"],
                perf_display,
                type_display,
                lang["description_ar"]
            )

        console.print(table)

        # Show high-performance languages separately
        high_perf = self.executor.get_performance_languages()
        if high_perf:
            console.print("\n🔥 لغات الأداء العالي | High-Performance Languages:")
            for lang in high_perf:
                if lang["performance_level"] == "extreme":
                    console.print(f"  🔥 {lang['display_name']} - {lang['description_ar']}")

    async def _show_code_samples(self):
        """Show code samples for different languages"""
        console.print("\n📝 أمثلة الكود | Code Samples")

        available_samples = []
        for lang_name in self.sample_codes.keys():
            try:
                lang_enum = Language(lang_name)
                if lang_enum in self.executor.available_languages:
                    available_samples.append(lang_name)
            except ValueError:
                continue

        if not available_samples:
            console.print("❌ لا توجد أمثلة متاحة للغات المثبتة")
            return

        # Show available samples
        console.print("الأمثلة المتاحة:")
        for i, lang in enumerate(available_samples, 1):
            console.print(f"[{i}] {lang.upper()}")

        try:
            choice = Prompt.ask("اختر رقم المثال", choices=[str(i) for i in range(1, len(available_samples) + 1)])
            selected_lang = available_samples[int(choice) - 1]

            # Display the sample code
            code = self.sample_codes[selected_lang]
            syntax = Syntax(code, selected_lang, theme="monokai", line_numbers=True)

            panel = Panel(
                syntax,
                title=f"🔥 مثال {selected_lang.upper()} | {selected_lang.upper()} Sample",
                border_style="green"
            )
            console.print(panel)

            # Ask if user wants to run it
            if Confirm.ask("هل تريد تشغيل هذا المثال؟ | Do you want to run this sample?"):
                await self._execute_sample_code(selected_lang, code)

        except (ValueError, KeyboardInterrupt):
            console.print("❌ تم الإلغاء")

    async def _execute_sample_code(self, language: str, code: str):
        """Execute sample code with progress display"""
        console.print(f"\n🚀 تشغيل مثال {language.upper()}...")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            transient=True
        ) as progress:

            task = progress.add_task(f"تنفيذ كود {language.upper()}...", total=100)

            # Execute the code
            result = await self.executor.execute_code(code, language, optimize=True)
            progress.update(task, completed=100)

        # Display results
        self._display_execution_result(result, language)

    async def _run_code_interactive(self):
        """Interactive code execution"""
        console.print("\n💻 تشغيل الكود التفاعلي | Interactive Code Execution")

        # Select language
        available_langs = self.executor.get_available_languages()
        if not available_langs:
            console.print("❌ لا توجد لغات برمجة متاحة")
            return

        console.print("اختر لغة البرمجة:")
        for i, lang in enumerate(available_langs, 1):
            perf_icon = {"extreme": "🔥", "high": "⚡", "medium": "⭐"}.get(lang["performance_level"], "📝")
            console.print(f"[{i}] {perf_icon} {lang['display_name']} - {lang['description_ar']}")

        try:
            choice = Prompt.ask("اختر رقم اللغة", choices=[str(i) for i in range(1, len(available_langs) + 1)])
            selected_lang = available_langs[int(choice) - 1]

            console.print(f"\n✅ تم اختيار: {selected_lang['display_name']}")
            console.print("أدخل الكود (اكتب 'END' في سطر منفصل للانتهاء):")

            # Collect code input
            code_lines = []
            while True:
                try:
                    line = input()
                    if line.strip() == "END":
                        break
                    code_lines.append(line)
                except KeyboardInterrupt:
                    console.print("\n❌ تم الإلغاء")
                    return

            code = "\n".join(code_lines)
            if not code.strip():
                console.print("❌ لم يتم إدخال أي كود")
                return

            # Ask for optimization
            optimize = True
            if selected_lang["performance_level"] in ["high", "extreme"]:
                optimize = Confirm.ask("تفعيل تحسينات الأداء؟ | Enable performance optimizations?", default=True)

            # Execute code
            console.print(f"\n🚀 تشغيل الكود...")
            result = await self.executor.execute_code(code, selected_lang["name"], optimize=optimize)

            # Display results
            self._display_execution_result(result, selected_lang["name"])

        except (ValueError, KeyboardInterrupt):
            console.print("❌ تم الإلغاء")

    def _display_execution_result(self, result, language: str):
        """Display code execution results with enhanced formatting"""
        if result.success:
            # Success panel
            success_content = f"✅ تم تنفيذ كود {language.upper()} بنجاح!\n"
            success_content += f"⏱️ وقت التنفيذ: {result.execution_time:.3f} ثانية\n"

            if result.compile_time:
                success_content += f"🔧 وقت التجميع: {result.compile_time:.3f} ثانية\n"

            success_content += f"🚀 كود الخروج: {result.exit_code}"

            console.print(Panel(success_content, title="نتيجة التنفيذ | Execution Result", border_style="green"))

            # Output panel
            if result.output.strip():
                console.print(Panel(result.output, title="المخرجات | Output", border_style="blue"))
        else:
            # Error panel
            error_content = f"❌ فشل في تنفيذ كود {language.upper()}\n"
            error_content += f"⏱️ وقت التنفيذ: {result.execution_time:.3f} ثانية\n"
            error_content += f"🚨 كود الخروج: {result.exit_code}"

            console.print(Panel(error_content, title="خطأ في التنفيذ | Execution Error", border_style="red"))

            # Error details
            if result.error.strip():
                console.print(Panel(result.error, title="تفاصيل الخطأ | Error Details", border_style="red"))

    async def _run_benchmark(self):
        """Run performance benchmark for available languages"""
        console.print("\n🏁 قياس الأداء | Performance Benchmark")

        # Simple benchmark code for each language
        benchmark_codes = {
            "python": '''
import time
start = time.time()
result = sum(i*i for i in range(100000))
end = time.time()
print(f"Sum of squares: {result}")
print(f"Time: {(end-start)*1000:.2f}ms")
''',
            "rust": '''
use std::time::Instant;

fn main() {
    let start = Instant::now();
    let result: u64 = (0..100000).map(|i| i * i).sum();
    let duration = start.elapsed();

    println!("Sum of squares: {}", result);
    println!("Time: {:.2}ms", duration.as_secs_f64() * 1000.0);
}
''',
            "cpp": '''
#include <iostream>
#include <chrono>

int main() {
    auto start = std::chrono::high_resolution_clock::now();

    long long result = 0;
    for (int i = 0; i < 100000; ++i) {
        result += i * i;
    }

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

    std::cout << "Sum of squares: " << result << std::endl;
    std::cout << "Time: " << duration.count() / 1000.0 << "ms" << std::endl;

    return 0;
}
'''
        }

        available_langs = [lang["name"] for lang in self.executor.get_available_languages()]
        benchmark_langs = [lang for lang in benchmark_codes.keys() if lang in available_langs]

        if not benchmark_langs:
            console.print("❌ لا توجد لغات متاحة للقياس")
            return

        console.print(f"🔥 قياس الأداء للغات: {', '.join(benchmark_langs)}")

        results = []
        for lang in benchmark_langs:
            console.print(f"\n⚡ اختبار {lang.upper()}...")

            benchmark_result = await self.executor.benchmark_language(lang, benchmark_codes[lang])
            if "error" not in benchmark_result:
                results.append(benchmark_result)
                console.print(f"✅ {lang.upper()}: {benchmark_result['total_time']:.3f}s")
            else:
                console.print(f"❌ {lang.upper()}: {benchmark_result['error']}")

        # Display benchmark results
        if results:
            self._display_benchmark_results(results)

    def _display_benchmark_results(self, results: List[Dict]):
        """Display benchmark results in a table"""
        console.print("\n🏆 نتائج قياس الأداء | Benchmark Results")

        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("اللغة | Language", style="cyan")
        table.add_column("وقت التجميع | Compile Time", justify="right")
        table.add_column("وقت التنفيذ | Execution Time", justify="right")
        table.add_column("الوقت الإجمالي | Total Time", justify="right")
        table.add_column("الترتيب | Rank", justify="center")

        # Sort by total time
        sorted_results = sorted(results, key=lambda x: x["total_time"])

        for i, result in enumerate(sorted_results, 1):
            rank_icon = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}️⃣"

            table.add_row(
                result["language"].upper(),
                f"{result['average_compile_time']:.3f}s" if result['average_compile_time'] > 0 else "N/A",
                f"{result['average_execution_time']:.3f}s",
                f"{result['total_time']:.3f}s",
                rank_icon
            )

        console.print(table)

    def _show_optimization_info(self):
        """Show optimization information for compiled languages"""
        console.print("\n🔧 معلومات التحسين | Optimization Information")

        opt_info = self.executor.get_optimization_info()

        if not opt_info:
            console.print("❌ لا توجد لغات مجمعة متاحة للتحسين")
            return

        for lang, info in opt_info.items():
            console.print(f"\n🔥 {lang.upper()}:")
            console.print(f"  📝 {info['description_ar']}")
            console.print(f"  ⚙️ أعلام التحسين: {' '.join(info['flags'])}")

            if lang == "rust":
                console.print("  🦀 تحسينات Rust الخاصة:")
                console.print("    • --edition=2021: استخدام أحدث إصدار")
                console.print("    • -O: تحسينات الأداء")
                console.print("    • --target: تحسين للمعالج المحدد")

            elif lang == "cpp":
                console.print("  ⚡ تحسينات C++ الخاصة:")
                console.print("    • -O3: أقصى تحسينات الأداء")
                console.print("    • -march=native: تحسين للمعالج الحالي")
                console.print("    • -std=c++20: استخدام أحدث معايير C++")

            elif lang == "c":
                console.print("  🔧 تحسينات C الخاصة:")
                console.print("    • -O3: أقصى تحسينات الأداء")
                console.print("    • -march=native: تحسين للمعالج الحالي")
                console.print("    • -std=c11: استخدام معيار C11")

    def execute(self, command: str, args: List[str]) -> Dict[str, Any]:
        """Execute plugin command - required by BasePlugin"""
        try:
            if command == "interactive":
                # Run interactive mode (this will be called from main app)
                return {"success": True, "message": "Interactive mode started"}
            else:
                # Handle specific commands
                return {"success": False, "message": f"Unknown command: {command}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
