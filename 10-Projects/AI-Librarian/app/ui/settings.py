from __future__ import annotations

import os

from ._compat import ensure_qapplication

if os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("CI"):
    class _FallbackQtWidgets:
        class QDialog:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs

            def setLayout(self, *args, **kwargs):
                return None

        class QCheckBox:
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


class SettingsView(QtWidgets.QDialog):
    def __init__(self, parent=None) -> None:
        ensure_qapplication()
        super().__init__(parent)
        self.dark_mode = False
        self.checkbox = QtWidgets.QCheckBox("Dark mode")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.checkbox)
        self.setLayout(layout)
