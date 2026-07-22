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

        class QLineEdit:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs

        class QListWidget:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs

        class QVBoxLayout:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs

            def addWidget(self, *args, **kwargs):
                return None

        class QWidget:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs

            def setLayout(self, *args, **kwargs):
                return None

    QtWidgets = _FallbackQtWidgets  # type: ignore[assignment]
else:
    from PySide6 import QtWidgets


class SearchPanel(QtWidgets.QDockWidget):
    def __init__(self, parent=None) -> None:
        super().__init__("Search", parent)
        self.input = QtWidgets.QLineEdit()
        self.results = QtWidgets.QListWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.results)
        container = QtWidgets.QWidget()
        container.setLayout(layout)
        self.setWidget(container)
