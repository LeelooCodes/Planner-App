from PySide6.QtCore import QSettings


class AppSettings:
    THEME_KEY = "appearance/theme"
    FONT_FAMILY_KEY = "appearance/font_family"
    FONT_SIZE_KEY = "appearance/font_size"

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

    def get_font_family(self, default_font):
        return self.settings.value(
            self.FONT_FAMILY_KEY,
            default_font,
            type=str
        )

    def set_font_family(self, font_family):
        self.settings.setValue(
            self.FONT_FAMILY_KEY,
            font_family
        )

        self.settings.sync()

    def get_font_size(self, default_size):
        return self.settings.value(
            self.FONT_SIZE_KEY,
            default_size,
            type=int
        )

    def set_font_size(self, font_size):
        self.settings.setValue(
            self.FONT_SIZE_KEY,
            font_size
        )

        self.settings.sync()

    