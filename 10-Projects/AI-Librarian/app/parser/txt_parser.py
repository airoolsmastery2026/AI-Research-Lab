"""Plain text parser."""

from __future__ import annotations

from pathlib import Path

from app.core.logger import get_logger

from .base import ParserCapabilities
from .cleaner import clean_text
from .encoding import detect_encoding, normalize_text_encoding
from .parser_result import ParseStats, ParsedDocument
from .tokenizer import count_characters, count_tokens, count_words

logger = get_logger("parser.txt")


class TextParser:
    """Parser for plain text files."""

    capabilities = ParserCapabilities(supports_txt=True)

    def parse(self, path: Path | str) -> ParsedDocument:
        candidate = Path(path).expanduser()
        encoding = detect_encoding(candidate)
        raw_text = candidate.read_text(encoding=encoding, errors="replace")
        normalized_text = normalize_text_encoding(raw_text)
        cleaned_text = clean_text(normalized_text)
        paragraphs = [segment for segment in cleaned_text.split("\n") if segment.strip()]
        stats = ParseStats(
            characters=count_characters(cleaned_text),
            words=count_words(cleaned_text),
            tokens=count_tokens(cleaned_text),
            paragraphs=len(paragraphs),
        )
        logger.info("Parsed text file %s", candidate)
        return ParsedDocument(
            source_path=candidate.resolve(),
            text=cleaned_text,
            language="unknown",
            metadata={"encoding": encoding},
            stats=stats,
            paragraphs=paragraphs,
            headings=[segment for segment in paragraphs if segment.startswith("#")],
        )
