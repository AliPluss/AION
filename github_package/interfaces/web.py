"""
🌐 AION Web Interface
FastAPI-based web interface with multilingual support
"""

from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
from pathlib import Path
from typing import Optional, Dict, Any
import json

from utils.translator import Translator
from core.security import SecurityManager

class WebInterface:
    """Web interface for AION"""
    
    def __init__(self, translator: Translator):
        self.translator = translator
        self.security = SecurityManager()
        self.app = FastAPI(
            title="AION Web Interface",
            description="AI Operating Node Web Interface",
            version="1.0.0"
        )
        
        # Setup templates and static files
        self.templates_dir = Path(__file__).parent.parent / "templates"
        self.static_dir = Path(__file__).parent.parent / "static"
        
        # Create directories if they don't exist
        self.templates_dir.mkdir(exist_ok=True)
        self.static_dir.mkdir(exist_ok=True)
        
        # Setup Jinja2 templates
        self.templates = Jinja2Templates(directory=str(self.templates_dir))
        
        # Mount static files
        if self.static_dir.exists():
            self.app.mount("/static", StaticFiles(directory=str(self.static_dir)), name="static")
        
        # Setup routes
        self._setup_routes()
        
        # Create default templates if they don't exist
        self._create_default_templates()
    
    def _setup_routes(self):
        """Setup web routes"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
            """Home page"""
            return self.templates.TemplateResponse("index.html", {
                "request": request,
                "title": "AION - AI Operating Node",
                "translator": self.translator,
                "current_language": self.translator.get_current_language(),
                "supported_languages": self.translator.get_supported_languages()
            })
        
        @self.app.get("/api/languages")
        async def get_languages():
            """Get supported languages"""
            return {
                "current": self.translator.get_current_language(),
                "supported": self.translator.get_supported_languages()
            }
        
        @self.app.post("/api/language")
        async def set_language(language: str = Form(...)):
            """Set current language"""
            if self.translator.set_language(language):
                return {"success": True, "message": self.translator.get("language_changed")}
            else:
                raise HTTPException(status_code=400, detail="Invalid language")
        
        @self.app.get("/api/translate/{key}")
        async def translate_key(key: str):
            """Get translation for a key"""
            return {"key": key, "translation": self.translator.get(key)}
        
        @self.app.post("/api/ai/chat")
        async def ai_chat(message: str = Form(...)):
            """AI chat endpoint"""
            # Placeholder for AI integration
            response = f"{self.translator.get('ai_placeholder', 'AI response coming soon!')}"
            return {"response": response}
        
        @self.app.post("/api/system/command")
        async def execute_command(command: str = Form(...)):
            """Execute system command"""
            if not self.security.is_command_allowed(command):
                raise HTTPException(status_code=403, detail="Command not allowed")
            
            # Placeholder for command execution
            return {
                "command": command,
                "output": f"{self.translator.get('command_placeholder', 'Command execution coming soon!')}"
            }
        
        @self.app.post("/api/code/execute")
        async def execute_code(code: str = Form(...), language: str = Form(...)):
            """Execute code"""
            # Placeholder for code execution
            return {
                "language": language,
                "code": code,
                "output": f"{self.translator.get('code_placeholder', 'Code execution coming soon!')}"
            }
        
        @self.app.get("/api/security/status")
        async def security_status():
            """Get security status"""
            return self.security.get_security_status()
    
    def _create_default_templates(self):
        """Create default HTML templates"""
        
        # Create index.html template
        index_template = """
