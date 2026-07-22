"""Retry helpers for transient LLM provider failures."""

from __future__ import annotations

import time
from typing import Callable, TypeVar

from .errors import LLMProviderError, LLMTimeoutError

T = TypeVar("T")


def retry_with_backoff(func: Callable[[], T], max_retries: int = 3, base_delay: float = 0.25) -> T:
    """Retry a function for transient provider errors."""

    last_error: Exception | None = None
    for attempt in range(max_retries + 1):
        try:
            return func()
        except (LLMProviderError, LLMTimeoutError) as exc:
            last_error = exc
            if attempt >= max_retries:
                raise
            time.sleep(base_delay * (attempt + 1))

    if last_error is not None:
        raise last_error
    raise LLMProviderError("Retry loop failed")
