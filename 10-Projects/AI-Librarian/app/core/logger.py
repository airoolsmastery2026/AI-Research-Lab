"""Structured logging helpers for the application."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from .constants import DEFAULT_LOG_DATE_FORMAT, DEFAULT_LOG_FORMAT, LOGGER_NAME
from .exceptions import LoggingError


def get_logger(
    name: Optional[str] = None,
    *,
    level: Optional[str] = None,
    log_file: Optional[Path | str] = None,
    propagate: bool = False,
) -> logging.Logger:
    """Create or retrieve a configured logger instance."""

    logger_name = name or LOGGER_NAME
    logger = logging.getLogger(logger_name)

    if logger.handlers:
        logger.propagate = propagate
        logger.setLevel(_coerce_log_level(level))
        return logger

    level_name = (level or "INFO").upper()
    logger.setLevel(_coerce_log_level(level_name))
    logger.propagate = propagate

    formatter = logging.Formatter(DEFAULT_LOG_FORMAT, DEFAULT_LOG_DATE_FORMAT)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_file is not None:
        log_path = Path(log_file).expanduser()
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_path,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def setup_logging(
    *,
    name: Optional[str] = None,
    level: Optional[str] = None,
    log_file: Optional[Path | str] = None,
) -> logging.Logger:
    """Compatibility helper for configuring application logging."""

    return get_logger(name=name, level=level, log_file=log_file, propagate=False)


def _coerce_log_level(level: Optional[str]) -> int:
    if level is None:
        return logging.INFO

    normalized = str(level).upper()
    mapping = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "NOTSET": logging.NOTSET,
    }
    if normalized not in mapping:
        raise LoggingError(f"Unsupported log level: {level}")
    return mapping[normalized]
