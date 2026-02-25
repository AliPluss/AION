"""
AION Advanced Configuration Manager
مدير الإعدادات المتقدم مع التشفير والنسخ الاحتياطي
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
import shutil

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

@dataclass
class ConfigProfile:
    """ملف تعريف الإعدادات"""
    name: str
    description: str
    created_date: datetime
    last_modified: datetime
    is_encrypted: bool = False
    is_default: bool = False
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class AdvancedConfigManager:
    """مدير الإعدادات المتقدم"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.cwd() / "config"
        self.config_dir.mkdir(exist_ok=True)
        
        # مجلدات فرعية
        self.profiles_dir = self.config_dir / "profiles"
        self.backups_dir = self.config_dir / "backups"
        self.templates_dir = self.config_dir / "templates"
        
        for dir_path in [self.profiles_dir, self.backups_dir, self.templates_dir]:
            dir_path.mkdir(exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
        
        # ملف الإعدادات الرئيسي
        self.main_config_file = self.config_dir / "aion_config.json"
        self.profiles_file = self.config_dir / "profiles.json"
        
        # إعدادات التشفير
        self.encryption_key_file = self.config_dir / ".encryption_key"
        self.encryption_key = self._load_or_create_encryption_key()
        
        # تحميل الإعدادات والملفات الشخصية
        self.config_data = self._load_main_config()
        self.profiles = self._load_profiles()
        
        # الملف الشخصي الحالي
        self.current_profile = self.config_data.get("current_profile", "default")
        
        # إعدادات النسخ الاحتياطي
        self.backup_settings = {
            "auto_backup": True,
            "max_backups": 10,
            "backup_on_change": True
        }
    
    def _load_or_create_encryption_key(self) -> Optional[bytes]:
        """تحميل أو إنشاء مفتاح التشفير"""
        if not CRYPTO_AVAILABLE:
            return None
        
        try:
            if self.encryption_key_file.exists():
                with open(self.encryption_key_file, 'rb') as f:
                    return f.read()
            else:
                # إنشاء مفتاح جديد
                key = Fernet.generate_key()
                with open(self.encryption_key_file, 'wb') as f:
                    f.write(key)
                
                # إخفاء الملف (Windows)
                if os.name == 'nt':
                    os.system(f'attrib +h "{self.encryption_key_file}"')
                
                return key
        except Exception as e:
            self.logger.error(f"Error handling encryption key: {e}")
            return None
    
    def _load_main_config(self) -> Dict[str, Any]:
        """تحميل الإعدادات الرئيسية"""
        try:
            if self.main_config_file.exists():
                with open(self.main_config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            
            # إعدادات افتراضية
            default_config = {
                "version": "1.0.0",
                "current_profile": "default",
                "auto_save": True,
                "backup_enabled": True,
                "encryption_enabled": CRYPTO_AVAILABLE,
                "created_date": datetime.now().isoformat(),
                "last_modified": datetime.now().isoformat()
            }
            
            self._save_main_config(default_config)
            return default_config
            
        except Exception as e:
            self.logger.error(f"Error loading main config: {e}")
            return {}
    
    def _save_main_config(self, config_data: Dict[str, Any]):
        """حفظ الإعدادات الرئيسية"""
        try:
            config_data["last_modified"] = datetime.now().isoformat()
            
            with open(self.main_config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False, default=str)
                
        except Exception as e:
            self.logger.error(f"Error saving main config: {e}")
    
    def _load_profiles(self) -> Dict[str, ConfigProfile]:
        """تحميل الملفات الشخصية"""
        try:
            if self.profiles_file.exists():
                with open(self.profiles_file, 'r', encoding='utf-8') as f:
                    profiles_data = json.load(f)
                
                profiles = {}
                for name, data in profiles_data.items():
                    data["created_date"] = datetime.fromisoformat(data["created_date"])
                    data["last_modified"] = datetime.fromisoformat(data["last_modified"])
                    profiles[name] = ConfigProfile(**data)
                
                return profiles
            
            # إنشاء ملف شخصي افتراضي
            default_profile = ConfigProfile(
                name="default",
                description="Default configuration profile",
                created_date=datetime.now(),
                last_modified=datetime.now(),
                is_default=True
            )
            
            profiles = {"default": default_profile}
            self._save_profiles(profiles)
            return profiles
            
        except Exception as e:
            self.logger.error(f"Error loading profiles: {e}")
            return {}
    
    def _save_profiles(self, profiles: Dict[str, ConfigProfile]):
        """حفظ الملفات الشخصية"""
        try:
            profiles_data = {}
            for name, profile in profiles.items():
                profiles_data[name] = asdict(profile)
            
            with open(self.profiles_file, 'w', encoding='utf-8') as f:
                json.dump(profiles_data, f, indent=2, ensure_ascii=False, default=str)
                
        except Exception as e:
            self.logger.error(f"Error saving profiles: {e}")
    
    def create_profile(self, name: str, description: str = "", 
                      copy_from: Optional[str] = None, encrypt: bool = False) -> bool:
        """إنشاء ملف شخصي جديد"""
        try:
            if name in self.profiles:
                self.logger.error(f"Profile '{name}' already exists")
                return False
            
            # إنشاء الملف الشخصي
            profile = ConfigProfile(
                name=name,
                description=description,
                created_date=datetime.now(),
                last_modified=datetime.now(),
                is_encrypted=encrypt and CRYPTO_AVAILABLE
            )
            
            # إنشاء ملف الإعدادات للملف الشخصي
            if copy_from and copy_from in self.profiles:
                # نسخ من ملف شخصي موجود
                source_file = self.profiles_dir / f"{copy_from}.json"
                if source_file.exists():
                    config_data = self._load_profile_config(copy_from)
                    if config_data:
                        self._save_profile_config(name, config_data, encrypt)
            else:
                # إنشاء إعدادات افتراضية
                default_config = {
                    "profile_name": name,
                    "created_date": datetime.now().isoformat(),
                    "settings": {}
                }
                self._save_profile_config(name, default_config, encrypt)
            
            # إضافة الملف الشخصي
            self.profiles[name] = profile
            self._save_profiles(self.profiles)
            
            self.logger.info(f"Profile '{name}' created successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating profile '{name}': {e}")
            return False
    
    def delete_profile(self, name: str) -> bool:
        """حذف ملف شخصي"""
        try:
            if name not in self.profiles:
                self.logger.error(f"Profile '{name}' not found")
                return False
            
            if self.profiles[name].is_default:
                self.logger.error(f"Cannot delete default profile '{name}'")
                return False
            
            # حذف ملف الإعدادات
            profile_config_file = self.profiles_dir / f"{name}.json"
            if profile_config_file.exists():
                profile_config_file.unlink()
            
            # حذف الملف الشخصي
            del self.profiles[name]
            self._save_profiles(self.profiles)
            
            # تغيير الملف الشخصي الحالي إذا كان المحذوف
            if self.current_profile == name:
                self.current_profile = "default"
                self.config_data["current_profile"] = "default"
                self._save_main_config(self.config_data)
            
            self.logger.info(f"Profile '{name}' deleted successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting profile '{name}': {e}")
            return False
    
    def switch_profile(self, name: str) -> bool:
        """تبديل الملف الشخصي"""
        try:
            if name not in self.profiles:
                self.logger.error(f"Profile '{name}' not found")
                return False
            
            self.current_profile = name
            self.config_data["current_profile"] = name
            self._save_main_config(self.config_data)
            
            self.logger.info(f"Switched to profile '{name}'")
            return True
            
        except Exception as e:
            self.logger.error(f"Error switching to profile '{name}': {e}")
            return False
    
    def _load_profile_config(self, profile_name: str) -> Optional[Dict[str, Any]]:
        """تحميل إعدادات ملف شخصي"""
        try:
            profile_config_file = self.profiles_dir / f"{profile_name}.json"
            
            if not profile_config_file.exists():
                return None
            
            profile = self.profiles.get(profile_name)
            if not profile:
                return None
            
            with open(profile_config_file, 'r', encoding='utf-8') as f:
                data = f.read()
            
            # فك التشفير إذا لزم الأمر
            if profile.is_encrypted and self.encryption_key:
                try:
                    fernet = Fernet(self.encryption_key)
                    data = fernet.decrypt(data.encode()).decode('utf-8')
                except Exception as e:
                    self.logger.error(f"Error decrypting profile '{profile_name}': {e}")
                    return None
            
            return json.loads(data)
            
        except Exception as e:
            self.logger.error(f"Error loading profile config '{profile_name}': {e}")
            return None
    
    def _save_profile_config(self, profile_name: str, config_data: Dict[str, Any], encrypt: bool = False):
        """حفظ إعدادات ملف شخصي"""
        try:
            profile_config_file = self.profiles_dir / f"{profile_name}.json"
            
            # تحديث تاريخ التعديل
            config_data["last_modified"] = datetime.now().isoformat()
            
            data = json.dumps(config_data, indent=2, ensure_ascii=False, default=str)
            
            # التشفير إذا لزم الأمر
            if encrypt and self.encryption_key:
                try:
                    fernet = Fernet(self.encryption_key)
                    data = fernet.encrypt(data.encode()).decode('utf-8')
                except Exception as e:
                    self.logger.error(f"Error encrypting profile '{profile_name}': {e}")
                    return
            
            with open(profile_config_file, 'w', encoding='utf-8') as f:
                f.write(data)
            
            # النسخ الاحتياطي التلقائي
            if self.backup_settings["backup_on_change"]:
                self._create_backup(profile_name)
                
        except Exception as e:
            self.logger.error(f"Error saving profile config '{profile_name}': {e}")
    
    def get_setting(self, key: str, default: Any = None, profile: Optional[str] = None) -> Any:
        """الحصول على إعداد"""
        try:
            profile_name = profile or self.current_profile
            config_data = self._load_profile_config(profile_name)
            
            if not config_data:
                return default
            
            # البحث في الإعدادات باستخدام النقاط للمسارات المتداخلة
            keys = key.split('.')
            value = config_data.get("settings", {})
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            
            return value
            
        except Exception as e:
            self.logger.error(f"Error getting setting '{key}': {e}")
            return default
    
    def set_setting(self, key: str, value: Any, profile: Optional[str] = None) -> bool:
        """تحديد إعداد"""
        try:
            profile_name = profile or self.current_profile
            config_data = self._load_profile_config(profile_name) or {"settings": {}}
            
            # تحديد القيمة باستخدام النقاط للمسارات المتداخلة
            keys = key.split('.')
            current = config_data.setdefault("settings", {})
            
            for k in keys[:-1]:
                current = current.setdefault(k, {})
            
            current[keys[-1]] = value
            
            # حفظ الإعدادات
            profile_obj = self.profiles.get(profile_name)
            encrypt = profile_obj.is_encrypted if profile_obj else False
            
            self._save_profile_config(profile_name, config_data, encrypt)
            
            # تحديث تاريخ التعديل للملف الشخصي
            if profile_obj:
                profile_obj.last_modified = datetime.now()
                self._save_profiles(self.profiles)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting '{key}': {e}")
            return False
    
    def remove_setting(self, key: str, profile: Optional[str] = None) -> bool:
        """إزالة إعداد"""
        try:
            profile_name = profile or self.current_profile
            config_data = self._load_profile_config(profile_name)
            
            if not config_data:
                return False
            
            # إزالة القيمة باستخدام النقاط للمسارات المتداخلة
            keys = key.split('.')
            current = config_data.get("settings", {})
            
            # الوصول إلى المستوى الأخير
            for k in keys[:-1]:
                if isinstance(current, dict) and k in current:
                    current = current[k]
                else:
                    return False  # المسار غير موجود
            
            # إزالة المفتاح الأخير
            if isinstance(current, dict) and keys[-1] in current:
                del current[keys[-1]]
                
                # حفظ الإعدادات
                profile_obj = self.profiles.get(profile_name)
                encrypt = profile_obj.is_encrypted if profile_obj else False
                
                self._save_profile_config(profile_name, config_data, encrypt)
                return True
            
            return False

        except Exception as e:
            self.logger.error(f"Error removing setting '{key}': {e}")
            return False

    def _create_backup(self, profile_name: str):
        """إنشاء نسخة احتياطية"""
        try:
            if not self.backup_settings["auto_backup"]:
                return

            profile_config_file = self.profiles_dir / f"{profile_name}.json"
            if not profile_config_file.exists():
                return

            # إنشاء اسم النسخة الاحتياطية
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{profile_name}_{timestamp}.json"
            backup_file = self.backups_dir / backup_name

            # نسخ الملف
            shutil.copy2(profile_config_file, backup_file)

            # تنظيف النسخ الاحتياطية القديمة
            self._cleanup_old_backups(profile_name)

        except Exception as e:
            self.logger.error(f"Error creating backup for '{profile_name}': {e}")

    def _cleanup_old_backups(self, profile_name: str):
        """تنظيف النسخ الاحتياطية القديمة"""
        try:
            max_backups = self.backup_settings["max_backups"]

            # البحث عن النسخ الاحتياطية للملف الشخصي
            backup_pattern = f"{profile_name}_*.json"
            backup_files = list(self.backups_dir.glob(backup_pattern))

            # ترتيب حسب تاريخ الإنشاء
            backup_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

            # حذف النسخ الزائدة
            for backup_file in backup_files[max_backups:]:
                backup_file.unlink()

        except Exception as e:
            self.logger.error(f"Error cleaning up backups for '{profile_name}': {e}")

    def restore_backup(self, profile_name: str, backup_timestamp: str) -> bool:
        """استعادة نسخة احتياطية"""
        try:
            backup_name = f"{profile_name}_{backup_timestamp}.json"
            backup_file = self.backups_dir / backup_name

            if not backup_file.exists():
                self.logger.error(f"Backup file not found: {backup_name}")
                return False

            profile_config_file = self.profiles_dir / f"{profile_name}.json"

            # إنشاء نسخة احتياطية من الحالة الحالية قبل الاستعادة
            if profile_config_file.exists():
                current_backup_name = f"{profile_name}_before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                current_backup_file = self.backups_dir / current_backup_name
                shutil.copy2(profile_config_file, current_backup_file)

            # استعادة النسخة الاحتياطية
            shutil.copy2(backup_file, profile_config_file)

            # تحديث تاريخ التعديل للملف الشخصي
            if profile_name in self.profiles:
                self.profiles[profile_name].last_modified = datetime.now()
                self._save_profiles(self.profiles)

            self.logger.info(f"Backup restored for profile '{profile_name}' from {backup_timestamp}")
            return True

        except Exception as e:
            self.logger.error(f"Error restoring backup for '{profile_name}': {e}")
            return False

    def list_backups(self, profile_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """عرض قائمة النسخ الاحتياطية"""
        try:
            backups = []

            if profile_name:
                backup_pattern = f"{profile_name}_*.json"
            else:
                backup_pattern = "*.json"

            backup_files = list(self.backups_dir.glob(backup_pattern))

            for backup_file in backup_files:
                # استخراج معلومات النسخة الاحتياطية من اسم الملف
                name_parts = backup_file.stem.split('_')
                if len(name_parts) >= 3:
                    profile = '_'.join(name_parts[:-2])
                    timestamp = '_'.join(name_parts[-2:])

                    backups.append({
                        "profile": profile,
                        "timestamp": timestamp,
                        "file_name": backup_file.name,
                        "size": backup_file.stat().st_size,
                        "created_date": datetime.fromtimestamp(backup_file.stat().st_mtime)
                    })

            # ترتيب حسب التاريخ
            backups.sort(key=lambda b: b["created_date"], reverse=True)

            return backups

        except Exception as e:
            self.logger.error(f"Error listing backups: {e}")
            return []

    def export_profile(self, profile_name: str, export_path: Path, include_encrypted: bool = False) -> bool:
        """تصدير ملف شخصي"""
        try:
            if profile_name not in self.profiles:
                self.logger.error(f"Profile '{profile_name}' not found")
                return False

            profile = self.profiles[profile_name]
            config_data = self._load_profile_config(profile_name)

            if not config_data:
                self.logger.error(f"Could not load config for profile '{profile_name}'")
                return False

            # إعداد بيانات التصدير
            export_data = {
                "profile_info": asdict(profile),
                "config_data": config_data,
                "export_date": datetime.now().isoformat(),
                "aion_version": self.config_data.get("version", "1.0.0")
            }

            # إزالة معلومات التشفير إذا لم يُطلب تضمينها
            if not include_encrypted and profile.is_encrypted:
                export_data["profile_info"]["is_encrypted"] = False
                export_data["note"] = "Encryption information removed for security"

            # حفظ ملف التصدير
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)

            self.logger.info(f"Profile '{profile_name}' exported to {export_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error exporting profile '{profile_name}': {e}")
            return False

    def import_profile(self, import_path: Path, new_name: Optional[str] = None,
                      overwrite: bool = False) -> bool:
        """استيراد ملف شخصي"""
        try:
            if not import_path.exists():
                self.logger.error(f"Import file not found: {import_path}")
                return False

            # تحميل بيانات التصدير
            with open(import_path, 'r', encoding='utf-8') as f:
                export_data = json.load(f)

            profile_info = export_data.get("profile_info", {})
            config_data = export_data.get("config_data", {})

            # تحديد اسم الملف الشخصي
            profile_name = new_name or profile_info.get("name", "imported_profile")

            # فحص الوجود
            if profile_name in self.profiles and not overwrite:
                self.logger.error(f"Profile '{profile_name}' already exists. Use overwrite=True to replace.")
                return False

            # إنشاء الملف الشخصي
            profile_info["name"] = profile_name
            profile_info["created_date"] = datetime.fromisoformat(profile_info["created_date"])
            profile_info["last_modified"] = datetime.now()

            profile = ConfigProfile(**profile_info)

            # حفظ الإعدادات
            self._save_profile_config(profile_name, config_data, profile.is_encrypted)

            # إضافة الملف الشخصي
            self.profiles[profile_name] = profile
            self._save_profiles(self.profiles)

            self.logger.info(f"Profile '{profile_name}' imported successfully")
            return True

        except Exception as e:
            self.logger.error(f"Error importing profile from {import_path}: {e}")
            return False

    def get_profile_info(self, profile_name: str) -> Optional[Dict[str, Any]]:
        """الحصول على معلومات ملف شخصي"""
        if profile_name not in self.profiles:
            return None

        profile = self.profiles[profile_name]
        config_data = self._load_profile_config(profile_name)

        return {
            "profile": asdict(profile),
            "settings_count": len(config_data.get("settings", {})) if config_data else 0,
            "config_size": len(json.dumps(config_data, default=str)) if config_data else 0,
            "backups_count": len([b for b in self.list_backups() if b["profile"] == profile_name])
        }

    def list_profiles(self) -> List[Dict[str, Any]]:
        """عرض قائمة الملفات الشخصية"""
        profiles_list = []

        for name in self.profiles.keys():
            info = self.get_profile_info(name)
            if info:
                info["is_current"] = (name == self.current_profile)
                profiles_list.append(info)

        return profiles_list

    def validate_config(self, profile_name: Optional[str] = None) -> Dict[str, Any]:
        """التحقق من صحة الإعدادات"""
        profile_name = profile_name or self.current_profile

        validation_result = {
            "profile": profile_name,
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "suggestions": []
        }

        try:
            # فحص وجود الملف الشخصي
            if profile_name not in self.profiles:
                validation_result["is_valid"] = False
                validation_result["errors"].append(f"Profile '{profile_name}' not found")
                return validation_result

            # فحص ملف الإعدادات
            config_data = self._load_profile_config(profile_name)
            if not config_data:
                validation_result["is_valid"] = False
                validation_result["errors"].append(f"Could not load config for profile '{profile_name}'")
                return validation_result

            # فحص البنية الأساسية
            required_fields = ["profile_name", "created_date"]
            for field in required_fields:
                if field not in config_data:
                    validation_result["warnings"].append(f"Missing field: {field}")

            # فحص الإعدادات
            settings = config_data.get("settings", {})
            if not settings:
                validation_result["warnings"].append("No settings found in profile")

            # اقتراحات التحسين
            if len(settings) > 100:
                validation_result["suggestions"].append("Consider organizing settings into categories")

            profile = self.profiles[profile_name]
            if not profile.description:
                validation_result["suggestions"].append("Add a description to the profile")

        except Exception as e:
            validation_result["is_valid"] = False
            validation_result["errors"].append(f"Validation error: {e}")

        return validation_result

    def get_config_statistics(self) -> Dict[str, Any]:
        """إحصائيات الإعدادات"""
        try:
            stats = {
                "total_profiles": len(self.profiles),
                "current_profile": self.current_profile,
                "encrypted_profiles": sum(1 for p in self.profiles.values() if p.is_encrypted),
                "total_backups": len(self.list_backups()),
                "config_directory_size": 0,
                "profiles_by_type": {},
                "last_activity": None
            }

            # حساب حجم مجلد الإعدادات
            for file_path in self.config_dir.rglob('*'):
                if file_path.is_file():
                    stats["config_directory_size"] += file_path.stat().st_size

            # آخر نشاط
            latest_modification = None
            for profile in self.profiles.values():
                if latest_modification is None or profile.last_modified > latest_modification:
                    latest_modification = profile.last_modified

            if latest_modification:
                stats["last_activity"] = latest_modification.isoformat()

            return stats

        except Exception as e:
            self.logger.error(f"Error calculating config statistics: {e}")
            return {}
