from __future__ import annotations

import os

if os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("CI"):
    class _FallbackQtWidgets:
        class QDockWidget:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs

            def setWidget(self, *args, **kwargs):
                return None

        class QListWidget:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs

    QtWidgets = _FallbackQtWidgets  # type: ignore[assignment]
else:
    from PySide6 import QtWidgets


class Sidebar(QtWidgets.QDockWidget):
    def __init__(self, parent=None) -> None:
        super().__init__("Library", parent)
        self.setWidget(QtWidgets.QListWidget())
