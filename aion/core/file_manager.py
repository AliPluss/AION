"""
📁 AION Advanced File Manager
Professional file management system with advanced operations
Features: File operations, search, compression, encryption, monitoring
"""

import os
import sys
import shutil
import hashlib
import zipfile
import tarfile
import tempfile
import mimetypes
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json
import re
import stat

# Optional imports with fallbacks
try:
    import watchdog
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False

try:
    from cryptography.fernet import Fernet
    ENCRYPTION_AVAILABLE = True
except ImportError:
    ENCRYPTION_AVAILABLE = False

class FileOperation(Enum):
    """File operations"""
    CREATE = "create"
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    COPY = "copy"
    MOVE = "move"
    RENAME = "rename"
    COMPRESS = "compress"
    EXTRACT = "extract"
    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"

class FileType(Enum):
    """File types"""
    TEXT = "text"
    BINARY = "binary"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    ARCHIVE = "archive"
    CODE = "code"
    DATA = "data"
    UNKNOWN = "unknown"

class SortBy(Enum):
    """Sort options"""
    NAME = "name"
    SIZE = "size"
    DATE_MODIFIED = "date_modified"
    DATE_CREATED = "date_created"
    TYPE = "type"
    EXTENSION = "extension"

@dataclass
class FileInfo:
    """File information structure"""
    path: Path
    name: str
    size: int
    file_type: FileType
    mime_type: str
    extension: str
    created_at: datetime
    modified_at: datetime
    accessed_at: datetime
    permissions: str
    is_directory: bool
    is_hidden: bool
    checksum: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class FileOperation:
    """File operation record"""
    operation_id: str
    operation_type: FileOperation
    source_path: str
    target_path: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = False
    error_message: str = ""
    file_size: int = 0
    duration: float = 0.0

class FileSystemWatcher(FileSystemEventHandler):
    """File system event handler"""
    
    def __init__(self, file_manager):
        self.file_manager = file_manager
        super().__init__()
    
    def on_created(self, event):
        if not event.is_directory:
            self.file_manager._log_file_event("created", event.src_path)
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.file_manager._log_file_event("deleted", event.src_path)
    
    def on_modified(self, event):
        if not event.is_directory:
            self.file_manager._log_file_event("modified", event.src_path)
    
    def on_moved(self, event):
        if not event.is_directory:
            self.file_manager._log_file_event("moved", event.src_path, event.dest_path)

