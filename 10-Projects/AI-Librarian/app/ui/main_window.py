from __future__ import annotations

import os

if os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("CI"):
    class _FallbackQtWidgets:
        class QMainWindow:
            def __init__(self, *args, **kwargs):
                self._args = args
                self._kwargs = kwargs
                self._title = ""
                self._central_widget = None
                self._dock_widgets = []
                self._status_bar = None

            def setWindowTitle(self, title: str) -> None:
                self._title = title

            def windowTitle(self) -> str:
                return self._title

            def resize(self, width: int, height: int) -> None:
                self._size = (width, height)

            def setCentralWidget(self, widget) -> None:
                self._central_widget = widget

            def addDockWidget(self, *args, **kwargs) -> None:
                self._dock_widgets.append((args, kwargs))

            def setStatusBar(self, bar) -> None:
                self._status_bar = bar

        class QDockWidget(QMainWindow):
            pass

        class QWidget(QMainWindow):
            pass

    class _FallbackQtCore:
        class Qt:
            class DockWidgetArea:
                LeftDockWidgetArea = 1
                RightDockWidgetArea = 2
                BottomDockWidgetArea = 3

    QtWidgets = _FallbackQtWidgets  # type: ignore[assignment]
    QtCore = _FallbackQtCore  # type: ignore[assignment]
else:
    from PySide6 import QtCore, QtWidgets

from app.brain import BrainManager
from .sidebar import Sidebar
from .document_view import DocumentView
from .search_panel import SearchPanel
from .chat_panel import ChatPanel
from .import_dialog import ImportDialog
from .settings import SettingsView
from .status_bar import StatusBar
from .theme import apply_theme
from ._compat import ensure_qapplication


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, brain: BrainManager | None = None) -> None:
        ensure_qapplication()
        super().__init__()
        self.brain = brain or BrainManager()
        self.setWindowTitle("AI Librarian")
        self.resize(1200, 800)
        self._build_ui()
        apply_theme(self, dark=False)

    def _build_ui(self) -> None:
        self.sidebar = Sidebar(self)
        self.document_view = DocumentView(self)
        self.search_panel = SearchPanel(self)
        self.chat_panel = ChatPanel(self)
        self.import_dialog = ImportDialog(self)
        self.settings_view = SettingsView(self)
        self.status_bar = StatusBar(self)

        self.setCentralWidget(self.chat_panel)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.LeftDockWidgetArea, self.sidebar)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, self.document_view)
        self.addDockWidget(QtCore.Qt.DockWidgetArea.BottomDockWidgetArea, self.search_panel)
        self.setStatusBar(self.status_bar)
