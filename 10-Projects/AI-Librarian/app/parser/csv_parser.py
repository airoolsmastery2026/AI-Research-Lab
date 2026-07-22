"""CSV parsing support."""

from __future__ import annotations

import csv
from pathlib import Path

from .base import ParserCapabilities
from .cleaner import clean_text
from .parser_result import ParseStats, ParsedDocument
from .tokenizer import count_characters, count_tokens, count_words


class CsvParser:
    """Parser for CSV files."""

    capabilities = ParserCapabilities(supports_csv=True)

    def parse(self, path: Path | str) -> ParsedDocument:
        candidate = Path(path).expanduser()
        with candidate.open("r", encoding="utf-8", errors="replace", newline="") as handle:
            rows = list(csv.reader(handle))
        text = "\n".join(" | ".join(row) for row in rows)
        cleaned_text = clean_text(text)
        stats = ParseStats(
            characters=count_characters(cleaned_text),
            words=count_words(cleaned_text),
            tokens=count_tokens(cleaned_text),
            tables=1 if rows else 0,
        )
        return ParsedDocument(
            source_path=candidate.resolve(),
            text=cleaned_text,
            metadata={"rows": len(rows), "columns": len(rows[0]) if rows else 0},
            stats=stats,
            tables=[rows],
        )
