"""Desktop UI package for AI Librarian."""

from .main_window import MainWindow
from .settings import SettingsView
from .file_explorer import FileExplorer
from .library_panel import LibraryPanel
from .document_viewer import DocumentViewer
from .search_bar import SearchBar
from .import_wizards import ImportFolderWizard, ImportUSBWizard
from .progress_windows import OCRProgressWindow, BackgroundIndexProgress
from .startup_wizard import StartupWizard
from .theme_manager import ThemeManager
from .notifications import NotificationCenter
from .status_bar import StatusBar

__all__ = [
    "MainWindow",
    "SettingsView",
    "FileExplorer",
    "LibraryPanel",
    "DocumentViewer",
    "SearchBar",
    "ImportFolderWizard",
    "ImportUSBWizard",
    "OCRProgressWindow",
    "BackgroundIndexProgress",
    "StartupWizard",
    "ThemeManager",
    "NotificationCenter",
    "StatusBar",
]
