import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.metadata import DocumentMetadata, extract_metadata, find_duplicates, serialize_metadata


def test_extract_metadata_for_text_file(tmp_path):
    document_path = tmp_path / "sample.txt"
    document_path.write_text("Hello world\nThis is a sample document.\n", encoding="utf-8")

    metadata = extract_metadata(document_path, root_dir=tmp_path)

    assert isinstance(metadata, DocumentMetadata)
    assert metadata.extension == ".txt"
    assert metadata.mime_type == "text/plain"
    assert metadata.file_size_bytes > 0
    assert metadata.sha256
    assert metadata.absolute_path == document_path.resolve()
    assert metadata.relative_path == "sample.txt"
    assert metadata.created_time is not None
    assert metadata.modified_time is not None
    assert metadata.accessed_time is not None
    assert metadata.language in {"en", "unknown"}


def test_duplicate_detection_detects_same_content(tmp_path):
    first_path = tmp_path / "first.txt"
    second_path = tmp_path / "second.txt"
    content = "Duplicate content\n"
    first_path.write_text(content, encoding="utf-8")
    second_path.write_text(content, encoding="utf-8")

    first_metadata = extract_metadata(first_path, root_dir=tmp_path)
    second_metadata = extract_metadata(second_path, root_dir=tmp_path)

    assert first_metadata.is_duplicate_of(second_metadata)
    duplicates = find_duplicates([first_metadata, second_metadata])
    assert len(duplicates) == 1


def test_serializer_round_trip(tmp_path):
    document_path = tmp_path / "roundtrip.md"
    document_path.write_text("# Heading\n", encoding="utf-8")

    metadata = extract_metadata(document_path, root_dir=tmp_path)
    payload = serialize_metadata(metadata)
    restored = DocumentMetadata.from_dict(payload)

    assert restored.document_id == metadata.document_id
    assert restored.absolute_path == metadata.absolute_path
    assert restored.relative_path == metadata.relative_path


def test_validation_reports_invalid_path(tmp_path):
    missing_path = tmp_path / "missing.txt"

    metadata = extract_metadata(missing_path, root_dir=tmp_path)
    assert metadata.validation_report.is_valid is False
    assert metadata.validation_report.issues
