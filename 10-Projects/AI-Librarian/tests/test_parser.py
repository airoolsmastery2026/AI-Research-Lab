import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.parser import ParserFactory, clean_text, count_characters, count_words, detect_encoding, normalize_text_encoding, parse_document


def test_text_parser_extracts_text_and_stats(tmp_path):
    document_path = tmp_path / "sample.txt"
    document_path.write_text("Hello world\nThis is a sample.\n", encoding="utf-8")

    result = parse_document(document_path)

    assert result.text
    assert result.stats.words >= 1
    assert result.stats.characters >= 1
    assert result.stats.paragraphs >= 1


def test_markdown_parser_detects_headings(tmp_path):
    document_path = tmp_path / "notes.md"
    document_path.write_text("# Title\n\nBody text\n", encoding="utf-8")

    result = parse_document(document_path)

    assert result.headings == ["Title"]


def test_factory_selects_parser_for_csv(tmp_path):
    document_path = tmp_path / "table.csv"
    document_path.write_text("a,b\n1,2\n", encoding="utf-8")

    parser = ParserFactory().get_parser(document_path)
    result = parser.parse(document_path)

    assert result.stats.tables == 1
    assert result.metadata["rows"] == 2


def test_cleaning_and_normalization_helpers(tmp_path):
    text = "Hello   world\n"
    cleaned = clean_text(text)
    normalized = normalize_text_encoding("Hello world")

    assert cleaned == "Hello world"
    assert normalized == "Hello world"
    assert count_words(cleaned) == 2
    assert count_characters(cleaned) == 11
