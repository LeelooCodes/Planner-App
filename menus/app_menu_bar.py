from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar

class AppMenuBar(QMenuBar):
    settings_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._build_menus()

    def _build_menus(self):
        settings_menu = self.addMenu("Settings")

        self.settings_action = QAction("Preferences...", self)
        self.settings_action.setMenuRole(
            QAction.MenuRole.PreferencesRole
        )

        self.settings_action.triggered.connect(
            self.settings_requested.emit
        )

        settings_menu.addAction(self.settings_action)