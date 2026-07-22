"""XML parser."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from .base import ParserCapabilities
from .cleaner import clean_text
from .parser_result import ParseStats, ParsedDocument
from .tokenizer import count_characters, count_tokens, count_words


class XmlParser:
    """Parser for XML files."""

    capabilities = ParserCapabilities(supports_xml=True)

    def parse(self, path: Path | str) -> ParsedDocument:
        candidate = Path(path).expanduser()
        tree = ET.parse(candidate)
        text = ET.tostring(tree.getroot(), encoding="unicode")
        cleaned_text = clean_text(text)
        stats = ParseStats(
            characters=count_characters(cleaned_text),
            words=count_words(cleaned_text),
            tokens=count_tokens(cleaned_text),
        )
        return ParsedDocument(
            source_path=candidate.resolve(),
            text=cleaned_text,
            metadata={"root_tag": tree.getroot().tag},
            stats=stats,
        )
