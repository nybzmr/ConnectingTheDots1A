"""Top-level package for PDF Outline Extractor."""

from .outline_extractor import get_outline
from .language_support import (
    contains_multilingual,
    is_cjk,
    is_rtl,
    multilingual_numbered_pattern
)

__all__ = [
    'get_outline',
    'contains_multilingual',
    'is_cjk',
    'is_rtl',
    'multilingual_numbered_pattern'
]