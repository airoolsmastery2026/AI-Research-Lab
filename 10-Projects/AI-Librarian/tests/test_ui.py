from app.ui.main_window import MainWindow
from app.ui.settings import SettingsView
from app.controllers.chat_controller import ChatController
from app.controllers.import_controller import ImportController


def test_main_window_initializes():
    window = MainWindow()
    assert window.windowTitle() == "AI Librarian"


def test_settings_view_default_state():
    view = SettingsView()
    assert view.dark_mode is False


def test_controllers_exist_and_connect():
    import_controller = ImportController()
    chat_controller = ChatController()

    assert import_controller is not None
    assert chat_controller is not None
