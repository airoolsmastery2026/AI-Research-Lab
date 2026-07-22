"""Main importer implementation for the ingestion pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

from app.core.logger import get_logger
from app.metadata import DocumentMetadata, extract_metadata, find_duplicates

from .detector import detect_file_type, supported_extensions
from .dispatcher import ImportDispatcher
from .errors import ImportError, ImportResumeError
from .filters import ImportFilter, build_default_filters
from .progress import ImportProgress, ProgressStage
from .queue import ImportQueue, ImportQueueItem
from .scanner import scan_documents

logger = get_logger("importer.main")


@dataclass(slots=True)
class ImportStatistics:
    scanned_files: int = 0
    imported_files: int = 0
    skipped_files: int = 0
    duplicate_files: int = 0
    failed_files: int = 0


@dataclass(slots=True)
class ImportResult:
    documents: list[DocumentMetadata] = field(default_factory=list)
    statistics: ImportStatistics = field(default_factory=ImportStatistics)
    progress: ImportProgress = field(default_factory=ImportProgress)
    duplicates: list[tuple[DocumentMetadata, DocumentMetadata]] = field(default_factory=list)


@dataclass(slots=True)
class Importer:
    """Production-ready document ingestion pipeline."""

    root_dir: Path | str
    filters: list[ImportFilter] = field(default_factory=build_default_filters)
    batch_size: int = 10
    resume_from: Path | None = None

    def run(self, *, resume: bool = False) -> ImportResult:
        root = Path(self.root_dir).expanduser().resolve()
        if not root.exists():
            raise ImportError(f"Import root does not exist: {root}")

        progress = ImportProgress(total_items=0)
        progress.update_stage(ProgressStage.SCANNING)
        discovered_paths = scan_documents(root, filters=self.filters)
        progress.total_items = len(discovered_paths)
        progress.update_stage(ProgressStage.QUEUING)

        dispatcher = ImportDispatcher()
        for path in discovered_paths:
            dispatcher.enqueue_path(path)

        if resume and self.resume_from is not None:
            self._ensure_resume_state(self.resume_from)

        progress.update_stage(ProgressStage.IMPORTING)
        imported_documents: list[DocumentMetadata] = []
        for _ in range(min(self.batch_size, len(discovered_paths))):
            try:
                batch = dispatcher.dispatch(batch_size=self.batch_size)
            except Exception as exc:
                logger.exception("Import batch failed")
                raise ImportError(f"Batch import failed: {exc}") from exc
            imported_documents.extend(batch)
            progress.mark_processed()

        progress.update_stage(ProgressStage.COMPLETE)
        duplicates = find_duplicates(imported_documents)
        statistics = ImportStatistics(
            scanned_files=len(discovered_paths),
            imported_files=len(imported_documents),
            skipped_files=0,
            duplicate_files=len(duplicates),
            failed_files=0,
        )
        return ImportResult(
            documents=imported_documents,
            statistics=statistics,
            progress=progress,
            duplicates=duplicates,
        )

    def _ensure_resume_state(self, checkpoint_path: Path | str) -> None:
        checkpoint = Path(checkpoint_path).expanduser()
        if not checkpoint.exists():
            raise ImportResumeError(f"Resume checkpoint not found: {checkpoint}")
