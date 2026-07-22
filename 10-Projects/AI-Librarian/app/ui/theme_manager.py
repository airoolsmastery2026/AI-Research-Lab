from __future__ import annotations

from ._compat import ensure_qapplication


class ThemeManager:
    def __init__(self) -> None:
        ensure_qapplication()
        self.current_theme = "light"

    def set_theme(self, theme: str) -> None:
        self.current_theme = theme
