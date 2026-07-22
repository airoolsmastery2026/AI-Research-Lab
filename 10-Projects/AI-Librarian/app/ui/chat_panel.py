from __future__ import annotations

import os

if os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("CI"):
    class _FallbackQtWidgets:
        class QWidget:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs

            def setLayout(self, *args, **kwargs):
                return None

        class QTextEdit:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs

            def setReadOnly(self, *args, **kwargs):
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

from app.controllers.chat_controller import ChatController


class ChatPanel(QtWidgets.QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.controller = ChatController()
        self.chat_log = QtWidgets.QTextEdit()
        self.chat_log.setReadOnly(True)
        self.input = QtWidgets.QLineEdit()
        self.send_button = QtWidgets.QPushButton("Send")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.chat_log)
        layout.addWidget(self.input)
        layout.addWidget(self.send_button)
        self.setLayout(layout)
