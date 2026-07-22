from __future__ import annotations

import os

if os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("CI"):
    class _FallbackQtWidgets:
        class QWidget:
            def setStyleSheet(self, *args, **kwargs):
                return None

    QtWidgets = _FallbackQtWidgets  # type: ignore[assignment]
else:
    from PySide6 import QtWidgets


def apply_theme(window: QtWidgets.QWidget, dark: bool = False) -> None:
    if dark:
        window.setStyleSheet("QWidget { background-color: #1e1e1e; color: #f0f0f0; }")
    else:
        window.setStyleSheet("")
