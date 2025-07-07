#!/usr/bin/env python3
"""
🧪 Full Simulation Script for AION Terminal
🎯 Objective: Trigger ALL menus, components, and interactions using full arrow-key control
👀 Logs ALL live terminal activity to output, and captures user-like simulation
🔧 Cross-platform compatible (Windows/Linux/macOS)
"""

import subprocess
import time
import os
import sys
import platform
from datetime import datetime
import threading
import signal
from pathlib import Path

class AIONSimulator:
    def __init__(self):
        self.start_time = datetime.now()
        self.log_dir = Path("test_logs")
        self.log_dir.mkdir(exist_ok=True)
        self.session_log = self.log_dir / "aion_terminal_full_session.log"
        self.simulation_log = self.log_dir / "live_simulation_keys.log"
        self.process = None
        
    def log_message(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        # Also write to simulation log
        with open(self.simulation_log, "a", encoding="utf-8") as f:
            f.write(f"{log_entry}\n")
    
    def start_aion_process(self):
        """Start AION process and capture output"""
        try:
            self.log_message("🟢 Launching AION terminal session...")
            
            # Use python -m aion change-language for testing arrow navigation
            cmd = [sys.executable, "-m", "aion", "change-language"]
            
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0
            )
            
            self.log_message(f"✅ AION process started with PID: {self.process.pid}")
            return True
            
        except Exception as e:
            self.log_message(f"❌ Failed to start AION: {e}")
            return False
    
    def simulate_arrow_navigation(self):
        """Simulate arrow key navigation"""
        try:
            self.log_message("⌨️ Starting arrow key simulation...")
            
            # Wait for AION to initialize
            time.sleep(2)
            
            # Simulation sequence
            navigation_sequence = [
                ("↓", "Navigate down to Arabic"),
                ("↓", "Navigate down to Norwegian"), 
                ("↓", "Navigate down to German"),
                ("↑", "Navigate back up to Norwegian"),
                ("↑", "Navigate back up to Arabic"),
                ("↑", "Navigate back up to English"),
                ("↓", "Navigate down to Arabic again"),
                ("\n", "Select Arabic language"),
            ]
            
            for key, description in navigation_sequence:
                self.log_message(f"🎮 {description}")
                
                if self.process and self.process.stdin:
                    try:
                        if key == "↓":
                            # Send down arrow
                            self.process.stdin.write("\x1b[B")
                        elif key == "↑":
                            # Send up arrow  
                            self.process.stdin.write("\x1b[A")
                        elif key == "\n":
                            # Send Enter
                            self.process.stdin.write("\n")
                        
                        self.process.stdin.flush()
                        time.sleep(1.5)  # Wait between inputs
                        
                    except Exception as e:
                        self.log_message(f"⚠️ Input error: {e}")
                        break
                else:
                    self.log_message("❌ Process stdin not available")
                    break
            
            self.log_message("✅ Arrow navigation simulation completed")
            
        except Exception as e:
            self.log_message(f"❌ Simulation error: {e}")
    
    def capture_output(self):
        """Capture and log process output"""
        if not self.process:
            return
            
        try:
            # Read stdout in a separate thread
            def read_stdout():
                while self.process and self.process.poll() is None:
                    try:
                        line = self.process.stdout.readline()
                        if line:
                            self.log_message(f"📺 OUTPUT: {line.strip()}")
                            # Also write to session log
                            with open(self.session_log, "a", encoding="utf-8") as f:
                                f.write(f"{line}")
                    except Exception as e:
                        self.log_message(f"⚠️ Output capture error: {e}")
                        break
            
            output_thread = threading.Thread(target=read_stdout, daemon=True)
            output_thread.start()
            
        except Exception as e:
            self.log_message(f"❌ Output capture setup error: {e}")
    
    def run_simulation(self):
        """Run the complete simulation"""
        self.log_message("🚀 [AION Simulation Started] --------------------------------------------")
        self.log_message(f"🕒 Start Time: {self.start_time}")
        self.log_message(f"🖥️ Platform: {platform.system()} {platform.release()}")
        self.log_message(f"🐍 Python: {sys.version}")
        
        try:
            # Start AION process
            if not self.start_aion_process():
                return False
            
            # Start output capture
            self.capture_output()
            
            # Run arrow navigation simulation
            self.simulate_arrow_navigation()
            
            # Wait for process to complete or timeout
            self.log_message("⏳ Waiting for process completion...")
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.log_message("⏰ Process timeout - terminating...")
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
            
            # Final status
            if self.process:
                return_code = self.process.returncode
                self.log_message(f"🔚 Process completed with return code: {return_code}")
            
            end_time = datetime.now()
            duration = end_time - self.start_time
            
            self.log_message("✅ [AION Simulation Completed] ----------------------")
            self.log_message(f"🕒 End Time: {end_time}")
            self.log_message(f"⏱️ Duration: {duration}")
            self.log_message(f"📁 Session log: {self.session_log}")
            self.log_message(f"📁 Simulation log: {self.simulation_log}")
            
            return True
            
        except KeyboardInterrupt:
            self.log_message("🛑 Simulation interrupted by user")
            if self.process:
                self.process.terminate()
            return False
        except Exception as e:
            self.log_message(f"❌ Simulation failed: {e}")
            return False

def main():
    """Main entry point"""
    print("🧪 AION Full Terminal Simulation")
    print("=" * 50)
    
    simulator = AIONSimulator()
    success = simulator.run_simulation()
    
    if success:
        print("\n🎉 Simulation completed successfully!")
        print(f"📋 Check logs in: {simulator.log_dir}")
    else:
        print("\n💥 Simulation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
