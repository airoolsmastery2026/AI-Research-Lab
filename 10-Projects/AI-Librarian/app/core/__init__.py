"""Core foundation package for AI Librarian."""

from .config import AppConfig, load_config
from .constants import (
    DEFAULT_APP_NAME,
    DEFAULT_APP_VERSION,
    DEFAULT_AUTO_CREATE_FOLDERS,
    DEFAULT_ENVIRONMENT,
    DEFAULT_LOG_LEVEL,
    DEFAULT_MAX_FILE_SIZE_MB,
    DEFAULT_REQUEST_TIMEOUT_SECONDS,
    DEFAULT_SUPPORTED_EXTENSIONS,
)
from .exceptions import (
    ConfigurationError,
    CoreError,
    FileSystemError,
    LoggingError,
    PathResolutionError,
)
from .logger import get_logger, setup_logging
from .paths import AppPaths

__all__ = [
    "AppConfig",
    "AppPaths",
    "ConfigurationError",
    "CoreError",
    "DEFAULT_APP_NAME",
    "DEFAULT_APP_VERSION",
    "DEFAULT_AUTO_CREATE_FOLDERS",
    "DEFAULT_ENVIRONMENT",
    "DEFAULT_LOG_LEVEL",
    "DEFAULT_MAX_FILE_SIZE_MB",
    "DEFAULT_REQUEST_TIMEOUT_SECONDS",
    "DEFAULT_SUPPORTED_EXTENSIONS",
    "FileSystemError",
    "LoggingError",
    "PathResolutionError",
    "get_logger",
    "load_config",
    "setup_logging",
]
