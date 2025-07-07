"""
🎤 AION Voice Control System
Advanced voice control with speech-to-text, text-to-speech, and voice command processing
Features: Voice recognition, Speech synthesis, Command processing, Multi-language support
"""

import asyncio
import json
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum

# Optional imports with fallbacks
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    sr = None

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    pyttsx3 = None

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    pyaudio = None

class VoiceCommandStatus(Enum):
    """Voice command processing status"""
    LISTENING = "listening"
    PROCESSING = "processing"
    EXECUTED = "executed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    NO_SPEECH = "no_speech"
    UNRECOGNIZED = "unrecognized"

class VoiceLanguage(Enum):
    """Supported voice languages"""
    ENGLISH = "en-US"
    ARABIC = "ar-SA"
    GERMAN = "de-DE"
    FRENCH = "fr-FR"
    SPANISH = "es-ES"
    CHINESE = "zh-CN"
    NORWEGIAN = "no-NO"

@dataclass
class VoiceCommand:
    """Voice command data structure"""
    command_id: str
    text: str
    language: VoiceLanguage
    confidence: float
    timestamp: datetime
    status: VoiceCommandStatus = VoiceCommandStatus.PROCESSING
    response: str = ""
    execution_time: float = 0.0
    error: str = ""

@dataclass
class VoiceSession:
    """Voice control session"""
    session_id: str
    start_time: datetime
    language: VoiceLanguage
    commands: List[VoiceCommand] = field(default_factory=list)
    is_active: bool = True
    total_commands: int = 0
    successful_commands: int = 0
    end_time: Optional[datetime] = None

