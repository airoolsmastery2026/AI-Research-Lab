"""Factory for selecting suitable parsers."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from app.core.logger import get_logger

from .csv_parser import CsvParser
from .epub_parser import EpubParser
from .errors import ParserValidationError
from .excel_parser import ExcelParser
from .html_parser import HtmlParser
from .json_parser import JsonParser
from .markdown_parser import MarkdownParser
from .txt_parser import TextParser
from .xml_parser import XmlParser
from .parser_result import ParsedDocument

logger = get_logger("parser.factory")


class ParserFactory:
    """Selects a parser based on file extension."""

    def __init__(self) -> None:
        self._parsers = {
            ".txt": TextParser(),
            ".md": MarkdownParser(),
            ".csv": CsvParser(),
            ".xlsx": ExcelParser(),
            ".xls": ExcelParser(),
            ".html": HtmlParser(),
            ".epub": EpubParser(),
            ".json": JsonParser(),
            ".xml": XmlParser(),
        }

    def get_parser(self, path: Path | str) -> object:
        candidate = Path(path).expanduser()
        extension = candidate.suffix.lower()
        parser = self._parsers.get(extension)
        if parser is None:
            raise ParserValidationError(f"No parser available for extension: {extension}")
        return parser


def parse_document(path: Path | str) -> ParsedDocument:
    factory = ParserFactory()
    parser = factory.get_parser(path)
    logger.info("Parsing %s with %s", path, parser.__class__.__name__)
    return parser.parse(path)
