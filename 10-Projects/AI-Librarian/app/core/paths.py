"""Path helpers for project directories and file locations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Union

from .constants import (
    DEFAULT_DATA_DIRNAME,
    DEFAULT_DOCS_DIRNAME,
    DEFAULT_LOGS_DIRNAME,
    DEFAULT_OUTPUT_DIRNAME,
    DEFAULT_PROJECT_ROOT,
    DEFAULT_PROMPTS_DIRNAME,
    DEFAULT_TEMPLATES_DIRNAME,
)
from .exceptions import FileSystemError, PathResolutionError


@dataclass(slots=True)
class AppPaths:
    """Centralized path definitions for the project."""

    project_root: Path
    data_dir: Path
    docs_dir: Path
    output_dir: Path
    prompts_dir: Path
    templates_dir: Path
    logs_dir: Path

    @classmethod
    def from_project_root(
        cls,
        project_root: Optional[Union[str, Path]] = None,
        *,
        create: bool = True,
    ) -> "AppPaths":
        resolved_root = cls._resolve_project_root(project_root)
        paths = cls(
            project_root=resolved_root,
            data_dir=resolved_root / DEFAULT_DATA_DIRNAME,
            docs_dir=resolved_root / DEFAULT_DOCS_DIRNAME,
            output_dir=resolved_root / DEFAULT_OUTPUT_DIRNAME,
            prompts_dir=resolved_root / DEFAULT_PROMPTS_DIRNAME,
            templates_dir=resolved_root / DEFAULT_TEMPLATES_DIRNAME,
            logs_dir=resolved_root / DEFAULT_LOGS_DIRNAME,
        )
        if create:
            paths.ensure_exists()
        return paths

    def ensure_exists(self) -> "AppPaths":
        """Create all configured directories if they are missing."""

        for directory in self.iter_directories():
            try:
                directory.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                raise FileSystemError(f"Unable to create directory: {directory}") from exc
        return self

    def resolve(self, *parts: Union[str, Path]) -> Path:
        """Resolve a path relative to the project root."""

        if not parts:
            raise PathResolutionError("At least one path segment is required")
        combined = Path(*parts)
        if combined.is_absolute():
            return combined.resolve()
        return (self.project_root / combined).resolve()

    def iter_directories(self) -> Iterable[Path]:
        """Return the configured directories in consistent order."""

        return (
            self.data_dir,
            self.docs_dir,
            self.output_dir,
            self.prompts_dir,
            self.templates_dir,
            self.logs_dir,
        )

    @staticmethod
    def _resolve_project_root(project_root: Optional[Union[str, Path]]) -> Path:
        if project_root is None:
            return DEFAULT_PROJECT_ROOT.resolve()
        candidate = Path(project_root).expanduser()
        if not candidate.is_absolute():
            candidate = (Path.cwd() / candidate).resolve()
        return candidate.resolve()
