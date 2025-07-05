"""
🌍 AION Multilingual Translation System
Supports: Arabic, English, Norwegian, German, French, Chinese, Spanish
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional

class Translator:
    """Multilingual translation system for AION"""
    
    def __init__(self, default_language: str = "en"):
        self.current_language = default_language
        self.translations: Dict[str, Dict[str, str]] = {}
        self.locales_dir = Path(__file__).parent.parent / "locales"
        self.supported_languages = {
            "ar": "العربية",
            "en": "English", 
            "no": "Norsk",
            "de": "Deutsch",
            "fr": "Français",
            "zh": "中文",
            "es": "Español"
        }
        self._load_translations()
    
    def _load_translations(self):
        """Load all translation files"""
        try:
            for lang_code in self.supported_languages.keys():
                lang_file = self.locales_dir / f"{lang_code}.json"
                if lang_file.exists():
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        self.translations[lang_code] = json.load(f)
                else:
                    # Create default translation file if it doesn't exist
                    self._create_default_translation(lang_code)
        except Exception as e:
            print(f"Error loading translations: {e}")
            # Fallback to English
            self.current_language = "en"
    
    def _create_default_translation(self, lang_code: str):
        """Create default translation file for a language"""
        # This will be populated with actual translations
        default_translations = self._get_default_translations(lang_code)
        
        # Ensure locales directory exists
        self.locales_dir.mkdir(exist_ok=True)
        
        lang_file = self.locales_dir / f"{lang_code}.json"
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(default_translations, f, ensure_ascii=False, indent=2)
        
        self.translations[lang_code] = default_translations
    
    def _get_default_translations(self, lang_code: str) -> Dict[str, str]:
        """Get default translations for each language"""
        translations = {
            "en": {
                "main_menu_title": "🤖 AION Main Menu",
                "menu_ai_assistant": "AI Assistant",
                "menu_system_commands": "System Commands",
                "menu_execute_code": "Execute Code",
                "menu_plugins": "Plugins",
                "menu_web_interface": "Web Interface",
                "menu_settings": "Settings",
                "menu_change_language": "Change Language",
                "menu_help": "Help",
                "menu_exit": "Exit",
                "enter_choice": "Enter your choice",
                "invalid_choice": "Invalid choice. Please try again.",
                "goodbye_message": "Thank you for using AION! Goodbye!",
                "welcome_message": "Welcome to AION - AI Operating Node",
                "language_changed": "Language changed successfully",
                "ai_mode_title": "🧠 AI Assistant Mode",
                "system_mode_title": "💻 System Commands Mode",
                "code_mode_title": "📜 Code Execution Mode",
                "plugins_mode_title": "🧩 Plugins Mode",
                "settings_mode_title": "⚙️ Settings",
                "help_title": "❓ Help & Documentation",
                "back_to_menu": "Back to Main Menu",
                "enter_command": "Enter command",
                "processing": "Processing...",
                "error_occurred": "An error occurred",
                "success": "Success",
                "loading": "Loading...",
                "choose_language": "Choose your language"
            },
            "ar": {
                "main_menu_title": "🤖 القائمة الرئيسية لـ AION",
                "menu_ai_assistant": "مساعد الذكاء الاصطناعي",
                "menu_system_commands": "أوامر النظام",
                "menu_execute_code": "تنفيذ الكود",
                "menu_plugins": "الإضافات",
                "menu_web_interface": "واجهة الويب",
                "menu_settings": "الإعدادات",
                "menu_change_language": "تغيير اللغة",
                "menu_help": "المساعدة",
                "menu_exit": "خروج",
                "enter_choice": "أدخل اختيارك",
                "invalid_choice": "اختيار غير صحيح. يرجى المحاولة مرة أخرى.",
                "goodbye_message": "شكراً لاستخدام AION! وداعاً!",
                "welcome_message": "مرحباً بك في AION - عقدة التشغيل الذكية",
                "language_changed": "تم تغيير اللغة بنجاح",
                "ai_mode_title": "🧠 وضع مساعد الذكاء الاصطناعي",
                "system_mode_title": "💻 وضع أوامر النظام",
                "code_mode_title": "📜 وضع تنفيذ الكود",
                "plugins_mode_title": "🧩 وضع الإضافات",
                "settings_mode_title": "⚙️ الإعدادات",
                "help_title": "❓ المساعدة والتوثيق",
                "back_to_menu": "العودة للقائمة الرئيسية",
                "enter_command": "أدخل الأمر",
                "processing": "جاري المعالجة...",
                "error_occurred": "حدث خطأ",
                "success": "نجح",
                "loading": "جاري التحميل...",
                "choose_language": "اختر لغتك"
            },
            "no": {
                "main_menu_title": "🤖 AION Hovedmeny",
                "menu_ai_assistant": "AI Assistent",
                "menu_system_commands": "Systemkommandoer",
                "menu_execute_code": "Kjør Kode",
                "menu_plugins": "Plugins",
                "menu_web_interface": "Web Grensesnitt",
                "menu_settings": "Innstillinger",
                "menu_change_language": "Endre Språk",
                "menu_help": "Hjelp",
                "menu_exit": "Avslutt",
                "enter_choice": "Skriv inn ditt valg",
                "invalid_choice": "Ugyldig valg. Vennligst prøv igjen.",
                "goodbye_message": "Takk for at du brukte AION! Ha det!",
                "welcome_message": "Velkommen til AION - AI Operating Node",
                "language_changed": "Språk endret vellykket",
                "ai_mode_title": "🧠 AI Assistent Modus",
                "system_mode_title": "💻 Systemkommando Modus",
                "code_mode_title": "📜 Kodekjøring Modus",
                "plugins_mode_title": "🧩 Plugin Modus",
                "settings_mode_title": "⚙️ Innstillinger",
                "help_title": "❓ Hjelp & Dokumentasjon",
                "back_to_menu": "Tilbake til Hovedmeny",
                "enter_command": "Skriv inn kommando",
                "processing": "Behandler...",
                "error_occurred": "En feil oppstod",
                "success": "Suksess",
                "loading": "Laster...",
                "choose_language": "Velg ditt språk"
            },
            "de": {
                "main_menu_title": "🤖 AION Hauptmenü",
                "menu_ai_assistant": "KI-Assistent",
                "menu_system_commands": "Systembefehle",
                "menu_execute_code": "Code Ausführen",
                "menu_plugins": "Plugins",
                "menu_web_interface": "Web-Interface",
                "menu_settings": "Einstellungen",
                "menu_change_language": "Sprache Ändern",
                "menu_help": "Hilfe",
                "menu_exit": "Beenden",
                "enter_choice": "Geben Sie Ihre Wahl ein",
                "invalid_choice": "Ungültige Wahl. Bitte versuchen Sie es erneut.",
                "goodbye_message": "Danke für die Nutzung von AION! Auf Wiedersehen!",
                "welcome_message": "Willkommen bei AION - AI Operating Node",
                "language_changed": "Sprache erfolgreich geändert",
                "ai_mode_title": "🧠 KI-Assistent Modus",
                "system_mode_title": "💻 Systembefehl Modus",
                "code_mode_title": "📜 Code-Ausführung Modus",
                "plugins_mode_title": "🧩 Plugin Modus",
                "settings_mode_title": "⚙️ Einstellungen",
                "help_title": "❓ Hilfe & Dokumentation",
                "back_to_menu": "Zurück zum Hauptmenü",
                "enter_command": "Befehl eingeben",
                "processing": "Verarbeitung...",
                "error_occurred": "Ein Fehler ist aufgetreten",
                "success": "Erfolg",
                "loading": "Laden...",
                "choose_language": "Wählen Sie Ihre Sprache"
            },
            "fr": {
                "main_menu_title": "🤖 Menu Principal AION",
                "menu_ai_assistant": "Assistant IA",
                "menu_system_commands": "Commandes Système",
                "menu_execute_code": "Exécuter Code",
                "menu_plugins": "Plugins",
                "menu_web_interface": "Interface Web",
                "menu_settings": "Paramètres",
                "menu_change_language": "Changer Langue",
                "menu_help": "Aide",
                "menu_exit": "Quitter",
                "enter_choice": "Entrez votre choix",
                "invalid_choice": "Choix invalide. Veuillez réessayer.",
                "goodbye_message": "Merci d'avoir utilisé AION! Au revoir!",
                "welcome_message": "Bienvenue dans AION - AI Operating Node",
                "language_changed": "Langue changée avec succès",
                "ai_mode_title": "🧠 Mode Assistant IA",
                "system_mode_title": "💻 Mode Commandes Système",
                "code_mode_title": "📜 Mode Exécution Code",
                "plugins_mode_title": "🧩 Mode Plugins",
                "settings_mode_title": "⚙️ Paramètres",
                "help_title": "❓ Aide & Documentation",
                "back_to_menu": "Retour au Menu Principal",
                "enter_command": "Entrer commande",
                "processing": "Traitement...",
                "error_occurred": "Une erreur s'est produite",
                "success": "Succès",
                "loading": "Chargement...",
                "choose_language": "Choisissez votre langue"
            },
            "zh": {
                "main_menu_title": "🤖 AION 主菜单",
                "menu_ai_assistant": "AI 助手",
                "menu_system_commands": "系统命令",
                "menu_execute_code": "执行代码",
                "menu_plugins": "插件",
                "menu_web_interface": "网页界面",
                "menu_settings": "设置",
                "menu_change_language": "更改语言",
                "menu_help": "帮助",
                "menu_exit": "退出",
                "enter_choice": "请输入您的选择",
                "invalid_choice": "无效选择。请重试。",
                "goodbye_message": "感谢使用 AION！再见！",
                "welcome_message": "欢迎使用 AION - AI 操作节点",
                "language_changed": "语言更改成功",
                "ai_mode_title": "🧠 AI 助手模式",
                "system_mode_title": "💻 系统命令模式",
                "code_mode_title": "📜 代码执行模式",
                "plugins_mode_title": "🧩 插件模式",
                "settings_mode_title": "⚙️ 设置",
                "help_title": "❓ 帮助与文档",
                "back_to_menu": "返回主菜单",
                "enter_command": "输入命令",
                "processing": "处理中...",
                "error_occurred": "发生错误",
                "success": "成功",
                "loading": "加载中...",
                "choose_language": "选择您的语言"
            },
            "es": {
                "main_menu_title": "🤖 Menú Principal AION",
                "menu_ai_assistant": "Asistente IA",
                "menu_system_commands": "Comandos del Sistema",
                "menu_execute_code": "Ejecutar Código",
                "menu_plugins": "Plugins",
                "menu_web_interface": "Interfaz Web",
                "menu_settings": "Configuración",
                "menu_change_language": "Cambiar Idioma",
                "menu_help": "Ayuda",
                "menu_exit": "Salir",
                "enter_choice": "Ingrese su elección",
                "invalid_choice": "Elección inválida. Por favor intente de nuevo.",
                "goodbye_message": "¡Gracias por usar AION! ¡Adiós!",
                "welcome_message": "Bienvenido a AION - AI Operating Node",
                "language_changed": "Idioma cambiado exitosamente",
                "ai_mode_title": "🧠 Modo Asistente IA",
                "system_mode_title": "💻 Modo Comandos del Sistema",
                "code_mode_title": "📜 Modo Ejecución de Código",
                "plugins_mode_title": "🧩 Modo Plugins",
                "settings_mode_title": "⚙️ Configuración",
                "help_title": "❓ Ayuda y Documentación",
                "back_to_menu": "Volver al Menú Principal",
                "enter_command": "Ingresar comando",
                "processing": "Procesando...",
                "error_occurred": "Ocurrió un error",
                "success": "Éxito",
                "loading": "Cargando...",
                "choose_language": "Elija su idioma"
            }
        }
        
        return translations.get(lang_code, translations["en"])
    
    def set_language(self, language_code: str):
        """Set the current language"""
        if language_code in self.supported_languages:
            self.current_language = language_code
            return True
        return False
    
    def get(self, key: str, default: Optional[str] = None) -> str:
        """Get translated text for the current language"""
        try:
            if self.current_language in self.translations:
                return self.translations[self.current_language].get(key, default or key)
            else:
                # Fallback to English
                return self.translations.get("en", {}).get(key, default or key)
        except Exception:
            return default or key
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return self.supported_languages.copy()
    
    def get_current_language(self) -> str:
        """Get current language code"""
        return self.current_language
    
    def get_current_language_name(self) -> str:
        """Get current language name"""
        return self.supported_languages.get(self.current_language, "English")
