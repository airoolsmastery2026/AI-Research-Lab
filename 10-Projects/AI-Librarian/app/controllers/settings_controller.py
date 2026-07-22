from __future__ import annotations

from app.ui.settings import SettingsView


class SettingsController:
    def __init__(self, view: SettingsView | None = None) -> None:
        self.view = view or SettingsView()

    def toggle_dark_mode(self, enabled: bool) -> None:
        self.view.dark_mode = enabled
