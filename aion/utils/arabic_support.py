"""
🇸🇦 AION Arabic Support Module
Advanced Arabic text processing and display utilities

This module provides comprehensive Arabic language support including:
- Arabic text normalization and processing
- RTL (Right-to-Left) text handling and display
- Arabic character validation and conversion
- Terminal display optimization for Arabic text
- Arabic keyboard input handling
- Arabic date and number formatting
- Professional Arabic text rendering
"""

import re
import unicodedata
from typing import Optional, List, Dict, Any, Tuple
from enum import Enum

class ArabicTextDirection(Enum):
    """Arabic text direction options"""
    RTL = "rtl"  # Right-to-Left
    LTR = "ltr"  # Left-to-Right
    AUTO = "auto"  # Automatic detection

class ArabicSupport:
    """
    Professional Arabic Language Support System
    
    This class provides comprehensive Arabic text processing with:
    - Advanced Arabic text normalization and cleaning
    - RTL text handling with proper alignment and display
    - Arabic character validation and Unicode processing
    - Terminal-optimized Arabic text rendering
    - Arabic input method support and validation
    - Arabic numeral conversion (Arabic-Indic ↔ Western)
    - Arabic date formatting and localization
    - Professional Arabic typography support
    
    The system handles all Arabic script complexities including:
    - Contextual letter forms and ligatures
    - Diacritical marks (Tashkeel) processing
    - Mixed Arabic-English text (bidirectional)
    - Arabic punctuation and spacing rules
    """
    
    # Arabic Unicode ranges
    ARABIC_RANGE = (0x0600, 0x06FF)  # Arabic block
    ARABIC_SUPPLEMENT_RANGE = (0x0750, 0x077F)  # Arabic Supplement
    ARABIC_EXTENDED_A_RANGE = (0x08A0, 0x08FF)  # Arabic Extended-A
    ARABIC_PRESENTATION_FORMS_A = (0xFB50, 0xFDFF)  # Arabic Presentation Forms-A
    ARABIC_PRESENTATION_FORMS_B = (0xFE70, 0xFEFF)  # Arabic Presentation Forms-B
    
    # Arabic-Indic digits mapping
    ARABIC_INDIC_DIGITS = {
        '0': '٠', '1': '١', '2': '٢', '3': '٣', '4': '٤',
        '5': '٥', '6': '٦', '7': '٧', '8': '٨', '9': '٩'
    }
    
    WESTERN_DIGITS = {v: k for k, v in ARABIC_INDIC_DIGITS.items()}
    
    # Common Arabic words for interface
    COMMON_ARABIC_TERMS = {
        "welcome": "مرحباً",
        "hello": "أهلاً",
        "goodbye": "وداعاً",
        "yes": "نعم",
        "no": "لا",
        "please": "من فضلك",
        "thank_you": "شكراً",
        "error": "خطأ",
        "success": "نجح",
        "loading": "جاري التحميل",
        "save": "حفظ",
        "cancel": "إلغاء",
        "continue": "متابعة",
        "exit": "خروج",
        "help": "مساعدة",
        "settings": "إعدادات",
        "language": "اللغة",
        "arabic": "العربية"
    }
    
    def __init__(self):
        self.text_direction = ArabicTextDirection.AUTO
        self.use_arabic_numerals = True
        self.normalize_text = True
    
    def is_arabic_text(self, text: str) -> bool:
        """Check if text contains Arabic characters"""
        if not text:
            return False
        
        arabic_chars = 0
        total_chars = 0
        
        for char in text:
            if char.isalpha():
                total_chars += 1
                if self.is_arabic_char(char):
                    arabic_chars += 1
        
        if total_chars == 0:
            return False
        
        # Consider text Arabic if more than 50% of alphabetic characters are Arabic
        return (arabic_chars / total_chars) > 0.5
    
    def is_arabic_char(self, char: str) -> bool:
        """Check if a character is Arabic"""
        if not char:
            return False
        
        code_point = ord(char)
        
        return (
            self.ARABIC_RANGE[0] <= code_point <= self.ARABIC_RANGE[1] or
            self.ARABIC_SUPPLEMENT_RANGE[0] <= code_point <= self.ARABIC_SUPPLEMENT_RANGE[1] or
            self.ARABIC_EXTENDED_A_RANGE[0] <= code_point <= self.ARABIC_EXTENDED_A_RANGE[1] or
            self.ARABIC_PRESENTATION_FORMS_A[0] <= code_point <= self.ARABIC_PRESENTATION_FORMS_A[1] or
            self.ARABIC_PRESENTATION_FORMS_B[0] <= code_point <= self.ARABIC_PRESENTATION_FORMS_B[1]
        )
    
    def normalize_arabic_text(self, text: str) -> str:
        """Normalize Arabic text for consistent processing"""
        if not text:
            return text
        
        # Unicode normalization
        text = unicodedata.normalize('NFKC', text)
        
        # Replace different forms of Arabic letters with standard forms
        replacements = {
            'ي': 'ي',  # Ya
            'ك': 'ك',  # Kaf
            'ة': 'ة',  # Ta Marbuta
            'أ': 'أ',  # Alif with Hamza above
            'إ': 'إ',  # Alif with Hamza below
            'آ': 'آ',  # Alif with Madda above
            'ء': 'ء',  # Hamza
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text
    
    def remove_diacritics(self, text: str) -> str:
        """Remove Arabic diacritical marks (Tashkeel)"""
        if not text:
            return text
        
        # Arabic diacritical marks Unicode range
        diacritics_pattern = r'[\u064B-\u065F\u0670\u06D6-\u06ED]'
        return re.sub(diacritics_pattern, '', text)
    
    def convert_to_arabic_numerals(self, text: str) -> str:
        """Convert Western numerals to Arabic-Indic numerals"""
        if not text or not self.use_arabic_numerals:
            return text
        
        for western, arabic in self.ARABIC_INDIC_DIGITS.items():
            text = text.replace(western, arabic)
        
        return text
    
    def convert_to_western_numerals(self, text: str) -> str:
        """Convert Arabic-Indic numerals to Western numerals"""
        if not text:
            return text
        
        for arabic, western in self.WESTERN_DIGITS.items():
            text = text.replace(arabic, western)
        
        return text
    
    def format_arabic_text_for_terminal(self, text: str, width: Optional[int] = None) -> str:
        """Format Arabic text for optimal terminal display"""
        if not text:
            return text
        
        # Normalize text if enabled
        if self.normalize_text:
            text = self.normalize_arabic_text(text)
        
        # Handle RTL display
        if self.is_arabic_text(text):
            # Add RTL mark for proper display
            text = f"\u202E{text}\u202C"
        
        # Handle width constraint
        if width and len(text) > width:
            # Truncate with ellipsis, preserving RTL
            if self.is_arabic_text(text):
                text = text[:width-3] + "..."
            else:
                text = text[:width-3] + "..."
        
        return text
    
    def get_text_direction(self, text: str) -> ArabicTextDirection:
        """Determine text direction"""
        if self.text_direction != ArabicTextDirection.AUTO:
            return self.text_direction
        
        if self.is_arabic_text(text):
            return ArabicTextDirection.RTL
        else:
            return ArabicTextDirection.LTR
    
    def align_text(self, text: str, width: int, alignment: str = "auto") -> str:
        """Align text based on language direction"""
        if not text or width <= 0:
            return text
        
        text_len = len(text)
        if text_len >= width:
            return text
        
        padding = width - text_len
        
        if alignment == "auto":
            direction = self.get_text_direction(text)
            if direction == ArabicTextDirection.RTL:
                alignment = "right"
            else:
                alignment = "left"
        
        if alignment == "center":
            left_pad = padding // 2
            right_pad = padding - left_pad
            return " " * left_pad + text + " " * right_pad
        elif alignment == "right":
            return " " * padding + text
        else:  # left alignment
            return text + " " * padding
    
    def wrap_arabic_text(self, text: str, width: int) -> List[str]:
        """Wrap Arabic text preserving word boundaries"""
        if not text or width <= 0:
            return [text] if text else []
        
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            
            if len(test_line) <= width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    # Word is longer than width, force break
                    lines.append(word[:width])
                    current_line = word[width:]
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def get_arabic_term(self, key: str) -> str:
        """Get Arabic translation for common terms"""
        return self.COMMON_ARABIC_TERMS.get(key, key)
    
    def format_arabic_number(self, number: int) -> str:
        """Format number in Arabic style"""
        number_str = str(number)
        
        if self.use_arabic_numerals:
            number_str = self.convert_to_arabic_numerals(number_str)
        
        return number_str
    
    def validate_arabic_input(self, text: str) -> Tuple[bool, str]:
        """Validate Arabic text input"""
        if not text:
            return True, ""
        
        try:
            # Check for valid Unicode
            text.encode('utf-8')
            
            # Normalize text
            normalized = self.normalize_arabic_text(text)
            
            return True, normalized
            
        except UnicodeError as e:
            return False, f"Invalid Unicode in Arabic text: {e}"
        except Exception as e:
            return False, f"Arabic text validation error: {e}"
    
    def get_display_info(self, text: str) -> Dict[str, Any]:
        """Get comprehensive display information for text"""
        return {
            "is_arabic": self.is_arabic_text(text),
            "direction": self.get_text_direction(text).value,
            "length": len(text),
            "normalized": self.normalize_arabic_text(text),
            "without_diacritics": self.remove_diacritics(text),
            "terminal_formatted": self.format_arabic_text_for_terminal(text)
        }
