from themes.light import (
    LIGHT_THEME,
    LIGHT_ICON_COLORS,
    )
from themes.dark import (
    DARK_THEME,
    DARK_ICON_COLORS,
)
from themes.pink import (
    PINK_THEME,
    PINK_ICON_COLORS,
)
from themes.purple import (
    PURPLE_THEME,
    PURPLE_ICON_COLORS,
)

from utils.paths import resource_path
from utils.themed_icon import refresh_themed_icons

class ThemeManager:
    DEFAULT_THEME = "Light"

    def __init__(self, app, settings):
        self.app = app
        self.settings = settings

        self.themes = {
            "Light": {
                "stylesheet": LIGHT_THEME,
                "icon_colors": LIGHT_ICON_COLORS,
            },
            "Dark": {
                "stylesheet": DARK_THEME,
                "icon_colors": DARK_ICON_COLORS,
            },
            "Pink": {
                "stylesheet": PINK_THEME,
                "icon_colors": PINK_ICON_COLORS,
            },
            "Purple":  {
                "stylesheet": PURPLE_THEME,
                "icon_colors": PURPLE_ICON_COLORS,
            },
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

        theme = self.themes[
            theme_name
        ]

        stylesheet = theme[
            "stylesheet"
        ].replace(
            "assets/icons/check.svg",
            resource_path(
                "assets/icons/check.svg"
            ).as_posix()
        )

        self.app.setProperty(
            "themeIconColors",
            theme["icon_colors"]
        )

        self.app.setStyleSheet(
            stylesheet
        )

        refresh_themed_icons()

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