class AdvancedFileManager:
    """
    🚀 Advanced File Manager System
    
    Professional file management with:
    - Complete file operations (CRUD, copy, move, rename)
    - Advanced search and filtering
    - File compression and extraction
    - File encryption and decryption
    - File system monitoring
    - Batch operations
    - File metadata analysis
    - Integration with AION systems
    """
    
    def __init__(self):
        # Storage
        self.manager_dir = Path.home() / ".aion" / "file_manager"
        self.manager_dir.mkdir(parents=True, exist_ok=True)
        
        self.temp_dir = self.manager_dir / "temp"
        self.temp_dir.mkdir(exist_ok=True)
        
        self.logs_dir = self.manager_dir / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        
        # Runtime data
        self.current_directory = Path.cwd()
        self.operation_history: List[FileOperation] = []
        self.watched_directories: Dict[str, Observer] = {}
        self.file_cache: Dict[str, FileInfo] = {}
        
        # Encryption key
        self.encryption_key = None
        if ENCRYPTION_AVAILABLE:
            self._initialize_encryption()
        
        # File type mappings
        self.file_type_mappings = self._load_file_type_mappings()
        
        # Statistics
        self.total_operations = 0
        self.successful_operations = 0
        self.failed_operations = 0
        
        print("📁 Advanced File Manager initialized")
        print(f"   Manager directory: {self.manager_dir}")
        print(f"   Current directory: {self.current_directory}")
        print(f"   File monitoring: {WATCHDOG_AVAILABLE}")
        print(f"   File encryption: {ENCRYPTION_AVAILABLE}")
    
    def _initialize_encryption(self):
        """Initialize encryption system"""
        key_file = self.manager_dir / "encryption.key"
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                self.encryption_key = f.read()
        else:
            self.encryption_key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(self.encryption_key)
            
            # Secure the key file
            os.chmod(key_file, stat.S_IRUSR | stat.S_IWUSR)
    
    def _load_file_type_mappings(self) -> Dict[str, FileType]:
        """Load file type mappings"""
        return {
            # Text files
            '.txt': FileType.TEXT,
            '.md': FileType.TEXT,
            '.rst': FileType.TEXT,
            '.log': FileType.TEXT,
            
            # Code files
            '.py': FileType.CODE,
            '.js': FileType.CODE,
            '.ts': FileType.CODE,
            '.html': FileType.CODE,
            '.css': FileType.CODE,
            '.cpp': FileType.CODE,
            '.c': FileType.CODE,
            '.rs': FileType.CODE,
            '.go': FileType.CODE,
            '.java': FileType.CODE,
            '.php': FileType.CODE,
            '.rb': FileType.CODE,
            
            # Images
            '.jpg': FileType.IMAGE,
            '.jpeg': FileType.IMAGE,
            '.png': FileType.IMAGE,
            '.gif': FileType.IMAGE,
            '.bmp': FileType.IMAGE,
            '.svg': FileType.IMAGE,
            '.webp': FileType.IMAGE,
            
            # Videos
            '.mp4': FileType.VIDEO,
            '.avi': FileType.VIDEO,
            '.mkv': FileType.VIDEO,
            '.mov': FileType.VIDEO,
            '.wmv': FileType.VIDEO,
            '.flv': FileType.VIDEO,
            '.webm': FileType.VIDEO,
            
            # Audio
            '.mp3': FileType.AUDIO,
            '.wav': FileType.AUDIO,
            '.flac': FileType.AUDIO,
            '.aac': FileType.AUDIO,
            '.ogg': FileType.AUDIO,
            '.wma': FileType.AUDIO,
            
            # Documents
            '.pdf': FileType.DOCUMENT,
            '.doc': FileType.DOCUMENT,
            '.docx': FileType.DOCUMENT,
            '.xls': FileType.DOCUMENT,
            '.xlsx': FileType.DOCUMENT,
            '.ppt': FileType.DOCUMENT,
            '.pptx': FileType.DOCUMENT,
            '.odt': FileType.DOCUMENT,
            '.ods': FileType.DOCUMENT,
            '.odp': FileType.DOCUMENT,
            
            # Archives
            '.zip': FileType.ARCHIVE,
            '.rar': FileType.ARCHIVE,
            '.7z': FileType.ARCHIVE,
            '.tar': FileType.ARCHIVE,
            '.gz': FileType.ARCHIVE,
            '.bz2': FileType.ARCHIVE,
            '.xz': FileType.ARCHIVE,
            
            # Data
            '.json': FileType.DATA,
            '.xml': FileType.DATA,
            '.yaml': FileType.DATA,
            '.yml': FileType.DATA,
            '.csv': FileType.DATA,
            '.sql': FileType.DATA,
            '.db': FileType.DATA,
            '.sqlite': FileType.DATA
        }
    
    def _get_file_type(self, file_path: Path) -> FileType:
        """Determine file type"""
        extension = file_path.suffix.lower()
        return self.file_type_mappings.get(extension, FileType.UNKNOWN)
    
    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate file checksum"""
        if not file_path.exists() or file_path.is_dir():
            return ""
        
        try:
            hash_md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception:
            return ""
    
    def get_file_info(self, file_path: Union[str, Path]) -> Optional[FileInfo]:
        """Get comprehensive file information"""
        path = Path(file_path)
        
        if not path.exists():
            return None
        
        try:
            stat_info = path.stat()
            
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(str(path))
            if mime_type is None:
                mime_type = "application/octet-stream"
            
            # Create file info
            file_info = FileInfo(
                path=path,
                name=path.name,
                size=stat_info.st_size if not path.is_dir() else 0,
                file_type=self._get_file_type(path),
                mime_type=mime_type,
                extension=path.suffix.lower(),
                created_at=datetime.fromtimestamp(stat_info.st_ctime),
                modified_at=datetime.fromtimestamp(stat_info.st_mtime),
                accessed_at=datetime.fromtimestamp(stat_info.st_atime),
                permissions=oct(stat_info.st_mode)[-3:],
                is_directory=path.is_dir(),
                is_hidden=path.name.startswith('.'),
                checksum=self._calculate_checksum(path) if not path.is_dir() else ""
            )
            
            # Cache file info
            self.file_cache[str(path)] = file_info
            
            return file_info
            
        except Exception as e:
            print(f"❌ Error getting file info: {e}")
            return None

    def list_directory(
        self,
        directory: Union[str, Path] = None,
        sort_by: SortBy = SortBy.NAME,
        reverse: bool = False,
        show_hidden: bool = False,
        file_types: List[FileType] = None
    ) -> List[FileInfo]:
        """List directory contents with filtering and sorting"""

        if directory is None:
            directory = self.current_directory
        else:
            directory = Path(directory)

        if not directory.exists() or not directory.is_dir():
            print(f"❌ Directory not found: {directory}")
            return []

        files_info = []

        try:
            for item in directory.iterdir():
                # Skip hidden files if not requested
                if not show_hidden and item.name.startswith('.'):
                    continue

                file_info = self.get_file_info(item)
                if file_info:
                    # Filter by file types if specified
                    if file_types and file_info.file_type not in file_types:
                        continue

                    files_info.append(file_info)

            # Sort files
            if sort_by == SortBy.NAME:
                files_info.sort(key=lambda x: x.name.lower(), reverse=reverse)
            elif sort_by == SortBy.SIZE:
                files_info.sort(key=lambda x: x.size, reverse=reverse)
            elif sort_by == SortBy.DATE_MODIFIED:
                files_info.sort(key=lambda x: x.modified_at, reverse=reverse)
            elif sort_by == SortBy.DATE_CREATED:
                files_info.sort(key=lambda x: x.created_at, reverse=reverse)
            elif sort_by == SortBy.TYPE:
                files_info.sort(key=lambda x: x.file_type.value, reverse=reverse)
            elif sort_by == SortBy.EXTENSION:
                files_info.sort(key=lambda x: x.extension, reverse=reverse)

            return files_info

        except Exception as e:
            print(f"❌ Error listing directory: {e}")
            return []

    def create_file(self, file_path: Union[str, Path], content: str = "") -> bool:
        """Create new file"""
        path = Path(file_path)

        try:
            # Ensure parent directory exists
            path.parent.mkdir(parents=True, exist_ok=True)

            # Create file
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

            self._log_operation(FileOperation.CREATE, str(path), success=True, file_size=len(content))
            print(f"✅ File created: {path}")
            return True

        except Exception as e:
            self._log_operation(FileOperation.CREATE, str(path), success=False, error=str(e))
            print(f"❌ Error creating file: {e}")
            return False

    def create_directory(self, dir_path: Union[str, Path]) -> bool:
        """Create new directory"""
        path = Path(dir_path)

        try:
            path.mkdir(parents=True, exist_ok=True)

            self._log_operation(FileOperation.CREATE, str(path), success=True)
            print(f"✅ Directory created: {path}")
            return True

        except Exception as e:
            self._log_operation(FileOperation.CREATE, str(path), success=False, error=str(e))
            print(f"❌ Error creating directory: {e}")
            return False

    def read_file(self, file_path: Union[str, Path], encoding: str = 'utf-8') -> Optional[str]:
        """Read file content"""
        path = Path(file_path)

        if not path.exists() or path.is_dir():
            print(f"❌ File not found: {path}")
            return None

        try:
            with open(path, 'r', encoding=encoding) as f:
                content = f.read()

            self._log_operation(FileOperation.READ, str(path), success=True, file_size=len(content))
            return content

        except Exception as e:
            self._log_operation(FileOperation.READ, str(path), success=False, error=str(e))
            print(f"❌ Error reading file: {e}")
            return None

    def write_file(self, file_path: Union[str, Path], content: str, encoding: str = 'utf-8') -> bool:
        """Write content to file"""
        path = Path(file_path)

        try:
            # Ensure parent directory exists
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, 'w', encoding=encoding) as f:
                f.write(content)

            self._log_operation(FileOperation.WRITE, str(path), success=True, file_size=len(content))
            print(f"✅ File written: {path}")
            return True

        except Exception as e:
            self._log_operation(FileOperation.WRITE, str(path), success=False, error=str(e))
            print(f"❌ Error writing file: {e}")
            return False

    def copy_file(self, source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """Copy file or directory"""
        src_path = Path(source)
        dst_path = Path(destination)

        if not src_path.exists():
            print(f"❌ Source not found: {src_path}")
            return False

        try:
            # Ensure destination parent directory exists
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            if src_path.is_dir():
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_path)

            file_size = src_path.stat().st_size if src_path.is_file() else 0
            self._log_operation(FileOperation.COPY, str(src_path), str(dst_path), success=True, file_size=file_size)
            print(f"✅ Copied: {src_path} → {dst_path}")
            return True

        except Exception as e:
            self._log_operation(FileOperation.COPY, str(src_path), str(dst_path), success=False, error=str(e))
            print(f"❌ Error copying: {e}")
            return False

    def move_file(self, source: Union[str, Path], destination: Union[str, Path]) -> bool:
        """Move file or directory"""
        src_path = Path(source)
        dst_path = Path(destination)

        if not src_path.exists():
            print(f"❌ Source not found: {src_path}")
            return False

        try:
            # Ensure destination parent directory exists
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            file_size = src_path.stat().st_size if src_path.is_file() else 0
            shutil.move(str(src_path), str(dst_path))

            self._log_operation(FileOperation.MOVE, str(src_path), str(dst_path), success=True, file_size=file_size)
            print(f"✅ Moved: {src_path} → {dst_path}")
            return True

        except Exception as e:
            self._log_operation(FileOperation.MOVE, str(src_path), str(dst_path), success=False, error=str(e))
            print(f"❌ Error moving: {e}")
            return False

    def delete_file(self, file_path: Union[str, Path], force: bool = False) -> bool:
        """Delete file or directory"""
        path = Path(file_path)

        if not path.exists():
            print(f"❌ File not found: {path}")
            return False

        try:
            file_size = path.stat().st_size if path.is_file() else 0

            if path.is_dir():
                if force:
                    shutil.rmtree(path)
                else:
                    path.rmdir()  # Only works if directory is empty
            else:
                path.unlink()

            self._log_operation(FileOperation.DELETE, str(path), success=True, file_size=file_size)
            print(f"✅ Deleted: {path}")
            return True

        except Exception as e:
            self._log_operation(FileOperation.DELETE, str(path), success=False, error=str(e))
            print(f"❌ Error deleting: {e}")
            return False

    def rename_file(self, old_path: Union[str, Path], new_name: str) -> bool:
        """Rename file or directory"""
        old_path = Path(old_path)

        if not old_path.exists():
            print(f"❌ File not found: {old_path}")
            return False

        new_path = old_path.parent / new_name

        try:
            old_path.rename(new_path)

            file_size = new_path.stat().st_size if new_path.is_file() else 0
            self._log_operation(FileOperation.RENAME, str(old_path), str(new_path), success=True, file_size=file_size)
            print(f"✅ Renamed: {old_path.name} → {new_name}")
            return True

        except Exception as e:
            self._log_operation(FileOperation.RENAME, str(old_path), str(new_path), success=False, error=str(e))
            print(f"❌ Error renaming: {e}")
            return False

    def search_files(
        self,
        search_term: str,
        search_directory: Union[str, Path] = None,
        search_content: bool = False,
        case_sensitive: bool = False,
        file_types: List[FileType] = None,
        max_results: int = 100
    ) -> List[FileInfo]:
        """Search for files by name or content"""

        if search_directory is None:
            search_directory = self.current_directory
        else:
            search_directory = Path(search_directory)

        if not search_directory.exists():
            print(f"❌ Search directory not found: {search_directory}")
            return []

        results = []
        search_pattern = search_term if case_sensitive else search_term.lower()

        try:
            for root, dirs, files in os.walk(search_directory):
                if len(results) >= max_results:
                    break

                for file in files:
                    if len(results) >= max_results:
                        break

                    file_path = Path(root) / file
                    file_info = self.get_file_info(file_path)

                    if not file_info:
                        continue

                    # Filter by file types if specified
                    if file_types and file_info.file_type not in file_types:
                        continue

                    # Search in filename
                    filename = file_info.name if case_sensitive else file_info.name.lower()
                    if search_pattern in filename:
                        results.append(file_info)
                        continue

                    # Search in content if requested
                    if search_content and file_info.file_type in [FileType.TEXT, FileType.CODE, FileType.DATA]:
                        try:
                            content = self.read_file(file_path)
                            if content:
                                content_search = content if case_sensitive else content.lower()
                                if search_pattern in content_search:
                                    results.append(file_info)
                        except Exception:
                            pass  # Skip files that can't be read

            print(f"🔍 Found {len(results)} files matching '{search_term}'")
            return results

        except Exception as e:
            print(f"❌ Error searching files: {e}")
            return []

    def compress_files(
        self,
        files: List[Union[str, Path]],
        archive_path: Union[str, Path],
        compression_type: str = "zip"
    ) -> bool:
        """Compress files into archive"""

        archive_path = Path(archive_path)

        try:
            if compression_type.lower() == "zip":
                with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in files:
                        file_path = Path(file_path)
                        if file_path.exists():
                            if file_path.is_file():
                                zipf.write(file_path, file_path.name)
                            elif file_path.is_dir():
                                for root, dirs, files_in_dir in os.walk(file_path):
                                    for file in files_in_dir:
                                        file_full_path = Path(root) / file
                                        arc_name = file_full_path.relative_to(file_path.parent)
                                        zipf.write(file_full_path, arc_name)

            elif compression_type.lower() in ["tar", "tar.gz", "tgz"]:
                mode = "w:gz" if compression_type.lower() in ["tar.gz", "tgz"] else "w"
                with tarfile.open(archive_path, mode) as tarf:
                    for file_path in files:
                        file_path = Path(file_path)
                        if file_path.exists():
                            tarf.add(file_path, file_path.name)

            else:
                print(f"❌ Unsupported compression type: {compression_type}")
                return False

            archive_size = archive_path.stat().st_size
            self._log_operation(FileOperation.COMPRESS, f"{len(files)} files", str(archive_path), success=True, file_size=archive_size)
            print(f"✅ Compressed {len(files)} files to: {archive_path}")
            return True

        except Exception as e:
            self._log_operation(FileOperation.COMPRESS, f"{len(files)} files", str(archive_path), success=False, error=str(e))
            print(f"❌ Error compressing files: {e}")
            return False

    def extract_archive(self, archive_path: Union[str, Path], extract_to: Union[str, Path] = None) -> bool:
        """Extract archive"""

        archive_path = Path(archive_path)

        if not archive_path.exists():
            print(f"❌ Archive not found: {archive_path}")
            return False

        if extract_to is None:
            extract_to = archive_path.parent / archive_path.stem
        else:
            extract_to = Path(extract_to)

        try:
            extract_to.mkdir(parents=True, exist_ok=True)

            if archive_path.suffix.lower() == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zipf:
                    zipf.extractall(extract_to)

            elif archive_path.suffix.lower() in ['.tar', '.gz', '.bz2', '.xz']:
                with tarfile.open(archive_path, 'r:*') as tarf:
                    tarf.extractall(extract_to)

            else:
                print(f"❌ Unsupported archive format: {archive_path.suffix}")
                return False

            self._log_operation(FileOperation.EXTRACT, str(archive_path), str(extract_to), success=True)
            print(f"✅ Extracted archive to: {extract_to}")
            return True

        except Exception as e:
            self._log_operation(FileOperation.EXTRACT, str(archive_path), str(extract_to), success=False, error=str(e))
            print(f"❌ Error extracting archive: {e}")
            return False

    def encrypt_file(self, file_path: Union[str, Path], encrypted_path: Union[str, Path] = None) -> bool:
        """Encrypt file"""

        if not ENCRYPTION_AVAILABLE:
            print("❌ Encryption not available (cryptography library not installed)")
            return False

        file_path = Path(file_path)

        if not file_path.exists() or file_path.is_dir():
            print(f"❌ File not found: {file_path}")
            return False

        if encrypted_path is None:
            encrypted_path = file_path.with_suffix(file_path.suffix + '.encrypted')
        else:
            encrypted_path = Path(encrypted_path)

        try:
            fernet = Fernet(self.encryption_key)

            # Read file content
            with open(file_path, 'rb') as f:
                file_data = f.read()

            # Encrypt data
            encrypted_data = fernet.encrypt(file_data)

            # Write encrypted file
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data)

            file_size = file_path.stat().st_size
            self._log_operation(FileOperation.ENCRYPT, str(file_path), str(encrypted_path), success=True, file_size=file_size)
            print(f"✅ File encrypted: {file_path} → {encrypted_path}")
            return True

        except Exception as e:
            self._log_operation(FileOperation.ENCRYPT, str(file_path), str(encrypted_path), success=False, error=str(e))
            print(f"❌ Error encrypting file: {e}")
            return False

    def decrypt_file(self, encrypted_path: Union[str, Path], decrypted_path: Union[str, Path] = None) -> bool:
        """Decrypt file"""

        if not ENCRYPTION_AVAILABLE:
            print("❌ Decryption not available (cryptography library not installed)")
            return False

        encrypted_path = Path(encrypted_path)

        if not encrypted_path.exists():
            print(f"❌ Encrypted file not found: {encrypted_path}")
            return False

        if decrypted_path is None:
            if encrypted_path.suffix == '.encrypted':
                decrypted_path = encrypted_path.with_suffix('')
            else:
                decrypted_path = encrypted_path.with_suffix('.decrypted')
        else:
            decrypted_path = Path(decrypted_path)

        try:
            fernet = Fernet(self.encryption_key)

            # Read encrypted file
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()

            # Decrypt data
            decrypted_data = fernet.decrypt(encrypted_data)

            # Write decrypted file
            with open(decrypted_path, 'wb') as f:
                f.write(decrypted_data)

            file_size = encrypted_path.stat().st_size
            self._log_operation(FileOperation.DECRYPT, str(encrypted_path), str(decrypted_path), success=True, file_size=file_size)
            print(f"✅ File decrypted: {encrypted_path} → {decrypted_path}")
            return True

        except Exception as e:
            self._log_operation(FileOperation.DECRYPT, str(encrypted_path), str(decrypted_path), success=False, error=str(e))
            print(f"❌ Error decrypting file: {e}")
            return False

    def start_monitoring(self, directory: Union[str, Path]) -> bool:
        """Start monitoring directory for changes"""

        if not WATCHDOG_AVAILABLE:
            print("❌ File monitoring not available (watchdog library not installed)")
            return False

        directory = Path(directory)

        if not directory.exists() or not directory.is_dir():
            print(f"❌ Directory not found: {directory}")
            return False

        directory_str = str(directory)

        if directory_str in self.watched_directories:
            print(f"⚠️ Directory already being monitored: {directory}")
            return True

        try:
            event_handler = FileSystemWatcher(self)
            observer = Observer()
            observer.schedule(event_handler, directory_str, recursive=True)
            observer.start()

            self.watched_directories[directory_str] = observer
            print(f"👁️ Started monitoring: {directory}")
            return True

        except Exception as e:
            print(f"❌ Error starting monitoring: {e}")
            return False

    def stop_monitoring(self, directory: Union[str, Path]) -> bool:
        """Stop monitoring directory"""

        directory_str = str(Path(directory))

        if directory_str not in self.watched_directories:
            print(f"⚠️ Directory not being monitored: {directory}")
            return False

        try:
            observer = self.watched_directories[directory_str]
            observer.stop()
            observer.join()

            del self.watched_directories[directory_str]
            print(f"🛑 Stopped monitoring: {directory}")
            return True

        except Exception as e:
            print(f"❌ Error stopping monitoring: {e}")
            return False

    def _log_file_event(self, event_type: str, file_path: str, dest_path: str = ""):
        """Log file system events"""
        timestamp = datetime.now()

        event_log = {
            "timestamp": timestamp.isoformat(),
            "event_type": event_type,
            "file_path": file_path,
            "dest_path": dest_path
        }

        # Log to file
        log_file = self.logs_dir / f"file_events_{timestamp.strftime('%Y%m%d')}.json"

        try:
            if log_file.exists():
                with open(log_file, 'r') as f:
                    events = json.load(f)
            else:
                events = []

            events.append(event_log)

            with open(log_file, 'w') as f:
                json.dump(events, f, indent=2)

        except Exception as e:
            print(f"❌ Error logging file event: {e}")

    def _log_operation(
        self,
        operation_type: FileOperation,
        source_path: str,
        target_path: str = "",
        success: bool = False,
        error: str = "",
        file_size: int = 0
    ):
        """Log file operations"""

        operation_id = f"op_{int(datetime.now().timestamp())}"

        operation = FileOperation(
            operation_id=operation_id,
            operation_type=operation_type,
            source_path=source_path,
            target_path=target_path,
            success=success,
            error_message=error,
            file_size=file_size
        )

        self.operation_history.append(operation)
        self.total_operations += 1

        if success:
            self.successful_operations += 1
        else:
            self.failed_operations += 1

        # Keep only last 1000 operations in memory
        if len(self.operation_history) > 1000:
            self.operation_history = self.operation_history[-1000:]

    def get_directory_size(self, directory: Union[str, Path]) -> int:
        """Calculate total size of directory"""
        directory = Path(directory)

        if not directory.exists() or not directory.is_dir():
            return 0

        total_size = 0

        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = Path(root) / file
                    try:
                        total_size += file_path.stat().st_size
                    except (OSError, FileNotFoundError):
                        pass  # Skip files that can't be accessed

            return total_size

        except Exception:
            return 0

    def get_file_count(self, directory: Union[str, Path], file_types: List[FileType] = None) -> Dict[str, int]:
        """Count files by type in directory"""
        directory = Path(directory)

        if not directory.exists() or not directory.is_dir():
            return {}

        counts = {
            "total_files": 0,
            "total_directories": 0,
            "by_type": {}
        }

        try:
            for root, dirs, files in os.walk(directory):
                counts["total_directories"] += len(dirs)

                for file in files:
                    file_path = Path(root) / file
                    file_type = self._get_file_type(file_path)

                    # Filter by file types if specified
                    if file_types and file_type not in file_types:
                        continue

                    counts["total_files"] += 1

                    type_name = file_type.value
                    if type_name not in counts["by_type"]:
                        counts["by_type"][type_name] = 0
                    counts["by_type"][type_name] += 1

            return counts

        except Exception as e:
            print(f"❌ Error counting files: {e}")
            return {}

    def get_duplicate_files(self, directory: Union[str, Path]) -> Dict[str, List[str]]:
        """Find duplicate files by checksum"""
        directory = Path(directory)

        if not directory.exists() or not directory.is_dir():
            return {}

        checksums = {}
        duplicates = {}

        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = Path(root) / file

                    if file_path.is_file():
                        checksum = self._calculate_checksum(file_path)

                        if checksum:
                            if checksum not in checksums:
                                checksums[checksum] = []
                            checksums[checksum].append(str(file_path))

            # Find duplicates
            for checksum, file_paths in checksums.items():
                if len(file_paths) > 1:
                    duplicates[checksum] = file_paths

            return duplicates

        except Exception as e:
            print(f"❌ Error finding duplicates: {e}")
            return {}

    def clean_temp_files(self) -> int:
        """Clean temporary files"""
        cleaned_count = 0

        try:
            for file_path in self.temp_dir.iterdir():
                if file_path.is_file():
                    file_path.unlink()
                    cleaned_count += 1
                elif file_path.is_dir():
                    shutil.rmtree(file_path)
                    cleaned_count += 1

            print(f"🧹 Cleaned {cleaned_count} temporary files")
            return cleaned_count

        except Exception as e:
            print(f"❌ Error cleaning temp files: {e}")
            return 0

    def get_statistics(self) -> Dict[str, Any]:
        """Get file manager statistics"""

        success_rate = 0.0
        if self.total_operations > 0:
            success_rate = (self.successful_operations / self.total_operations) * 100

        return {
            "total_operations": self.total_operations,
            "successful_operations": self.successful_operations,
            "failed_operations": self.failed_operations,
            "success_rate": round(success_rate, 2),
            "current_directory": str(self.current_directory),
            "watched_directories": len(self.watched_directories),
            "cached_files": len(self.file_cache),
            "file_monitoring": WATCHDOG_AVAILABLE,
            "file_encryption": ENCRYPTION_AVAILABLE,
            "manager_directory": str(self.manager_dir),
            "recent_operations": len(self.operation_history)
        }

    def get_recent_operations(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent file operations"""

        recent_ops = self.operation_history[-count:] if self.operation_history else []

        return [
            {
                "operation_id": op.operation_id,
                "type": op.operation_type.value,
                "source": op.source_path,
                "target": op.target_path,
                "timestamp": op.timestamp.isoformat(),
                "success": op.success,
                "error": op.error_message,
                "file_size": op.file_size,
                "duration": op.duration
            }
            for op in reversed(recent_ops)
        ]
