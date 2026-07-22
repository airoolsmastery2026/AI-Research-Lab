from __future__ import annotations

import os

from app.brain import BrainManager
from ._compat import ensure_qapplication

if os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("CI"):
    class _FallbackQtWidgets:
        class QStatusBar:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs
                self.message = ""

            def addWidget(self, *args, **kwargs):
                return None

        class QProgressBar:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs

            def setValue(self, *args, **kwargs):
                return None

    QtWidgets = _FallbackQtWidgets  # type: ignore[assignment]
else:
    from PySide6 import QtWidgets


class StatusBar(QtWidgets.QStatusBar):
    def __init__(self, parent=None, brain: BrainManager | None = None) -> None:
        ensure_qapplication()
        super().__init__(parent)
        self.brain = brain or BrainManager()
        self.message = ""

    def set_message(self, message: str) -> None:
        self.message = message
        self.showMessage(message)
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setValue(0)
        self.addWidget(self.progress_bar)
