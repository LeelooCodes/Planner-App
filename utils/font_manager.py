import re

from PySide6.QtGui import (
    QFont,
    QFontDatabase,
)

from utils.paths import resource_path

class FontManager:
    SYSTEM_DEFAULT = "System Default"

    DEFAULT_TEXT_SIZE = "Default"

    TEXT_SIZE_SCALES = {
        "Small": 0.90,
        "Default": 1.0,
        "Large": 1.15,
        "Extra Large": 1.3,
    }

    FONT_FILE_SUFFIXES = {
        ".ttf",
        ".otf",
    }

    FONT_SIZE_PATTERN = re.compile(
        r"(font-size\s*:\s*)"
        r"(\d+(?:\.\d+)?)"
        r"(px|pt)"
        r"(\s*;)",
        re.IGNORECASE
    )

    def __init__(
            self,
            app,
            settings
    ):
        self.app = app
        self.settings = settings

        #Keep a copy of the OS's original application font.
        #This lets "system defaults" genuinely restore the original font.

        self.system_font = QFont(
            app.font()
        )

        self.bundled_families = []

        self.current_font_family = self.SYSTEM_DEFAULT

        self.current_text_size = self.DEFAULT_TEXT_SIZE

        self.load_bundled_fonts()

    def load_bundled_fonts(self):
        fonts_directory = resource_path(
            "assets/fonts"
        )

        if not fonts_directory.exists():
            self.bundled_families = []
            return

        loaded_families = set()

        for font_path in sorted(
            fonts_directory.rglob("*")
        ):
            if (
                font_path.suffix.lower()
                not in self.FONT_FILE_SUFFIXES
            ):
                continue

            font_id = (
                QFontDatabase
                .addApplicationFont(
                    str(font_path)
                )
            )

            if font_id == -1:
                continue

            families = (
                QFontDatabase
                .applicationFontFamilies(
                    font_id
                )
            )

            loaded_families.update(families)

        self.bundled_families = sorted(
            loaded_families,
            key=str.casefold
        )

    def get_available_fonts(self):
        all_families = sorted(
            set(
                QFontDatabase
                .families()
            ),
            key=str.casefold
        )

        bundled_set = set(
            self.bundled_families
        )

        installed_families = [
            family
            for family in all_families
            if family not in bundled_set
        ]

        return {
            "bundled": list(
                self.bundled_families
            ),
            "installed": installed_families,
        }

    def get_available_text_sizes(self):
        return list(
            self.TEXT_SIZE_SCALES.keys()
        )

    def get_system_font_family(self):
        return self.system_font.family()

    def get_current_font_family(self):
        return self.current_font_family

    def get_current_text_size(self):
        return self.current_text_size

    def get_text_size_scale(self, text_size):
        return self.TEXT_SIZE_SCALES.get(
            text_size,
            self.TEXT_SIZE_SCALES[
                self.DEFAULT_TEXT_SIZE
            ]
        )

    def is_font_available(self, font_family):
        if (
            font_family
            == self.SYSTEM_DEFAULT
        ):
            return True

        return (
            font_family
            in QFontDatabase.families()
        )

    def build_font(
            self,
            font_family,
            text_size
    ):
        font = QFont(
            self.system_font
        )

        if (
            font_family
            != self.SYSTEM_DEFAULT
        ):
            font.setFamily(
                font_family
            )

        base_size = (
            self.system_font
            .pointSizeF()
        )

        if base_size <= 0:
            base_size = 10.0

        scale = self.get_text_size_scale(
            text_size
        )

        font.setPointSizeF(
            base_size * scale
        )

        return font

    def apply_font(
            self,
            font_family,
            text_size,
            persist=True
    ):
        if not self.is_font_available(
            font_family
        ):
            font_family = (
                self.SYSTEM_DEFAULT
            )

        if (
            text_size
            not in self.TEXT_SIZE_SCALES
        ):
            text_size = (
                self.DEFAULT_TEXT_SIZE
            )

        font = self.build_font(
            font_family,
            text_size
        )

        self.app.setFont(
            font
        )

        self.current_font_family = (
            font_family
        )

        self.current_text_size = (
            text_size
        )

        if persist:
            self.settings.set_font_family(
                font_family
            )

            self.settings.set_font_size(
                text_size
            )

    def apply_saved_font(self):
        saved_font = (
            self.settings
            .get_font_family(
                self.SYSTEM_DEFAULT
            )
        )
        saved_size = (
            self.settings
            .get_font_size(
                self.DEFAULT_TEXT_SIZE
            )
        )

        if not self.is_font_available(
            saved_font
        ):
            saved_font = (
                self.SYSTEM_DEFAULT
            )

            self.settings.set_font_family(
                saved_font
            )

        if (
            saved_size
            not in self.TEXT_SIZE_SCALES
        ):
            saved_size = (
                self.DEFAULT_TEXT_SIZE
            )

            self.settings.set_font_size(
                saved_size
            )

        self.apply_font(
            saved_font,
            saved_size,
            persist=False
        )

    def scale_stylesheet(
            self,
            stylesheet
    ):
        scale = self.get_text_size_scale(
            self.current_text_size
        )

        if scale == 1.0:
            return stylesheet

        def replace_font_size(match):
            original_size = float(
                match.group(2)
            )

            scaled_size = max(
            1,
                round(
                    original_size
                    * scale
                )
            )

            return (
                f"{match.group(1)}"
                f"{scaled_size}"
                f"{match.group(3)}"
                f"{match.group(4)}"
            )

        return self.FONT_SIZE_PATTERN.sub(
            replace_font_size,
            stylesheet
        )
    