import re
import langcodes

def is_cjk(char):
    """Check if character is Chinese, Japanese, or Korean"""
    cp = ord(char)
    return (
        (0x4E00 <= cp <= 0x9FFF) or  # CJK Unified Ideographs
        (0x3040 <= cp <= 0x30FF) or  # Japanese Hiragana/Katakana
        (0xAC00 <= cp <= 0xD7AF)    # Hangul Syllables
    )

def is_rtl(char):
    """Check if character is from a right-to-left script"""
    return ord(char) >= 0x0590 and ord(char) <= 0x08FF

def contains_multilingual(text):
    """Detect presence of non-Latin scripts"""
    for char in text:
        if is_cjk(char) or is_rtl(char):
            return True
    return False

def multilingual_numbered_pattern():
    """Generate regex pattern for numbered lists in multiple languages"""
    # Western digits, Japanese, Chinese, Arabic-Indic, etc.
    return re.compile(
        r'^([0-9]+[\.\)]|'                  # Western: 1. 1)
        r'[一二三四五六七八九十]+[\.、．]|'     # Chinese: 一、 二．
        r'[①②③④⑤⑥⑦⑧⑨⑩]+|'              # Circled numbers
        r'[⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽]+|'              # Parenthesized numbers
        r'[\u0660-\u0669]+[\.\)]'           # Arabic-Indic: ١. ٢)
        r')'
    )