class VoiceControlManager:
    """
    🚀 Advanced Voice Control Manager
    
    Professional voice control system with:
    - Speech-to-text recognition
    - Text-to-speech synthesis
    - Multi-language support
    - Voice command processing
    - Continuous listening mode
    - Command history and analytics
    - Voice feedback and responses
    - Integration with AION commands
    """
    
    def __init__(self):
        # Storage
        self.voice_dir = Path.home() / ".aion" / "voice"
        self.voice_dir.mkdir(parents=True, exist_ok=True)
        
        # Voice engines
        self.recognizer = None
        self.microphone = None
        self.tts_engine = None
        
        # Initialize engines
        self._initialize_speech_recognition()
        self._initialize_text_to_speech()
        
        # Runtime data
        self.sessions: Dict[str, VoiceSession] = {}
        self.active_session: Optional[VoiceSession] = None
        self.command_handlers: Dict[str, Callable] = {}
        
        # Configuration
        self.current_language = VoiceLanguage.ENGLISH
        self.listening_enabled = False
        self.voice_feedback_enabled = True
        self.confidence_threshold = 0.7
        
        # Statistics
        self.total_commands = 0
        self.successful_recognitions = 0
        self.failed_recognitions = 0
        
        # Load command handlers
        self._load_command_handlers()
        
        print("🎤 Voice Control Manager initialized")
        print(f"   Speech Recognition: {SPEECH_RECOGNITION_AVAILABLE}")
        print(f"   Text-to-Speech: {PYTTSX3_AVAILABLE}")
        print(f"   Audio Input: {PYAUDIO_AVAILABLE}")
    
    def _initialize_speech_recognition(self):
        """Initialize speech recognition engine"""
        if not SPEECH_RECOGNITION_AVAILABLE:
            print("⚠️ Speech recognition not available (install speech_recognition)")
            return
        
        try:
            self.recognizer = sr.Recognizer()
            
            # Try to initialize microphone
            if PYAUDIO_AVAILABLE:
                self.microphone = sr.Microphone()
                
                # Adjust for ambient noise
                with self.microphone as source:
                    print("🎤 Adjusting for ambient noise...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                print("✅ Speech recognition initialized with microphone")
            else:
                print("⚠️ Microphone not available (install pyaudio)")
                
        except Exception as e:
            print(f"⚠️ Speech recognition initialization failed: {e}")
            self.recognizer = None
            self.microphone = None
    
    def _initialize_text_to_speech(self):
        """Initialize text-to-speech engine"""
        if not PYTTSX3_AVAILABLE:
            print("⚠️ Text-to-speech not available (install pyttsx3)")
            return
        
        try:
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS settings
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to find English voice
                for voice in voices:
                    if 'english' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            # Set speech rate and volume
            self.tts_engine.setProperty('rate', 180)  # Speed
            self.tts_engine.setProperty('volume', 0.8)  # Volume
            
            print("✅ Text-to-speech initialized")
            
        except Exception as e:
            print(f"⚠️ Text-to-speech initialization failed: {e}")
            self.tts_engine = None
    
    def _load_command_handlers(self):
        """Load voice command handlers"""
        self.command_handlers = {
            # Basic commands
            "hello": self._handle_hello,
            "help": self._handle_help,
            "status": self._handle_status,
            "time": self._handle_time,
            "date": self._handle_date,
            
            # AION commands
            "execute": self._handle_execute,
            "run": self._handle_run,
            "code": self._handle_code,
            "python": self._handle_python,
            "javascript": self._handle_javascript,
            
            # System commands
            "stop listening": self._handle_stop_listening,
            "start listening": self._handle_start_listening,
            "change language": self._handle_change_language,
            "volume up": self._handle_volume_up,
            "volume down": self._handle_volume_down,
            
            # Session commands
            "new session": self._handle_new_session,
            "end session": self._handle_end_session,
            "session history": self._handle_session_history,
            
            # AI commands
            "ask ai": self._handle_ask_ai,
            "generate": self._handle_generate,
            "explain": self._handle_explain,
            "translate": self._handle_translate
        }
    
    async def start_voice_session(self, language: VoiceLanguage = VoiceLanguage.ENGLISH) -> str:
        """Start new voice control session"""
        session_id = f"voice_session_{int(time.time())}"
        
        session = VoiceSession(
            session_id=session_id,
            start_time=datetime.now(),
            language=language
        )
        
        self.sessions[session_id] = session
        self.active_session = session
        self.current_language = language
        
        print(f"🎤 Voice session started: {session_id}")
        print(f"   Language: {language.value}")
        
        if self.voice_feedback_enabled:
            await self.speak("Voice control session started. I'm listening for your commands.")
        
        return session_id
    
    async def listen_for_command(self, timeout: int = 5) -> Optional[VoiceCommand]:
        """Listen for a single voice command"""
        if not self.recognizer or not self.microphone:
            print("⚠️ Speech recognition not available")
            return None
        
        command_id = f"cmd_{int(time.time() * 1000)}"
        
        try:
            print("🎤 Listening for command...")
            
            with self.microphone as source:
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            
            print("🔄 Processing speech...")
            
            # Recognize speech
            start_time = time.time()
            text = self.recognizer.recognize_google(
                audio, 
                language=self.current_language.value
            )
            processing_time = time.time() - start_time
            
            # Create command
            command = VoiceCommand(
                command_id=command_id,
                text=text.lower(),
                language=self.current_language,
                confidence=0.8,  # Google doesn't provide confidence
                timestamp=datetime.now(),
                execution_time=processing_time
            )
            
            print(f"🎯 Recognized: '{text}'")
            self.successful_recognitions += 1
            
            return command
            
        except sr.WaitTimeoutError:
            print("⏰ Listening timeout")
            return VoiceCommand(
                command_id=command_id,
                text="",
                language=self.current_language,
                confidence=0.0,
                timestamp=datetime.now(),
                status=VoiceCommandStatus.TIMEOUT
            )
            
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
            self.failed_recognitions += 1
            return VoiceCommand(
                command_id=command_id,
                text="",
                language=self.current_language,
                confidence=0.0,
                timestamp=datetime.now(),
                status=VoiceCommandStatus.UNRECOGNIZED
            )
            
        except Exception as e:
            print(f"❌ Speech recognition error: {e}")
            self.failed_recognitions += 1
            return VoiceCommand(
                command_id=command_id,
                text="",
                language=self.current_language,
                confidence=0.0,
                timestamp=datetime.now(),
                status=VoiceCommandStatus.FAILED,
                error=str(e)
            )
    
    async def process_command(self, command: VoiceCommand) -> VoiceCommand:
        """Process voice command"""
        if not command or command.status != VoiceCommandStatus.PROCESSING:
            return command
        
        self.total_commands += 1
        
        try:
            # Find matching command handler
            handler = None
            for cmd_pattern, cmd_handler in self.command_handlers.items():
                if cmd_pattern in command.text:
                    handler = cmd_handler
                    break
            
            if handler:
                print(f"⚡ Executing command: {command.text}")
                response = await handler(command)
                command.response = response
                command.status = VoiceCommandStatus.EXECUTED
                
                if self.voice_feedback_enabled and response:
                    await self.speak(response)
            else:
                command.response = f"Unknown command: {command.text}"
                command.status = VoiceCommandStatus.UNRECOGNIZED
                
                if self.voice_feedback_enabled:
                    await self.speak("I didn't understand that command. Say 'help' for available commands.")
        
        except Exception as e:
            command.status = VoiceCommandStatus.FAILED
            command.error = str(e)
            command.response = f"Command execution failed: {str(e)}"
            
            if self.voice_feedback_enabled:
                await self.speak("Sorry, there was an error executing that command.")
        
        # Add to active session
        if self.active_session:
            self.active_session.commands.append(command)
            self.active_session.total_commands += 1
            if command.status == VoiceCommandStatus.EXECUTED:
                self.active_session.successful_commands += 1
        
        return command
    
    async def speak(self, text: str) -> bool:
        """Convert text to speech"""
        if not self.tts_engine:
            print(f"🔊 TTS: {text}")
            return False
        
        try:
            print(f"🔊 Speaking: {text}")
            
            # Run TTS in separate thread to avoid blocking
            def speak_text():
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            
            thread = threading.Thread(target=speak_text)
            thread.daemon = True
            thread.start()
            thread.join(timeout=10)  # Timeout after 10 seconds
            
            return True
            
        except Exception as e:
            print(f"⚠️ Text-to-speech error: {e}")
            return False

    # Command Handlers
    async def _handle_hello(self, command: VoiceCommand) -> str:
        """Handle hello command"""
        responses = [
            "Hello! I'm AION, your AI assistant. How can I help you?",
            "Hi there! Ready to assist you with voice commands.",
            "Greetings! AION voice control is active and ready."
        ]
        import random
        return random.choice(responses)

    async def _handle_help(self, command: VoiceCommand) -> str:
        """Handle help command"""
        return ("Available voice commands: hello, help, status, time, date, execute code, "
                "run python, ask AI, new session, stop listening, change language. "
                "Say any command clearly and I'll help you.")

    async def _handle_status(self, command: VoiceCommand) -> str:
        """Handle status command"""
        session = self.active_session
        if session:
            return (f"Voice session active. {session.total_commands} commands processed, "
                   f"{session.successful_commands} successful. Language: {session.language.value}")
        return "No active voice session."

    async def _handle_time(self, command: VoiceCommand) -> str:
        """Handle time command"""
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"

    async def _handle_date(self, command: VoiceCommand) -> str:
        """Handle date command"""
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}"

    async def _handle_execute(self, command: VoiceCommand) -> str:
        """Handle execute command"""
        # Extract code from command
        text = command.text.replace("execute", "").strip()
        if not text:
            return "Please specify what code to execute."

        # Simple code execution (would integrate with sandbox)
        return f"Executing: {text}. Code execution feature requires integration with sandbox system."

    async def _handle_run(self, command: VoiceCommand) -> str:
        """Handle run command"""
        return await self._handle_execute(command)

    async def _handle_code(self, command: VoiceCommand) -> str:
        """Handle code command"""
        return "Code execution mode activated. Please specify the programming language and code."

    async def _handle_python(self, command: VoiceCommand) -> str:
        """Handle python command"""
        text = command.text.replace("python", "").strip()
        if not text:
            return "Please specify Python code to execute."
        return f"Python execution: {text}. Integration with code executor needed."

    async def _handle_javascript(self, command: VoiceCommand) -> str:
        """Handle javascript command"""
        text = command.text.replace("javascript", "").strip()
        if not text:
            return "Please specify JavaScript code to execute."
        return f"JavaScript execution: {text}. Integration with code executor needed."

    async def _handle_stop_listening(self, command: VoiceCommand) -> str:
        """Handle stop listening command"""
        self.listening_enabled = False
        return "Voice listening stopped. Say 'start listening' to resume."

    async def _handle_start_listening(self, command: VoiceCommand) -> str:
        """Handle start listening command"""
        self.listening_enabled = True
        return "Voice listening started. I'm ready for your commands."

    async def _handle_change_language(self, command: VoiceCommand) -> str:
        """Handle change language command"""
        # Simple language detection from command
        text = command.text.lower()
        if "arabic" in text:
            self.current_language = VoiceLanguage.ARABIC
            return "Language changed to Arabic"
        elif "german" in text:
            self.current_language = VoiceLanguage.GERMAN
            return "Language changed to German"
        elif "french" in text:
            self.current_language = VoiceLanguage.FRENCH
            return "Language changed to French"
        elif "spanish" in text:
            self.current_language = VoiceLanguage.SPANISH
            return "Language changed to Spanish"
        elif "chinese" in text:
            self.current_language = VoiceLanguage.CHINESE
            return "Language changed to Chinese"
        elif "norwegian" in text:
            self.current_language = VoiceLanguage.NORWEGIAN
            return "Language changed to Norwegian"
        else:
            self.current_language = VoiceLanguage.ENGLISH
            return "Language changed to English"

    async def _handle_volume_up(self, command: VoiceCommand) -> str:
        """Handle volume up command"""
        if self.tts_engine:
            current_volume = self.tts_engine.getProperty('volume')
            new_volume = min(1.0, current_volume + 0.1)
            self.tts_engine.setProperty('volume', new_volume)
            return f"Volume increased to {int(new_volume * 100)}%"
        return "Volume control not available"

    async def _handle_volume_down(self, command: VoiceCommand) -> str:
        """Handle volume down command"""
        if self.tts_engine:
            current_volume = self.tts_engine.getProperty('volume')
            new_volume = max(0.0, current_volume - 0.1)
            self.tts_engine.setProperty('volume', new_volume)
            return f"Volume decreased to {int(new_volume * 100)}%"
        return "Volume control not available"

    async def _handle_new_session(self, command: VoiceCommand) -> str:
        """Handle new session command"""
        session_id = await self.start_voice_session(self.current_language)
        return f"New voice session started: {session_id}"

    async def _handle_end_session(self, command: VoiceCommand) -> str:
        """Handle end session command"""
        if self.active_session:
            self.active_session.end_time = datetime.now()
            self.active_session.is_active = False
            session_id = self.active_session.session_id
            self.active_session = None
            return f"Voice session ended: {session_id}"
        return "No active session to end"

    async def _handle_session_history(self, command: VoiceCommand) -> str:
        """Handle session history command"""
        if self.active_session:
            total = self.active_session.total_commands
            successful = self.active_session.successful_commands
            return f"Session history: {total} total commands, {successful} successful"
        return "No active session"

    async def _handle_ask_ai(self, command: VoiceCommand) -> str:
        """Handle ask AI command"""
        question = command.text.replace("ask ai", "").strip()
        if not question:
            return "Please specify your question for the AI."
        return f"AI query: {question}. Integration with AI providers needed."

    async def _handle_generate(self, command: VoiceCommand) -> str:
        """Handle generate command"""
        request = command.text.replace("generate", "").strip()
        if not request:
            return "Please specify what to generate."
        return f"Generation request: {request}. AI integration needed."

    async def _handle_explain(self, command: VoiceCommand) -> str:
        """Handle explain command"""
        topic = command.text.replace("explain", "").strip()
        if not topic:
            return "Please specify what to explain."
        return f"Explanation request: {topic}. AI integration needed."

    async def _handle_translate(self, command: VoiceCommand) -> str:
        """Handle translate command"""
        text = command.text.replace("translate", "").strip()
        if not text:
            return "Please specify text to translate."
        return f"Translation request: {text}. Translation service integration needed."

    async def start_continuous_listening(self):
        """Start continuous voice listening mode"""
        if not self.recognizer or not self.microphone:
            print("⚠️ Voice recognition not available")
            return

        self.listening_enabled = True
        print("🎤 Starting continuous listening mode...")

        if self.voice_feedback_enabled:
            await self.speak("Continuous listening mode activated. I'm ready for your commands.")

        while self.listening_enabled:
            try:
                # Listen for command
                command = await self.listen_for_command(timeout=3)

                if command and command.text:
                    # Process command
                    processed_command = await self.process_command(command)

                    print(f"✅ Command processed: {processed_command.status.value}")

                    # Check for stop command
                    if "stop listening" in command.text:
                        break

                # Small delay between listening cycles
                await asyncio.sleep(0.5)

            except KeyboardInterrupt:
                print("\n🛑 Stopping continuous listening...")
                break
            except Exception as e:
                print(f"⚠️ Continuous listening error: {e}")
                await asyncio.sleep(1)

        self.listening_enabled = False
        print("🎤 Continuous listening stopped")

        if self.voice_feedback_enabled:
            await self.speak("Voice listening stopped.")

    def get_session(self, session_id: str) -> Optional[VoiceSession]:
        """Get voice session by ID"""
        return self.sessions.get(session_id)

    def list_sessions(self, limit: int = 10) -> List[VoiceSession]:
        """List voice sessions"""
        sessions = list(self.sessions.values())
        return sorted(sessions, key=lambda s: s.start_time, reverse=True)[:limit]

    def get_statistics(self) -> Dict[str, Any]:
        """Get voice control statistics"""
        active_sessions = len([s for s in self.sessions.values() if s.is_active])

        return {
            "total_commands": self.total_commands,
            "successful_recognitions": self.successful_recognitions,
            "failed_recognitions": self.failed_recognitions,
            "recognition_rate": (self.successful_recognitions / max(1, self.total_commands)) * 100,
            "total_sessions": len(self.sessions),
            "active_sessions": active_sessions,
            "current_language": self.current_language.value,
            "listening_enabled": self.listening_enabled,
            "voice_feedback_enabled": self.voice_feedback_enabled,
            "speech_recognition_available": SPEECH_RECOGNITION_AVAILABLE,
            "text_to_speech_available": PYTTSX3_AVAILABLE,
            "audio_input_available": PYAUDIO_AVAILABLE,
            "supported_languages": [lang.value for lang in VoiceLanguage],
            "available_commands": list(self.command_handlers.keys())
        }
