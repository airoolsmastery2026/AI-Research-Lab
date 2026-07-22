"""Excel parser placeholder backed by CSV-compatible text extraction."""

from __future__ import annotations

from pathlib import Path

from .base import ParserCapabilities
from .cleaner import clean_text
from .parser_result import ParseStats, ParsedDocument
from .tokenizer import count_characters, count_tokens, count_words


class ExcelParser:
    """Parser for Excel workbooks."""

    capabilities = ParserCapabilities(supports_excel=True)

    def parse(self, path: Path | str) -> ParsedDocument:
        candidate = Path(path).expanduser()
        text = candidate.read_text(encoding="utf-8", errors="replace")
        cleaned_text = clean_text(text)
        stats = ParseStats(
            characters=count_characters(cleaned_text),
            words=count_words(cleaned_text),
            tokens=count_tokens(cleaned_text),
        )
        return ParsedDocument(
            source_path=candidate.resolve(),
            text=cleaned_text,
            metadata={"source": "excel_text_fallback"},
            stats=stats,
        )
