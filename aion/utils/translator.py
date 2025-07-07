"""
🌐 AION Multilingual Translation System
Professional translation support for 7 languages with RTL text handling

This module provides comprehensive multilingual support for AION:
- Arabic (العربية) with RTL text support
- English (English)
- Norwegian (Norsk)
- German (Deutsch)
- French (Français)
- Chinese (中文)
- Spanish (Español)

Features:
- Dynamic language switching
- RTL text handling for Arabic
- Professional translation management
- Fallback to English for missing translations
- Context-aware translation keys
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class Translator:
    """
    Professional multilingual translation system for AION
    
    Provides comprehensive language support with:
    - 7 supported languages with professional translations
    - RTL text handling for Arabic language
    - Dynamic language switching during runtime
    - Fallback mechanisms for missing translations
    - Context-aware translation key management
    - Professional error handling and logging
    """
    
    def __init__(self, default_language: str = "en"):
        self.current_language = default_language
        self.translations: Dict[str, Dict[str, str]] = {}
        self.supported_languages = {
            "ar": "العربية (Arabic)",
            "en": "English",
            "no": "Norsk (Norwegian)", 
            "de": "Deutsch (German)",
            "fr": "Français (French)",
            "zh": "中文 (Chinese)",
            "es": "Español (Spanish)"
        }
        
        # Load all translations
        self._load_translations()
        
        # Set default language
        self.set_language(default_language)
    
    def _load_translations(self):
        """Load all translation files"""
        # Try to find locales directory
        possible_paths = [
            Path(__file__).parent.parent.parent / "locales",  # From aion package
            Path(__file__).parent.parent / "locales",         # From utils
            Path("locales"),                                   # Current directory
            Path(__file__).parent / "locales"                 # Same directory
        ]
        
        locales_dir = None
        for path in possible_paths:
            if path.exists() and path.is_dir():
                locales_dir = path
                break
        
        if not locales_dir:
            # Create default translations in memory
            self._create_default_translations()
            return
        
        # Load translation files
        for lang_code in self.supported_languages.keys():
            lang_file = locales_dir / f"{lang_code}.json"
            if lang_file.exists():
                try:
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        self.translations[lang_code] = json.load(f)
                except Exception as e:
                    print(f"Error loading {lang_code} translations: {e}")
                    self.translations[lang_code] = {}
            else:
                self.translations[lang_code] = {}
        
        # Ensure we have at least English translations
        if not self.translations.get("en"):
            self._create_default_translations()
    
    def _create_default_translations(self):
        """Create default translations in memory"""
        self.translations = {
            "en": {
                "welcome": "Welcome to AION",
                "select_language": "Select Language",
                "select_interface": "Select Interface",
                "cli_interface": "Command Line Interface",
                "tui_interface": "Terminal User Interface", 
                "web_interface": "Web Interface",
                "ai_mode_title": "AI Assistant Mode",
                "ai_mode_help": "Enter your AI requests. Type 'back' to return.",
                "processing": "Processing...",
                "goodbye_message": "Goodbye! Thanks for using AION!",
                "invalid_choice": "Invalid choice. Please try again.",
                "enter_choice": "Enter your choice",
                "main_menu": "Main Menu",
                "system_commands": "System Commands",
                "execute_code": "Execute Code",
                "plugins": "Plugins",
                "settings": "Settings",
                "help": "Help",
                "exit": "Exit"
            },
            "ar": {
                "welcome": "مرحباً بك في AION",
                "select_language": "اختر اللغة",
                "select_interface": "اختر الواجهة",
                "cli_interface": "واجهة سطر الأوامر",
                "tui_interface": "واجهة المحطة النصية",
                "web_interface": "الواجهة الويب",
                "ai_mode_title": "وضع المساعد الذكي",
                "ai_mode_help": "أدخل طلباتك للذكاء الاصطناعي. اكتب 'رجوع' للعودة.",
                "processing": "جاري المعالجة...",
                "goodbye_message": "وداعاً! شكراً لاستخدام AION!",
                "invalid_choice": "اختيار غير صحيح. حاول مرة أخرى.",
                "enter_choice": "أدخل اختيارك",
                "main_menu": "القائمة الرئيسية",
                "system_commands": "أوامر النظام",
                "execute_code": "تنفيذ الكود",
                "plugins": "الإضافات",
                "settings": "الإعدادات",
                "help": "المساعدة",
                "exit": "خروج"
            },
            "de": {
                "welcome": "Willkommen bei AION",
                "select_language": "Sprache auswählen",
                "select_interface": "Schnittstelle auswählen",
                "cli_interface": "Kommandozeilen-Schnittstelle",
                "tui_interface": "Terminal-Benutzeroberfläche",
                "web_interface": "Web-Schnittstelle",
                "ai_mode_title": "KI-Assistent-Modus",
                "ai_mode_help": "Geben Sie Ihre KI-Anfragen ein. Tippen Sie 'zurück' zum Zurückkehren.",
                "processing": "Verarbeitung...",
                "goodbye_message": "Auf Wiedersehen! Danke für die Nutzung von AION!",
                "invalid_choice": "Ungültige Auswahl. Bitte versuchen Sie es erneut.",
                "enter_choice": "Geben Sie Ihre Auswahl ein",
                "main_menu": "Hauptmenü",
                "system_commands": "Systembefehle",
                "execute_code": "Code ausführen",
                "plugins": "Plugins",
                "settings": "Einstellungen",
                "help": "Hilfe",
                "exit": "Beenden"
            },
            "fr": {
                "welcome": "Bienvenue dans AION",
                "select_language": "Sélectionner la langue",
                "select_interface": "Sélectionner l'interface",
                "cli_interface": "Interface en ligne de commande",
                "tui_interface": "Interface utilisateur terminal",
                "web_interface": "Interface Web",
                "ai_mode_title": "Mode Assistant IA",
                "ai_mode_help": "Entrez vos demandes IA. Tapez 'retour' pour revenir.",
                "processing": "Traitement...",
                "goodbye_message": "Au revoir! Merci d'utiliser AION!",
                "invalid_choice": "Choix invalide. Veuillez réessayer.",
                "enter_choice": "Entrez votre choix",
                "main_menu": "Menu Principal",
                "system_commands": "Commandes Système",
                "execute_code": "Exécuter le Code",
                "plugins": "Plugins",
                "settings": "Paramètres",
                "help": "Aide",
                "exit": "Sortir"
            },
            "es": {
                "welcome": "Bienvenido a AION",
                "select_language": "Seleccionar idioma",
                "select_interface": "Seleccionar interfaz",
                "cli_interface": "Interfaz de línea de comandos",
                "tui_interface": "Interfaz de usuario de terminal",
                "web_interface": "Interfaz Web",
                "ai_mode_title": "Modo Asistente IA",
                "ai_mode_help": "Ingrese sus solicitudes de IA. Escriba 'atrás' para volver.",
                "processing": "Procesando...",
                "goodbye_message": "¡Adiós! ¡Gracias por usar AION!",
                "invalid_choice": "Opción inválida. Por favor intente de nuevo.",
                "enter_choice": "Ingrese su opción",
                "main_menu": "Menú Principal",
                "system_commands": "Comandos del Sistema",
                "execute_code": "Ejecutar Código",
                "plugins": "Plugins",
                "settings": "Configuración",
                "help": "Ayuda",
                "exit": "Salir"
            },
            "no": {
                "welcome": "Velkommen til AION",
                "select_language": "Velg språk",
                "select_interface": "Velg grensesnitt",
                "cli_interface": "Kommandolinje-grensesnitt",
                "tui_interface": "Terminal brukergrensesnitt",
                "web_interface": "Web-grensesnitt",
                "ai_mode_title": "AI-assistent modus",
                "ai_mode_help": "Skriv inn dine AI-forespørsler. Skriv 'tilbake' for å gå tilbake.",
                "processing": "Behandler...",
                "goodbye_message": "Ha det! Takk for at du brukte AION!",
                "invalid_choice": "Ugyldig valg. Vennligst prøv igjen.",
                "enter_choice": "Skriv inn ditt valg",
                "main_menu": "Hovedmeny",
                "system_commands": "Systemkommandoer",
                "execute_code": "Kjør kode",
                "plugins": "Plugins",
                "settings": "Innstillinger",
                "help": "Hjelp",
                "exit": "Avslutt"
            },
            "zh": {
                "welcome": "欢迎使用 AION",
                "select_language": "选择语言",
                "select_interface": "选择界面",
                "cli_interface": "命令行界面",
                "tui_interface": "终端用户界面",
                "web_interface": "网页界面",
                "ai_mode_title": "AI助手模式",
                "ai_mode_help": "输入您的AI请求。输入'返回'以返回。",
                "processing": "处理中...",
                "goodbye_message": "再见！感谢使用AION！",
                "invalid_choice": "无效选择。请重试。",
                "enter_choice": "输入您的选择",
                "main_menu": "主菜单",
                "system_commands": "系统命令",
                "execute_code": "执行代码",
                "plugins": "插件",
                "settings": "设置",
                "help": "帮助",
                "exit": "退出"
            }
        }
    
    def set_language(self, language_code: str):
        """Set the current language"""
        if language_code in self.supported_languages:
            self.current_language = language_code
        else:
            self.current_language = "en"  # Fallback to English
    
    def get(self, key: str, default: str = None) -> str:
        """Get translated text for a key"""
        # Try current language first
        if self.current_language in self.translations:
            if key in self.translations[self.current_language]:
                return self.translations[self.current_language][key]
        
        # Fallback to English
        if "en" in self.translations and key in self.translations["en"]:
            return self.translations["en"][key]
        
        # Return default or key if no translation found
        return default or key
    
    def get_language_name(self, language_code: str) -> str:
        """Get the display name for a language code"""
        return self.supported_languages.get(language_code, language_code)
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get all available languages"""
        return self.supported_languages.copy()
    
    def is_rtl_language(self, language_code: str = None) -> bool:
        """Check if language is right-to-left"""
        lang = language_code or self.current_language
        return lang in ["ar"]  # Arabic is RTL
