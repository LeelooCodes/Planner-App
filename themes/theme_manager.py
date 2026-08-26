from themes.light import LIGHT_THEME
from themes.dark import DARK_THEME
from themes.pink import PINK_THEME
from themes.purple import PURPLE_THEME

from utils.paths import resource_path

class ThemeManager:
    DEFAULT_THEME = "Light"

    def __init__(self, app, settings):
        self.app = app
        self.settings = settings

        self.themes = {
            "Light": LIGHT_THEME,
            "Dark": DARK_THEME,
            "Pink": PINK_THEME,
            "Purple": PURPLE_THEME,
        }

        self.current_theme = None

    def get_available_themes(self):
        return list(
            self.themes.keys()
        )

    def apply_theme(self, theme_name, persist = True):
        if theme_name not in self.themes:
            raise ValueError(
                f"Unknown theme: {theme_name}"
            )

        stylesheet = self.themes[
            theme_name
        ].replace(
            "assets/icons/check.svg",
            resource_path(
                "assets/icons/check.svg"
            ).as_posix()
        )

        self.app.setStyleSheet(
            stylesheet
        )

        self.current_theme = theme_name

        if persist:
            self.settings.set_theme(
                theme_name
            )

    def apply_saved_theme(self):
        saved_theme = self.settings.get_theme(
            self.DEFAULT_THEME
        )

        if saved_theme not in self.themes:
            saved_theme = self.DEFAULT_THEME

            self.settings.set_theme(
                saved_theme
            )

        self.apply_theme(
            saved_theme,
            persist=False
        )

    def get_current_theme(self):
        return self.current_theme
