"""Application configuration helpers and environment loading."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Sequence, Union

from .constants import (
    DEFAULT_APP_NAME,
    DEFAULT_APP_VERSION,
    DEFAULT_AUTO_CREATE_FOLDERS,
    DEFAULT_ENVIRONMENT,
    DEFAULT_LOG_LEVEL,
    DEFAULT_MAX_FILE_SIZE_MB,
    DEFAULT_REQUEST_TIMEOUT_SECONDS,
    DEFAULT_SUPPORTED_EXTENSIONS,
    ENV_APP_NAME,
    ENV_APP_VERSION,
    ENV_AUTO_CREATE_FOLDERS,
    ENV_DEBUG,
    ENV_DOCS_DIR,
    ENV_ENVIRONMENT,
    ENV_LOG_FILE,
    ENV_LOG_LEVEL,
    ENV_MAX_FILE_SIZE_MB,
    ENV_OUTPUT_DIR,
    ENV_PROJECT_ROOT,
    ENV_PROMPTS_DIR,
    ENV_REQUEST_TIMEOUT_SECONDS,
    ENV_SUPPORTED_EXTENSIONS,
    ENV_TEMPLATES_DIR,
    ENV_DATA_DIR,
)
from .exceptions import ConfigurationError
from .paths import AppPaths


@dataclass(slots=True)
class AppConfig:
    """Configuration object for application behavior."""

    app_name: str = DEFAULT_APP_NAME
    app_version: str = DEFAULT_APP_VERSION
    environment: str = DEFAULT_ENVIRONMENT
    debug: bool = False
    log_level: str = DEFAULT_LOG_LEVEL
    log_file: Optional[Path] = None
    project_root: Path = field(default_factory=lambda: Path.cwd())
    data_dir: Path = field(default_factory=lambda: Path("data"))
    docs_dir: Path = field(default_factory=lambda: Path("docs"))
    output_dir: Path = field(default_factory=lambda: Path("output"))
    prompts_dir: Path = field(default_factory=lambda: Path("prompts"))
    templates_dir: Path = field(default_factory=lambda: Path("templates"))
    supported_extensions: tuple[str, ...] = DEFAULT_SUPPORTED_EXTENSIONS
    auto_create_folders: bool = DEFAULT_AUTO_CREATE_FOLDERS
    max_file_size_mb: int = DEFAULT_MAX_FILE_SIZE_MB
    request_timeout_seconds: int = DEFAULT_REQUEST_TIMEOUT_SECONDS

    @classmethod
    def from_env(cls, env: Optional[dict[str, str]] = None) -> "AppConfig":
        """Load configuration from the environment with sensible defaults."""

        values = env or os.environ
        config = cls()
        config.app_name = _get_env_str(values, ENV_APP_NAME, config.app_name)
        config.app_version = _get_env_str(values, ENV_APP_VERSION, config.app_version)
        config.environment = _get_env_str(values, ENV_ENVIRONMENT, config.environment)
        config.debug = _get_env_bool(values, ENV_DEBUG, config.debug)
        config.log_level = _get_env_str(values, ENV_LOG_LEVEL, config.log_level)
        config.log_file = _get_env_path(values, ENV_LOG_FILE)
        config.project_root = _get_env_path(values, ENV_PROJECT_ROOT, default=config.project_root)
        config.data_dir = _get_env_path(values, ENV_DATA_DIR, default=config.data_dir)
        config.docs_dir = _get_env_path(values, ENV_DOCS_DIR, default=config.docs_dir)
        config.output_dir = _get_env_path(values, ENV_OUTPUT_DIR, default=config.output_dir)
        config.prompts_dir = _get_env_path(values, ENV_PROMPTS_DIR, default=config.prompts_dir)
        config.templates_dir = _get_env_path(values, ENV_TEMPLATES_DIR, default=config.templates_dir)
        config.supported_extensions = _get_env_extensions(values, config.supported_extensions)
        config.auto_create_folders = _get_env_bool(values, ENV_AUTO_CREATE_FOLDERS, config.auto_create_folders)
        config.max_file_size_mb = _get_env_int(values, ENV_MAX_FILE_SIZE_MB, config.max_file_size_mb)
        config.request_timeout_seconds = _get_env_int(
            values,
            ENV_REQUEST_TIMEOUT_SECONDS,
            config.request_timeout_seconds,
        )
        config.validate()
        return config

    def validate(self) -> None:
        """Validate configuration values before use."""

        if not self.app_name.strip():
            raise ConfigurationError("app_name must not be empty")
        if not self.app_version.strip():
            raise ConfigurationError("app_version must not be empty")
        if not self.environment.strip():
            raise ConfigurationError("environment must not be empty")
        if self.max_file_size_mb <= 0:
            raise ConfigurationError("max_file_size_mb must be greater than zero")
        if self.request_timeout_seconds <= 0:
            raise ConfigurationError("request_timeout_seconds must be greater than zero")
        if not self.supported_extensions:
            raise ConfigurationError("supported_extensions must not be empty")

    def to_paths(self) -> AppPaths:
        """Build a path object rooted at the configured project directory."""

        return AppPaths.from_project_root(self.project_root, create=self.auto_create_folders)

    def resolve_path(self, path_value: Union[str, Path], *, root: Optional[Path] = None) -> Path:
        """Resolve a path relative to the configured project root."""

        candidate = Path(path_value).expanduser()
        if not candidate.is_absolute():
            base_root = root or self.project_root
            candidate = (base_root / candidate).resolve()
        return candidate.resolve()


def load_config(
    env: Optional[dict[str, str]] = None,
    *,
    project_root: Optional[Union[str, Path]] = None,
) -> AppConfig:
    """Load configuration from the environment and normalize the project root."""

    config = AppConfig.from_env(env)
    if project_root is not None:
        config.project_root = Path(project_root).expanduser().resolve()
    config.project_root.mkdir(parents=True, exist_ok=True)
    config.data_dir = config.resolve_path(config.data_dir, root=config.project_root)
    config.docs_dir = config.resolve_path(config.docs_dir, root=config.project_root)
    config.output_dir = config.resolve_path(config.output_dir, root=config.project_root)
    config.prompts_dir = config.resolve_path(config.prompts_dir, root=config.project_root)
    config.templates_dir = config.resolve_path(config.templates_dir, root=config.project_root)
    return config


def _get_env_str(values: dict[str, str], key: str, default: str) -> str:
    value = values.get(key)
    if value is None:
        return default
    return value.strip() or default


def _get_env_bool(values: dict[str, str], key: str, default: bool) -> bool:
    value = values.get(key)
    if value is None:
        return default
    if value.strip().lower() in {"1", "true", "yes", "on"}:
        return True
    if value.strip().lower() in {"0", "false", "no", "off"}:
        return False
    raise ConfigurationError(f"Invalid boolean value for {key}: {value}")


def _get_env_int(values: dict[str, str], key: str, default: int) -> int:
    value = values.get(key)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ConfigurationError(f"Invalid integer value for {key}: {value}") from exc


def _get_env_path(values: dict[str, str], key: str, default: Optional[Path] = None) -> Optional[Path]:
    value = values.get(key)
    if value is None:
        return default
    if not value.strip():
        return default
    return Path(value.strip()).expanduser()


def _get_env_extensions(values: dict[str, str], default: Sequence[str]) -> tuple[str, ...]:
    value = values.get(ENV_SUPPORTED_EXTENSIONS)
    if value is None:
        return tuple(default)
    entries = [entry.strip().lower() for entry in value.split(",") if entry.strip()]
    if not entries:
        raise ConfigurationError("supported_extensions cannot be empty")
    return tuple(entries)
