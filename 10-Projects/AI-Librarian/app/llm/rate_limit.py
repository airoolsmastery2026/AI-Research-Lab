"""Basic rate limiting for LLM requests."""

from __future__ import annotations

import time
from collections import deque
from threading import Lock


class RateLimiter:
    """A simple token-bucket-style limiter based on request count."""

    def __init__(self, requests_per_minute: int) -> None:
        self.requests_per_minute = requests_per_minute
        self._timestamps: deque[float] = deque()
        self._lock = Lock()

    def acquire(self) -> None:
        """Block until a request slot is available."""

        with self._lock:
            now = time.time()
            window_start = now - 60.0
            while self._timestamps and self._timestamps[0] < window_start:
                self._timestamps.popleft()
            if len(self._timestamps) >= self.requests_per_minute:
                sleep_for = 61.0 - (now - self._timestamps[0])
                time.sleep(max(0.0, sleep_for))
                return self.acquire()
            self._timestamps.append(now)
