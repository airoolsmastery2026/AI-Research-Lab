"""Base classes for format-specific parsers."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from app.core.logger import get_logger

from .parser_result import ParsedDocument
from .errors import ParserError

logger = get_logger("parser.base")


@dataclass(slots=True)
class ParserCapabilities:
    supports_pdf: bool = False
    supports_docx: bool = False
    supports_txt: bool = False
    supports_markdown: bool = False
    supports_csv: bool = False
    supports_excel: bool = False
    supports_html: bool = False
    supports_epub: bool = False
    supports_json: bool = False
    supports_xml: bool = False


class BaseParser(Protocol):
    """Protocol for all concrete parsers."""

    capabilities: ParserCapabilities

    def parse(self, path: Path | str) -> ParsedDocument:
        ...
