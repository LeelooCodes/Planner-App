from PySide6.QtCore import QSettings


class AppSettings:
    THEME_KEY = "appearance/theme"

    def __init__(self):
        self.settings = QSettings(
            "PyPlanner",
            "PyPlanner"
        )

    def get_theme(self, default_theme):
        return self.settings.value(
            self.THEME_KEY,
            default_theme,
            type=str
        )

    def set_theme(self, theme_name):
        self.settings.setValue(
            self.THEME_KEY,
            theme_name
        )

        self.settings.sync()