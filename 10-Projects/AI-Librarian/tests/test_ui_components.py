from app.ui.file_explorer import FileExplorer
from app.ui.library_panel import LibraryPanel
from app.ui.document_viewer import DocumentViewer
from app.ui.search_bar import SearchBar
from app.ui.import_wizards import ImportFolderWizard, ImportUSBWizard
from app.ui.progress_windows import OCRProgressWindow, BackgroundIndexProgress
from app.ui.settings import SettingsView
from app.ui.startup_wizard import StartupWizard
from app.ui.theme_manager import ThemeManager
from app.ui.notifications import NotificationCenter
from app.ui.status_bar import StatusBar


def test_ui_components_bootstrap_and_connect():
    brain = None
    explorer = FileExplorer(brain=brain)
    library = LibraryPanel(brain=brain)
    viewer = DocumentViewer(brain=brain)
    search = SearchBar(brain=brain)
    import_folder = ImportFolderWizard(brain=brain)
    import_usb = ImportUSBWizard(brain=brain)
    ocr = OCRProgressWindow(brain=brain)
    index = BackgroundIndexProgress(brain=brain)
    settings = SettingsView()
    wizard = StartupWizard(brain=brain)
    theme = ThemeManager()
    notifications = NotificationCenter()
    status = StatusBar(brain=brain)

    explorer.load_directory(".")
    library.refresh(".")
    viewer.show_document("README.md")
    search.search("ai")
    import_folder.run(".")
    import_usb.run("D:\\USB")
    ocr.start()
    index.start()
    notifications.notify("Ready", "UI ready")
    status.set_message("Ready")

    assert explorer is not None
    assert library is not None
    assert viewer is not None
    assert search is not None
    assert import_folder is not None
    assert import_usb is not None
    assert ocr is not None
    assert index is not None
    assert settings.dark_mode is False
    assert wizard is not None
    assert theme.current_theme == "light"
    assert notifications.unread_count() == 1
    assert status.message == "Ready"
