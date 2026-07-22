"""JSON parser."""

from __future__ import annotations

import json
from pathlib import Path

from .base import ParserCapabilities
from .cleaner import clean_text
from .parser_result import ParseStats, ParsedDocument
from .tokenizer import count_characters, count_tokens, count_words


class JsonParser:
    """Parser for JSON files."""

    capabilities = ParserCapabilities(supports_json=True)

    def parse(self, path: Path | str) -> ParsedDocument:
        candidate = Path(path).expanduser()
        with candidate.open("r", encoding="utf-8", errors="replace") as handle:
            payload = json.load(handle)
        text = json.dumps(payload, ensure_ascii=False)
        cleaned_text = clean_text(text)
        stats = ParseStats(
            characters=count_characters(cleaned_text),
            words=count_words(cleaned_text),
            tokens=count_tokens(cleaned_text),
        )
        return ParsedDocument(
            source_path=candidate.resolve(),
            text=cleaned_text,
            metadata={"json_type": type(payload).__name__},
            stats=stats,
        )
