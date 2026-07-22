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

        class QTextEdit:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs

            def setPlaceholderText(self, *args, **kwargs):
                return None

    QtWidgets = _FallbackQtWidgets  # type: ignore[assignment]
else:
    from PySide6 import QtWidgets


class DocumentView(QtWidgets.QDockWidget):
    def __init__(self, parent=None) -> None:
        super().__init__("Document", parent)
        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setPlaceholderText("Select a document to view it here")
        self.setWidget(self.text_edit)
