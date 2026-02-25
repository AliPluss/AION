"""
AION Advanced Settings Manager
Advanced settings manager with encryption and synchronization
"""

import json
import threading
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, Callable
from datetime import datetime
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import base64

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

class SettingType(Enum):
    """Setting types"""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"
    PASSWORD = "password"
    PATH = "path"
    URL = "url"
    EMAIL = "email"

class SettingScope(Enum):
    """Setting scopes"""
    GLOBAL = "global"
    USER = "user"
    SESSION = "session"
    TEMPORARY = "temporary"

@dataclass
class SettingDefinition:
    """تعريف إعداد"""
    key: str
    name: str
    description: str
    setting_type: SettingType
    scope: SettingScope
    default_value: Any
    required: bool = False
    encrypted: bool = False
    validation_pattern: Optional[str] = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    allowed_values: Optional[List[Any]] = None
    category: str = "general"
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

@dataclass
class SettingValue:
    """قيمة إعداد"""
    key: str
    value: Any
    encrypted: bool
    last_modified: datetime
    modified_by: str
    scope: SettingScope
    version: int = 1

class AdvancedSettingsManager:
    """Advanced settings manager"""
    
    def __init__(self, config_dir: Optional[Path] = None, encryption_key: Optional[str] = None):
        self.config_dir = config_dir or Path.cwd() / "config"
        self.config_dir.mkdir(exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
        
        # ملفات الإعدادات
        self.settings_file = self.config_dir / "settings.json"
        self.definitions_file = self.config_dir / "setting_definitions.json"
        self.encrypted_file = self.config_dir / "encrypted_settings.dat"
        self.backup_dir = self.config_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # إعداد التشفير
        self.encryption_key = encryption_key
        self.cipher = None
        if CRYPTO_AVAILABLE and encryption_key:
            self._setup_encryption(encryption_key)
        
        # بيانات الإعدادات
        self.settings: Dict[str, SettingValue] = {}
        self.definitions: Dict[str, SettingDefinition] = {}
        self.watchers: Dict[str, List[Callable]] = {}
        
        # إعدادات النظام
        self.lock = threading.RLock()
        self.auto_save = True
        self.backup_enabled = True
        self.max_backups = 10
        
        # تحميل البيانات
        self._load_definitions()
        self._load_settings()
        
        # إعداد الإعدادات الافتراضية
        self._setup_default_settings()
    
    def _setup_encryption(self, key: str):
        """إعداد التشفير"""
        try:
            # إنشاء مفتاح تشفير من النص
            key_bytes = key.encode('utf-8')
            key_hash = hashlib.sha256(key_bytes).digest()
            fernet_key = base64.urlsafe_b64encode(key_hash)
            self.cipher = Fernet(fernet_key)
            
        except Exception as e:
            self.logger.error(f"Error setting up encryption: {e}")
            self.cipher = None
    
    def _setup_default_settings(self):
        """إعداد الإعدادات الافتراضية"""
        default_definitions = [
            # إعدادات عامة
            SettingDefinition(
                key="app.name",
                name="Application Name",
                description="Name of the application",
                setting_type=SettingType.STRING,
                scope=SettingScope.GLOBAL,
                default_value="AION",
                category="general"
            ),
            SettingDefinition(
                key="app.version",
                name="Application Version",
                description="Version of the application",
                setting_type=SettingType.STRING,
                scope=SettingScope.GLOBAL,
                default_value="1.0.0",
                category="general"
            ),
            SettingDefinition(
                key="app.language",
                name="Interface Language",
                description="Default interface language",
                setting_type=SettingType.STRING,
                scope=SettingScope.USER,
                default_value="en",
                allowed_values=["en", "ar", "de", "fr", "es", "zh", "no"],
                category="interface"
            ),
            SettingDefinition(
                key="app.theme",
                name="Interface Theme",
                description="Application theme",
                setting_type=SettingType.STRING,
                scope=SettingScope.USER,
                default_value="dark",
                allowed_values=["light", "dark", "auto"],
                category="interface"
            ),
            
            # إعدادات الأمان
            SettingDefinition(
                key="security.encryption_enabled",
                name="Enable Encryption",
                description="Enable data encryption",
                setting_type=SettingType.BOOLEAN,
                scope=SettingScope.GLOBAL,
                default_value=True,
                category="security"
            ),
            SettingDefinition(
                key="security.session_timeout",
                name="Session Timeout",
                description="Session timeout in minutes",
                setting_type=SettingType.INTEGER,
                scope=SettingScope.GLOBAL,
                default_value=30,
                min_value=5,
                max_value=480,
                category="security"
            ),
            SettingDefinition(
                key="security.max_login_attempts",
                name="Max Login Attempts",
                description="Maximum login attempts before lockout",
                setting_type=SettingType.INTEGER,
                scope=SettingScope.GLOBAL,
                default_value=3,
                min_value=1,
                max_value=10,
                category="security"
            ),
            
            # إعدادات الذكاء الاصطناعي
            SettingDefinition(
                key="ai.default_provider",
                name="Default AI Provider",
                description="Default AI service provider",
                setting_type=SettingType.STRING,
                scope=SettingScope.USER,
                default_value="openai",
                allowed_values=["openai", "deepseek", "openrouter", "gemini"],
                category="ai"
            ),
            SettingDefinition(
                key="ai.api_key",
                name="AI API Key",
                description="API key for AI services",
                setting_type=SettingType.PASSWORD,
                scope=SettingScope.USER,
                default_value="",
                encrypted=True,
                required=True,
                category="ai"
            ),
            SettingDefinition(
                key="ai.max_tokens",
                name="Max Tokens",
                description="Maximum tokens per request",
                setting_type=SettingType.INTEGER,
                scope=SettingScope.USER,
                default_value=4000,
                min_value=100,
                max_value=32000,
                category="ai"
            ),
            SettingDefinition(
                key="ai.temperature",
                name="AI Temperature",
                description="AI response creativity (0.0-2.0)",
                setting_type=SettingType.FLOAT,
                scope=SettingScope.USER,
                default_value=0.7,
                min_value=0.0,
                max_value=2.0,
                category="ai"
            ),
            
            # إعدادات الأداء
            SettingDefinition(
                key="performance.max_workers",
                name="Max Workers",
                description="Maximum number of worker threads",
                setting_type=SettingType.INTEGER,
                scope=SettingScope.GLOBAL,
                default_value=4,
                min_value=1,
                max_value=16,
                category="performance"
            ),
            SettingDefinition(
                key="performance.cache_size",
                name="Cache Size",
                description="Maximum cache size in MB",
                setting_type=SettingType.INTEGER,
                scope=SettingScope.GLOBAL,
                default_value=100,
                min_value=10,
                max_value=1000,
                category="performance"
            ),
            SettingDefinition(
                key="performance.auto_cleanup",
                name="Auto Cleanup",
                description="Enable automatic cleanup of temporary files",
                setting_type=SettingType.BOOLEAN,
                scope=SettingScope.GLOBAL,
                default_value=True,
                category="performance"
            ),
            
            # إعدادات التسجيل
            SettingDefinition(
                key="logging.level",
                name="Log Level",
                description="Logging level",
                setting_type=SettingType.STRING,
                scope=SettingScope.GLOBAL,
                default_value="INFO",
                allowed_values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                category="logging"
            ),
            SettingDefinition(
                key="logging.file_enabled",
                name="File Logging",
                description="Enable logging to file",
                setting_type=SettingType.BOOLEAN,
                scope=SettingScope.GLOBAL,
                default_value=True,
                category="logging"
            ),
            SettingDefinition(
                key="logging.max_file_size",
                name="Max Log File Size",
                description="Maximum log file size in MB",
                setting_type=SettingType.INTEGER,
                scope=SettingScope.GLOBAL,
                default_value=10,
                min_value=1,
                max_value=100,
                category="logging"
            ),
            
            # إعدادات التكامل
            SettingDefinition(
                key="integrations.email_enabled",
                name="Email Integration",
                description="Enable email integration",
                setting_type=SettingType.BOOLEAN,
                scope=SettingScope.USER,
                default_value=False,
                category="integrations"
            ),
            SettingDefinition(
                key="integrations.github_enabled",
                name="GitHub Integration",
                description="Enable GitHub integration",
                setting_type=SettingType.BOOLEAN,
                scope=SettingScope.USER,
                default_value=False,
                category="integrations"
            ),
            SettingDefinition(
                key="integrations.slack_enabled",
                name="Slack Integration",
                description="Enable Slack integration",
                setting_type=SettingType.BOOLEAN,
                scope=SettingScope.USER,
                default_value=False,
                category="integrations"
            )
        ]
        
        # إضافة التعريفات الافتراضية
        for definition in default_definitions:
            if definition.key not in self.definitions:
                self.definitions[definition.key] = definition
                
                # إضافة القيمة الافتراضية إذا لم تكن موجودة
                if definition.key not in self.settings:
                    self.set_setting(definition.key, definition.default_value, save=False)
        
        # حفظ التعريفات
        self._save_definitions()
        
        # حفظ الإعدادات
        if self.auto_save:
            self._save_settings()
    
    def _load_definitions(self):
        """تحميل تعريفات الإعدادات"""
        try:
            if self.definitions_file.exists():
                with open(self.definitions_file, 'r', encoding='utf-8') as f:
                    definitions_data = json.load(f)
                
                for key, def_data in definitions_data.items():
                    # تحويل enums
                    def_data["setting_type"] = SettingType(def_data["setting_type"])
                    def_data["scope"] = SettingScope(def_data["scope"])
                    
                    definition = SettingDefinition(**def_data)
                    self.definitions[key] = definition
                    
        except Exception as e:
            self.logger.error(f"Error loading setting definitions: {e}")
    
    def _save_definitions(self):
        """حفظ تعريفات الإعدادات"""
        try:
            definitions_data = {}
            for key, definition in self.definitions.items():
                definitions_data[key] = asdict(definition)
            
            with open(self.definitions_file, 'w', encoding='utf-8') as f:
                json.dump(definitions_data, f, indent=2, ensure_ascii=False, default=str)
                
        except Exception as e:
            self.logger.error(f"Error saving setting definitions: {e}")
    
    def _load_settings(self):
        """تحميل الإعدادات"""
        try:
            # تحميل الإعدادات العادية
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings_data = json.load(f)
                
                for key, setting_data in settings_data.items():
                    # تحويل التاريخ
                    setting_data["last_modified"] = datetime.fromisoformat(setting_data["last_modified"])
                    setting_data["scope"] = SettingScope(setting_data["scope"])
                    
                    setting = SettingValue(**setting_data)
                    self.settings[key] = setting
            
            # تحميل الإعدادات المشفرة
            if self.cipher and self.encrypted_file.exists():
                with open(self.encrypted_file, 'rb') as f:
                    encrypted_data = f.read()
                
                try:
                    decrypted_data = self.cipher.decrypt(encrypted_data)
                    encrypted_settings = json.loads(decrypted_data.decode('utf-8'))
                    
                    for key, setting_data in encrypted_settings.items():
                        setting_data["last_modified"] = datetime.fromisoformat(setting_data["last_modified"])
                        setting_data["scope"] = SettingScope(setting_data["scope"])
                        
                        setting = SettingValue(**setting_data)
                        self.settings[key] = setting
                        
                except Exception as e:
                    self.logger.error(f"Error decrypting settings: {e}")
                    
        except Exception as e:
            self.logger.error(f"Error loading settings: {e}")
    
    def _save_settings(self):
        """حفظ الإعدادات"""
        try:
            with self.lock:
                # إنشاء نسخة احتياطية
                if self.backup_enabled:
                    self._create_backup()
                
                # فصل الإعدادات المشفرة وغير المشفرة
                regular_settings = {}
                encrypted_settings = {}
                
                for key, setting in self.settings.items():
                    setting_dict = asdict(setting)
                    
                    if setting.encrypted and self.cipher:
                        encrypted_settings[key] = setting_dict
                    else:
                        regular_settings[key] = setting_dict
                
                # حفظ الإعدادات العادية
                if regular_settings:
                    with open(self.settings_file, 'w', encoding='utf-8') as f:
                        json.dump(regular_settings, f, indent=2, ensure_ascii=False, default=str)
                
                # حفظ الإعدادات المشفرة
                if encrypted_settings and self.cipher:
                    encrypted_json = json.dumps(encrypted_settings, ensure_ascii=False, default=str)
                    encrypted_data = self.cipher.encrypt(encrypted_json.encode('utf-8'))
                    
                    with open(self.encrypted_file, 'wb') as f:
                        f.write(encrypted_data)
                        
        except Exception as e:
            self.logger.error(f"Error saving settings: {e}")
    
    def _create_backup(self):
        """إنشاء نسخة احتياطية"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"settings_backup_{timestamp}.json"
            
            # نسخ الإعدادات الحالية
            if self.settings_file.exists():
                import shutil
                shutil.copy2(self.settings_file, backup_file)
            
            # تنظيف النسخ الاحتياطية القديمة
            self._cleanup_old_backups()
            
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
    
    def _cleanup_old_backups(self):
        """تنظيف النسخ الاحتياطية القديمة"""
        try:
            backup_files = list(self.backup_dir.glob("settings_backup_*.json"))
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # حذف النسخ الزائدة
            for backup_file in backup_files[self.max_backups:]:
                backup_file.unlink()
                
        except Exception as e:
            self.logger.error(f"Error cleaning up backups: {e}")

    def set_setting(self, key: str, value: Any, user: str = "system", save: bool = True) -> bool:
        """تعيين قيمة إعداد"""
        try:
            with self.lock:
                # فحص وجود التعريف
                if key not in self.definitions:
                    self.logger.warning(f"Setting definition not found: {key}")
                    return False

                definition = self.definitions[key]

                # التحقق من صحة القيمة
                if not self._validate_value(key, value):
                    return False

                # تحديد ما إذا كان الإعداد مشفراً
                encrypted = definition.encrypted and self.cipher is not None

                # إنشاء أو تحديث الإعداد
                if key in self.settings:
                    setting = self.settings[key]
                    old_value = setting.value
                    setting.value = value
                    setting.last_modified = datetime.now()
                    setting.modified_by = user
                    setting.version += 1
                    setting.encrypted = encrypted
                else:
                    setting = SettingValue(
                        key=key,
                        value=value,
                        encrypted=encrypted,
                        last_modified=datetime.now(),
                        modified_by=user,
                        scope=definition.scope
                    )
                    old_value = None

                self.settings[key] = setting

                # حفظ تلقائي
                if save and self.auto_save:
                    self._save_settings()

                # إشعار المراقبين
                self._notify_watchers(key, old_value, value)

                return True

        except Exception as e:
            self.logger.error(f"Error setting value for {key}: {e}")
            return False

    def get_setting(self, key: str, default: Any = None) -> Any:
        """الحصول على قيمة إعداد"""
        try:
            if key in self.settings:
                return self.settings[key].value

            # البحث عن القيمة الافتراضية في التعريف
            if key in self.definitions:
                return self.definitions[key].default_value

            return default

        except Exception as e:
            self.logger.error(f"Error getting setting {key}: {e}")
            return default

    def get_setting_info(self, key: str) -> Optional[Dict[str, Any]]:
        """الحصول على معلومات كاملة عن إعداد"""
        try:
            if key not in self.definitions:
                return None

            definition = self.definitions[key]
            setting = self.settings.get(key)

            info = {
                "key": key,
                "name": definition.name,
                "description": definition.description,
                "type": definition.setting_type.value,
                "scope": definition.scope.value,
                "category": definition.category,
                "tags": definition.tags,
                "required": definition.required,
                "encrypted": definition.encrypted,
                "default_value": definition.default_value,
                "current_value": setting.value if setting else definition.default_value,
                "validation": {
                    "pattern": definition.validation_pattern,
                    "min_value": definition.min_value,
                    "max_value": definition.max_value,
                    "allowed_values": definition.allowed_values
                }
            }

            if setting:
                info.update({
                    "last_modified": setting.last_modified.isoformat(),
                    "modified_by": setting.modified_by,
                    "version": setting.version
                })

            return info

        except Exception as e:
            self.logger.error(f"Error getting setting info for {key}: {e}")
            return None

    def _validate_value(self, key: str, value: Any) -> bool:
        """التحقق من صحة قيمة الإعداد"""
        try:
            if key not in self.definitions:
                return False

            definition = self.definitions[key]

            # فحص النوع
            if definition.setting_type == SettingType.STRING:
                if not isinstance(value, str):
                    return False
            elif definition.setting_type == SettingType.INTEGER:
                if not isinstance(value, int):
                    return False
                if definition.min_value is not None and value < definition.min_value:
                    return False
                if definition.max_value is not None and value > definition.max_value:
                    return False
            elif definition.setting_type == SettingType.FLOAT:
                if not isinstance(value, (int, float)):
                    return False
                if definition.min_value is not None and value < definition.min_value:
                    return False
                if definition.max_value is not None and value > definition.max_value:
                    return False
            elif definition.setting_type == SettingType.BOOLEAN:
                if not isinstance(value, bool):
                    return False
            elif definition.setting_type == SettingType.LIST:
                if not isinstance(value, list):
                    return False
            elif definition.setting_type == SettingType.DICT:
                if not isinstance(value, dict):
                    return False
            elif definition.setting_type in [SettingType.PASSWORD, SettingType.PATH,
                                           SettingType.URL, SettingType.EMAIL]:
                if not isinstance(value, str):
                    return False

            # فحص القيم المسموحة
            if definition.allowed_values and value not in definition.allowed_values:
                return False

            # فحص النمط (regex)
            if definition.validation_pattern and isinstance(value, str):
                import re
                if not re.match(definition.validation_pattern, value):
                    return False

            return True

        except Exception as e:
            self.logger.error(f"Error validating value for {key}: {e}")
            return False

    def _notify_watchers(self, key: str, old_value: Any, new_value: Any):
        """إشعار مراقبي الإعدادات"""
        try:
            if key in self.watchers:
                for callback in self.watchers[key]:
                    try:
                        callback(key, old_value, new_value)
                    except Exception as e:
                        self.logger.error(f"Error in setting watcher callback: {e}")

        except Exception as e:
            self.logger.error(f"Error notifying watchers: {e}")

    def watch_setting(self, key: str, callback: Callable[[str, Any, Any], None]):
        """مراقبة تغييرات إعداد معين"""
        try:
            if key not in self.watchers:
                self.watchers[key] = []

            self.watchers[key].append(callback)

        except Exception as e:
            self.logger.error(f"Error adding setting watcher: {e}")

    def unwatch_setting(self, key: str, callback: Callable[[str, Any, Any], None]):
        """إلغاء مراقبة إعداد"""
        try:
            if key in self.watchers and callback in self.watchers[key]:
                self.watchers[key].remove(callback)

                # إزالة القائمة إذا كانت فارغة
                if not self.watchers[key]:
                    del self.watchers[key]

        except Exception as e:
            self.logger.error(f"Error removing setting watcher: {e}")

    def list_settings(self, category: Optional[str] = None,
                     scope: Optional[SettingScope] = None,
                     search: Optional[str] = None) -> List[Dict[str, Any]]:
        """عرض قائمة الإعدادات مع فلترة"""
        try:
            settings_list = []

            for key, definition in self.definitions.items():
                # تطبيق الفلاتر
                if category and definition.category != category:
                    continue

                if scope and definition.scope != scope:
                    continue

                if search and search.lower() not in key.lower() and search.lower() not in definition.name.lower():
                    continue

                # الحصول على معلومات الإعداد
                setting_info = self.get_setting_info(key)
                if setting_info:
                    settings_list.append(setting_info)

            # ترتيب حسب الفئة ثم الاسم
            settings_list.sort(key=lambda x: (x["category"], x["name"]))

            return settings_list

        except Exception as e:
            self.logger.error(f"Error listing settings: {e}")
            return []

    def get_categories(self) -> List[str]:
        """الحصول على قائمة الفئات"""
        try:
            categories = set()
            for definition in self.definitions.values():
                categories.add(definition.category)

            return sorted(list(categories))

        except Exception as e:
            self.logger.error(f"Error getting categories: {e}")
            return []

    def reset_setting(self, key: str, user: str = "system") -> bool:
        """إعادة تعيين إعداد للقيمة الافتراضية"""
        try:
            if key not in self.definitions:
                return False

            definition = self.definitions[key]
            return self.set_setting(key, definition.default_value, user)

        except Exception as e:
            self.logger.error(f"Error resetting setting {key}: {e}")
            return False

    def reset_category(self, category: str, user: str = "system") -> int:
        """إعادة تعيين جميع إعدادات فئة معينة"""
        try:
            reset_count = 0

            for key, definition in self.definitions.items():
                if definition.category == category:
                    if self.reset_setting(key, user):
                        reset_count += 1

            return reset_count

        except Exception as e:
            self.logger.error(f"Error resetting category {category}: {e}")
            return 0

    def export_settings(self, export_path: Path, include_encrypted: bool = False) -> bool:
        """تصدير الإعدادات"""
        try:
            export_data = {
                "definitions": {},
                "settings": {},
                "metadata": {
                    "export_timestamp": datetime.now().isoformat(),
                    "app_version": self.get_setting("app.version", "1.0.0"),
                    "include_encrypted": include_encrypted
                }
            }

            # تصدير التعريفات
            for key, definition in self.definitions.items():
                export_data["definitions"][key] = asdict(definition)

            # تصدير الإعدادات
            for key, setting in self.settings.items():
                # تخطي الإعدادات المشفرة إذا لم يُطلب تضمينها
                if setting.encrypted and not include_encrypted:
                    continue

                setting_dict = asdict(setting)
                # إزالة القيمة المشفرة للأمان
                if setting.encrypted and not include_encrypted:
                    setting_dict["value"] = "[ENCRYPTED]"

                export_data["settings"][key] = setting_dict

            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)

            return True

        except Exception as e:
            self.logger.error(f"Error exporting settings: {e}")
            return False

    def import_settings(self, import_path: Path, merge: bool = True) -> bool:
        """استيراد الإعدادات"""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)

            # استيراد التعريفات
            if "definitions" in import_data:
                for key, def_data in import_data["definitions"].items():
                    if not merge and key in self.definitions:
                        continue

                    # تحويل enums
                    def_data["setting_type"] = SettingType(def_data["setting_type"])
                    def_data["scope"] = SettingScope(def_data["scope"])

                    definition = SettingDefinition(**def_data)
                    self.definitions[key] = definition

            # استيراد الإعدادات
            if "settings" in import_data:
                for key, setting_data in import_data["settings"].items():
                    if not merge and key in self.settings:
                        continue

                    # تخطي الإعدادات المشفرة المحمية
                    if setting_data.get("value") == "[ENCRYPTED]":
                        continue

                    # تحويل التاريخ والنطاق
                    setting_data["last_modified"] = datetime.fromisoformat(setting_data["last_modified"])
                    setting_data["scope"] = SettingScope(setting_data["scope"])

                    setting = SettingValue(**setting_data)
                    self.settings[key] = setting

            # حفظ البيانات المستوردة
            self._save_definitions()
            if self.auto_save:
                self._save_settings()

            return True

        except Exception as e:
            self.logger.error(f"Error importing settings: {e}")
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """الحصول على إحصائيات الإعدادات"""
        try:
            stats = {
                "total_settings": len(self.settings),
                "total_definitions": len(self.definitions),
                "by_category": {},
                "by_scope": {},
                "by_type": {},
                "encrypted_count": 0,
                "modified_today": 0,
                "watchers_count": len(self.watchers)
            }

            today = datetime.now().date()

            for definition in self.definitions.values():
                # إحصائيات الفئات
                category = definition.category
                stats["by_category"][category] = stats["by_category"].get(category, 0) + 1

                # إحصائيات النطاقات
                scope = definition.scope.value
                stats["by_scope"][scope] = stats["by_scope"].get(scope, 0) + 1

                # إحصائيات الأنواع
                setting_type = definition.setting_type.value
                stats["by_type"][setting_type] = stats["by_type"].get(setting_type, 0) + 1

            for setting in self.settings.values():
                # عدد الإعدادات المشفرة
                if setting.encrypted:
                    stats["encrypted_count"] += 1

                # الإعدادات المعدلة اليوم
                if setting.last_modified.date() == today:
                    stats["modified_today"] += 1

            return stats

        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
            return {}

    def validate_all_settings(self) -> Dict[str, List[str]]:
        """التحقق من صحة جميع الإعدادات"""
        try:
            validation_results = {
                "valid": [],
                "invalid": [],
                "missing_required": [],
                "warnings": []
            }

            # فحص الإعدادات المطلوبة
            for key, definition in self.definitions.items():
                if definition.required and key not in self.settings:
                    validation_results["missing_required"].append(key)
                    continue

                if key in self.settings:
                    setting = self.settings[key]
                    if self._validate_value(key, setting.value):
                        validation_results["valid"].append(key)
                    else:
                        validation_results["invalid"].append(key)
                else:
                    # استخدام القيمة الافتراضية
                    if self._validate_value(key, definition.default_value):
                        validation_results["valid"].append(key)
                    else:
                        validation_results["warnings"].append(f"Default value for {key} is invalid")

            return validation_results

        except Exception as e:
            self.logger.error(f"Error validating settings: {e}")
            return {"valid": [], "invalid": [], "missing_required": [], "warnings": []}

    def create_setting_definition(self, definition: SettingDefinition) -> bool:
        """إنشاء تعريف إعداد جديد"""
        try:
            if definition.key in self.definitions:
                self.logger.warning(f"Setting definition already exists: {definition.key}")
                return False

            self.definitions[definition.key] = definition

            # إضافة القيمة الافتراضية
            if definition.key not in self.settings:
                self.set_setting(definition.key, definition.default_value, save=False)

            # حفظ التعريفات
            self._save_definitions()

            return True

        except Exception as e:
            self.logger.error(f"Error creating setting definition: {e}")
            return False

    def update_setting_definition(self, key: str, **updates) -> bool:
        """تحديث تعريف إعداد"""
        try:
            if key not in self.definitions:
                return False

            definition = self.definitions[key]

            # تطبيق التحديثات
            for field, value in updates.items():
                if hasattr(definition, field):
                    setattr(definition, field, value)

            # حفظ التعريفات
            self._save_definitions()

            return True

        except Exception as e:
            self.logger.error(f"Error updating setting definition: {e}")
            return False

    def delete_setting(self, key: str) -> bool:
        """حذف إعداد"""
        try:
            # حذف الإعداد
            if key in self.settings:
                del self.settings[key]

            # حذف التعريف
            if key in self.definitions:
                del self.definitions[key]

            # حذف المراقبين
            if key in self.watchers:
                del self.watchers[key]

            # حفظ التغييرات
            self._save_definitions()
            if self.auto_save:
                self._save_settings()

            return True

        except Exception as e:
            self.logger.error(f"Error deleting setting: {e}")
            return False

    def backup_settings(self, backup_name: Optional[str] = None) -> Path:
        """إنشاء نسخة احتياطية مسماة"""
        try:
            if not backup_name:
                backup_name = f"manual_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            backup_file = self.backup_dir / f"{backup_name}.json"

            if self.export_settings(backup_file, include_encrypted=True):
                return backup_file
            else:
                raise Exception("Failed to export settings")

        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            return None

    def restore_settings(self, backup_path: Path) -> bool:
        """استعادة الإعدادات من نسخة احتياطية"""
        try:
            # إنشاء نسخة احتياطية من الحالة الحالية
            current_backup = self.backup_settings("pre_restore")

            # استيراد الإعدادات
            if self.import_settings(backup_path, merge=False):
                self.logger.info(f"Settings restored from {backup_path}")
                return True
            else:
                # استعادة النسخة الاحتياطية في حالة الفشل
                if current_backup:
                    self.import_settings(current_backup, merge=False)
                return False

        except Exception as e:
            self.logger.error(f"Error restoring settings: {e}")
            return False

    def list_backups(self) -> List[Dict[str, Any]]:
        """عرض قائمة النسخ الاحتياطية"""
        try:
            backups = []

            for backup_file in self.backup_dir.glob("*.json"):
                try:
                    stat = backup_file.stat()
                    # استخدام st_birthtime إذا كان متوفراً، وإلا st_mtime
                    created_time = getattr(stat, 'st_birthtime', stat.st_mtime)
                    backups.append({
                        "name": backup_file.stem,
                        "path": str(backup_file),
                        "size": stat.st_size,
                        "created": datetime.fromtimestamp(created_time),
                        "modified": datetime.fromtimestamp(stat.st_mtime)
                    })
                except Exception:
                    continue

            # ترتيب حسب تاريخ الإنشاء
            backups.sort(key=lambda x: x["created"], reverse=True)

            return backups

        except Exception as e:
            self.logger.error(f"Error listing backups: {e}")
            return []

    def cleanup_settings(self) -> Dict[str, int]:
        """تنظيف الإعدادات"""
        try:
            cleanup_stats = {
                "removed_orphaned": 0,
                "removed_invalid": 0,
                "reset_corrupted": 0
            }

            # إزالة الإعدادات اليتيمة (بدون تعريف)
            orphaned_keys = []
            for key in self.settings.keys():
                if key not in self.definitions:
                    orphaned_keys.append(key)

            for key in orphaned_keys:
                del self.settings[key]
                cleanup_stats["removed_orphaned"] += 1

            # فحص وإصلاح الإعدادات غير الصحيحة
            for key, setting in list(self.settings.items()):
                if not self._validate_value(key, setting.value):
                    # محاولة إعادة تعيين القيمة الافتراضية
                    if key in self.definitions:
                        default_value = self.definitions[key].default_value
                        if self._validate_value(key, default_value):
                            setting.value = default_value
                            setting.last_modified = datetime.now()
                            setting.modified_by = "system_cleanup"
                            cleanup_stats["reset_corrupted"] += 1
                        else:
                            del self.settings[key]
                            cleanup_stats["removed_invalid"] += 1

            # حفظ التغييرات
            if self.auto_save:
                self._save_settings()

            return cleanup_stats

        except Exception as e:
            self.logger.error(f"Error cleaning up settings: {e}")
            return {"removed_orphaned": 0, "removed_invalid": 0, "reset_corrupted": 0}

    def get_setting_history(self, key: str) -> List[Dict[str, Any]]:
        """الحصول على تاريخ تغييرات إعداد (محاكاة)"""
        try:
            # في التطبيق الحقيقي، يمكن حفظ تاريخ التغييرات
            if key in self.settings:
                setting = self.settings[key]
                return [{
                    "version": setting.version,
                    "value": setting.value,
                    "modified_by": setting.modified_by,
                    "modified_at": setting.last_modified.isoformat(),
                    "encrypted": setting.encrypted
                }]

            return []

        except Exception as e:
            self.logger.error(f"Error getting setting history: {e}")
            return []

    def shutdown(self):
        """إغلاق مدير الإعدادات"""
        try:
            # حفظ نهائي للإعدادات
            self._save_settings()

            # مسح المراقبين
            self.watchers.clear()

            self.logger.info("Settings manager shutdown completed")

        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        # تجاهل معاملات الاستثناء - نحن نقوم بالتنظيف فقط
        _ = exc_type, exc_val, exc_tb
        self.shutdown()
        return False