<!DOCTYPE html>
<html lang="{{ current_language }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .logo {
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .language-selector {
            position: absolute;
            top: 20px;
            right: 20px;
        }
        
        .language-selector select {
            padding: 8px 12px;
            border: none;
            border-radius: 5px;
            background: rgba(255,255,255,0.2);
            color: white;
            font-size: 14px;
        }
        
        .modules {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }
        
        .module {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            cursor: pointer;
            backdrop-filter: blur(10px);
        }
        
        .module:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        .module-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        
        .module-title {
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .module-description {
            opacity: 0.8;
            line-height: 1.5;
        }
        
        .chat-container {
            display: none;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            backdrop-filter: blur(10px);
        }
        
        .chat-messages {
            height: 300px;
            overflow-y: auto;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            background: rgba(0,0,0,0.1);
        }
        
        .chat-input {
            display: flex;
            gap: 10px;
        }
        
        .chat-input input {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 8px;
            background: rgba(255,255,255,0.2);
            color: white;
            font-size: 16px;
        }
        
        .chat-input input::placeholder {
            color: rgba(255,255,255,0.7);
        }
        
        .chat-input button {
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            background: #4CAF50;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        
        .chat-input button:hover {
            background: #45a049;
        }
        
        .message {
            margin-bottom: 10px;
            padding: 8px 12px;
            border-radius: 8px;
        }
        
        .user-message {
            background: rgba(33, 150, 243, 0.3);
            text-align: right;
        }
        
        .ai-message {
            background: rgba(76, 175, 80, 0.3);
        }
    </style>
</head>
<body>
    <div class="language-selector">
        <select id="languageSelect" onchange="changeLanguage()">
            {% for code, name in supported_languages.items() %}
            <option value="{{ code }}" {% if code == current_language %}selected{% endif %}>
                {{ name }}
            </option>
            {% endfor %}
        </select>
    </div>
    
    <div class="container">
        <div class="header">
            <div class="logo">🤖 AION</div>
            <div class="subtitle">{{ translator.get('welcome_message') }}</div>
        </div>
        
        <div class="modules">
            <div class="module" onclick="showModule('ai')">
                <div class="module-icon">🧠</div>
                <div class="module-title">{{ translator.get('menu_ai_assistant') }}</div>
                <div class="module-description">{{ translator.get('ai_description', 'AI-powered code generation and assistance') }}</div>
            </div>
            
            <div class="module" onclick="showModule('system')">
                <div class="module-icon">💻</div>
                <div class="module-title">{{ translator.get('menu_system_commands') }}</div>
                <div class="module-description">{{ translator.get('system_description', 'Execute and explain system commands') }}</div>
            </div>
            
            <div class="module" onclick="showModule('code')">
                <div class="module-icon">📜</div>
                <div class="module-title">{{ translator.get('menu_execute_code') }}</div>
                <div class="module-description">{{ translator.get('code_description', 'Multi-language code execution') }}</div>
            </div>
            
            <div class="module" onclick="showModule('plugins')">
                <div class="module-icon">🧩</div>
                <div class="module-title">{{ translator.get('menu_plugins') }}</div>
                <div class="module-description">{{ translator.get('plugins_description', 'Extensible plugin system') }}</div>
            </div>
        </div>
        
        <div id="aiChat" class="chat-container">
            <h3>🧠 {{ translator.get('menu_ai_assistant') }}</h3>
            <div id="chatMessages" class="chat-messages"></div>
            <div class="chat-input">
                <input type="text" id="chatInput" placeholder="{{ translator.get('enter_message', 'Enter your message...') }}" onkeypress="handleChatKeyPress(event)">
                <button onclick="sendMessage()">{{ translator.get('send', 'Send') }}</button>
            </div>
        </div>
    </div>
    
    <script>
        function changeLanguage() {
            const select = document.getElementById('languageSelect');
            const language = select.value;
            
            fetch('/api/language', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `language=${language}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                }
            });
        }
        
        function showModule(module) {
            // Hide all modules
            document.querySelectorAll('.chat-container').forEach(el => {
                el.style.display = 'none';
            });
            
            if (module === 'ai') {
                document.getElementById('aiChat').style.display = 'block';
            } else {
                alert(`${module} module coming soon! 🚧`);
            }
        }
        
        function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            
            if (message) {
                addMessage(message, 'user');
                input.value = '';
                
                fetch('/api/ai/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `message=${encodeURIComponent(message)}`
                })
                .then(response => response.json())
                .then(data => {
                    addMessage(data.response, 'ai');
                });
            }
        }
        
        function addMessage(message, sender) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            messageDiv.textContent = `${sender === 'user' ? '👤' : '🤖'} ${message}`;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function handleChatKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
    </script>
</body>
</html>
        """
        
        index_file = self.templates_dir / "index.html"
        if not index_file.exists():
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_template)
    
    def start(self, host: str = "127.0.0.1", port: int = 8000):
        """Start the web server"""
        print(f"🌐 Starting AION Web Interface at http://{host}:{port}")
        print(f"🌍 Current language: {self.translator.get_current_language_name()}")
        
        uvicorn.run(
            self.app,
            host=host,
            port=port,
            log_level="info"
        )
