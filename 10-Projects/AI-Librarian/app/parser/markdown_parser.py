"""Markdown parser."""

from __future__ import annotations

from pathlib import Path

from .base import ParserCapabilities
from .cleaner import clean_text
from .encoding import detect_encoding, normalize_text_encoding
from .parser_result import ParseStats, ParsedDocument
from .tokenizer import count_characters, count_tokens, count_words


class MarkdownParser:
    """Parser for Markdown files."""

    capabilities = ParserCapabilities(supports_markdown=True)

    def parse(self, path: Path | str) -> ParsedDocument:
        candidate = Path(path).expanduser()
        encoding = detect_encoding(candidate)
        raw_text = candidate.read_text(encoding=encoding, errors="replace")
        normalized_text = normalize_text_encoding(raw_text)
        cleaned_text = clean_text(normalized_text)
        headings = [
            line.strip().lstrip("#").strip()
            for line in cleaned_text.splitlines()
            if line.lstrip().startswith("#") and line.strip()
        ]
        paragraphs = [
            segment.strip()
            for segment in cleaned_text.splitlines()
            if segment.strip() and not segment.lstrip().startswith("#")
        ]
        stats = ParseStats(
            characters=count_characters(cleaned_text),
            words=count_words(cleaned_text),
            tokens=count_tokens(cleaned_text),
            headings=len(headings),
            paragraphs=len(paragraphs),
        )
        return ParsedDocument(
            source_path=candidate.resolve(),
            text=cleaned_text,
            metadata={"encoding": encoding},
            stats=stats,
            headings=headings,
            paragraphs=paragraphs,
        )
