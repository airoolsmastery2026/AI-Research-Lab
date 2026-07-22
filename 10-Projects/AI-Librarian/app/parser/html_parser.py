"""HTML parser."""

from __future__ import annotations

import re
from pathlib import Path

from .base import ParserCapabilities
from .cleaner import clean_text
from .encoding import detect_encoding, normalize_text_encoding
from .parser_result import ParseStats, ParsedDocument
from .tokenizer import count_characters, count_tokens, count_words


class HtmlParser:
    """Parser for HTML files."""

    capabilities = ParserCapabilities(supports_html=True)

    def parse(self, path: Path | str) -> ParsedDocument:
        candidate = Path(path).expanduser()
        encoding = detect_encoding(candidate)
        raw_text = candidate.read_text(encoding=encoding, errors="replace")
        normalized_text = normalize_text_encoding(raw_text)
        cleaned_text = clean_text(re.sub(r"<[^>]+>", " ", normalized_text))
        stats = ParseStats(
            characters=count_characters(cleaned_text),
            words=count_words(cleaned_text),
            tokens=count_tokens(cleaned_text),
        )
        return ParsedDocument(
            source_path=candidate.resolve(),
            text=cleaned_text,
            metadata={"encoding": encoding},
            stats=stats,
        )
