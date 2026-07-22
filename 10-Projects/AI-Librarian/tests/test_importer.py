import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.importer import Importer, build_default_filters, detect_file_type, scan_documents
from app.importer.dispatcher import ImportDispatcher
from app.importer.filters import ImportFilter
from app.importer.progress import ProgressStage


def test_scan_documents_recurses_and_filters(tmp_path):
    sample_dir = tmp_path / "input"
    sample_dir.mkdir()
    visible_path = sample_dir / "visible.txt"
    visible_path.write_text("visible content\n", encoding="utf-8")
    hidden_dir = sample_dir / ".hidden"
    hidden_dir.mkdir()
    hidden_path = hidden_dir / "skip.md"
    hidden_path.write_text("hidden\n", encoding="utf-8")
    unsupported = sample_dir / "notes.bin"
    unsupported.write_bytes(b"data")

    filters = build_default_filters()
    discovered = scan_documents(sample_dir, filters=filters)

    assert visible_path in discovered
    assert hidden_path not in discovered
    assert unsupported not in discovered


def test_detect_file_type_reports_supported_extension(tmp_path):
    path = tmp_path / "report.pdf"
    path.write_bytes(b"pdf")

    file_info = detect_file_type(path)

    assert file_info.extension == ".pdf"
    assert file_info.is_supported is True


def test_dispatcher_builds_metadata_for_valid_file(tmp_path):
    path = tmp_path / "sample.txt"
    path.write_text("hello\n", encoding="utf-8")

    dispatcher = ImportDispatcher()
    dispatcher.enqueue_path(path)
    documents = dispatcher.dispatch(batch_size=1)

    assert len(documents) == 1
    assert documents[0].absolute_path == path.resolve()


def test_importer_run_returns_statistics(tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    path = root / "import.md"
    path.write_text("# Heading\n", encoding="utf-8")

    importer = Importer(root_dir=root, batch_size=1)
    result = importer.run()

    assert result.statistics.scanned_files == 1
    assert result.statistics.imported_files == 1
    assert result.progress.current_stage == ProgressStage.COMPLETE
