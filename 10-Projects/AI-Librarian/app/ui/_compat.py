from __future__ import annotations

import os


class _FallbackQApplication:
    _instance = None

    def __init__(self, *args, **kwargs) -> None:
        self._args = args
        self._kwargs = kwargs
        type(self)._instance = self

    @classmethod
    def instance(cls):
        return cls._instance


if os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("CI"):
    QApplication = _FallbackQApplication
else:
    try:
        from PySide6.QtWidgets import QApplication as _QApplication
    except Exception:  # pragma: no cover - fallback for missing Qt runtime
        QApplication = _FallbackQApplication
    else:
        QApplication = _QApplication


def ensure_qapplication():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app
