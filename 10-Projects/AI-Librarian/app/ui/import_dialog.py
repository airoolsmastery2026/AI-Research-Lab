from __future__ import annotations

import os

if os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("CI"):
    class _FallbackQtWidgets:
        class QDialog:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs

            def setWindowTitle(self, *args, **kwargs):
                return None

        class QLineEdit:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs

        class QPushButton:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs

        class QVBoxLayout:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs

            def addWidget(self, *args, **kwargs):
                return None

    QtWidgets = _FallbackQtWidgets  # type: ignore[assignment]
else:
    from PySide6 import QtWidgets


class ImportDialog(QtWidgets.QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Import")
        self.path_input = QtWidgets.QLineEdit()
        self.import_button = QtWidgets.QPushButton("Import")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.path_input)
        layout.addWidget(self.import_button)
        self.setLayout(layout)
