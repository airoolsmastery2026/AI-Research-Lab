"""Document parsing engine package."""

from .base import BaseParser, ParserCapabilities
from .cleaner import clean_text
from .encoding import detect_encoding, normalize_text_encoding
from .errors import ParserError, ParserValidationError
from .factory import ParserFactory, parse_document
from .parser_result import ParseStats, ParsedDocument
from .tokenizer import count_characters, count_tokens, count_words

__all__ = [
    "BaseParser",
    "ParserCapabilities",
    "ParserError",
    "ParserFactory",
    "ParserValidationError",
    "ParseStats",
    "ParsedDocument",
    "clean_text",
    "count_characters",
    "count_tokens",
    "count_words",
    "detect_encoding",
    "normalize_text_encoding",
    "parse_document",
]
