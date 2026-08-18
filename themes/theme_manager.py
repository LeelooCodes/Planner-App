from themes.light import LIGHT_THEME

class ThemeManager:
    DEFAULT_THEME = "Light"

    def __init__(self, app):
        self.app = app

        self.themes = {
            "Light": LIGHT_THEME,
        }

        self.current_theme = None

    def get_available_themes(self):
        return list(
            self.themes.keys()
        )

    def apply_theme(self, theme_name):
        if theme_name not in self.themes:
            raise ValueError(
                f"Unknown theme: {theme_name}"
            )

        stylesheet = self.themes[
            theme_name
        ]

        self.app.setStyleSheet(
            stylesheet
        )

        self.current_theme = theme_name

    def get_current_theme(self):
        return self.current_theme