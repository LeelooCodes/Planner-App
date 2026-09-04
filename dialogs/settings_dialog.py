from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QVBoxLayout,
)


class SettingsDialog(QDialog):
    def __init__(
            self,
            available_themes,
            current_theme,
            font_manager,
            parent=None
    ):
        super().__init__(parent)

        self.font_manager = font_manager

        self.setWindowTitle(
            "Preferences"
        )

        self.setModal(
            True
        )

        self.setMinimumWidth(
            520
        )

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setSpacing(
            16
        )

        # =========================================================
        # APPEARANCE
        # =========================================================

        heading = QLabel(
            "Appearance"
        )

        heading.setObjectName(
            "settingsSectionTitle"
        )

        main_layout.addWidget(
            heading
        )

        form_layout = QFormLayout()

        form_layout.setSpacing(
            12
        )

        # =========================================================
        # THEME
        # =========================================================

        self.theme_combo = QComboBox()

        self.theme_combo.setObjectName(
            "themeSelector"
        )

        self.theme_combo.addItems(
            available_themes
        )

        theme_index = (
            self.theme_combo.findText(
                current_theme
            )
        )

        if theme_index >= 0:
            self.theme_combo.setCurrentIndex(
                theme_index
            )

        form_layout.addRow(
            "Theme:",
            self.theme_combo
        )

        # =========================================================
        # FONT
        # =========================================================

        self.font_combo = QComboBox()

        self.font_combo.setObjectName(
            "fontSelector"
        )

        font_groups = (
            self.font_manager
            .get_available_fonts()
        )

        bundled_fonts = (
            font_groups["bundled"]
        )

        installed_fonts = (
            font_groups["installed"]
        )

        system_font_family = (
            self.font_manager
            .get_system_font_family()
        )

        self.font_combo.addItem(
            (
                "System Default "
                f"({system_font_family})"
            ),
            self.font_manager.SYSTEM_DEFAULT
        )

        if bundled_fonts or installed_fonts:
            self.font_combo.insertSeparator(
                self.font_combo.count()
            )

        for font_family in bundled_fonts:
            self.font_combo.addItem(
                f"PyPlanner • {font_family}",
                font_family
            )

        if bundled_fonts and installed_fonts:
            self.font_combo.insertSeparator(
                self.font_combo.count()
            )

        for font_family in installed_fonts:
            self.font_combo.addItem(
                font_family,
                font_family
            )

        current_font_family = (
            self.font_manager
            .get_current_font_family()
        )

        for index in range(
            self.font_combo.count()
        ):
            if (
                self.font_combo.itemData(
                    index
                )
                == current_font_family
            ):
                self.font_combo.setCurrentIndex(
                    index
                )

                break

        form_layout.addRow(
            "Font:",
            self.font_combo
        )

        # =========================================================
        # TEXT SIZE
        # =========================================================

        self.text_size_combo = QComboBox()

        self.text_size_combo.setObjectName(
            "textSizeSelector"
        )

        available_text_sizes = (
            self.font_manager
            .get_available_text_sizes()
        )

        for text_size in available_text_sizes:
            scale = (
                self.font_manager
                .get_text_size_scale(
                    text_size
                )
            )

            percentage = round(
                scale * 100
            )

            self.text_size_combo.addItem(
                (
                    f"{text_size} "
                    f"({percentage}%)"
                ),
                text_size
            )

        current_text_size = (
            self.font_manager
            .get_current_text_size()
        )

        for index in range(
            self.text_size_combo.count()
        ):
            if (
                self.text_size_combo.itemData(
                    index
                )
                == current_text_size
            ):
                (
                    self.text_size_combo
                    .setCurrentIndex(
                        index
                    )
                )

                break

        form_layout.addRow(
            "Text size:",
            self.text_size_combo
        )

        main_layout.addLayout(
            form_layout
        )

        # =========================================================
        # PREVIEW
        # =========================================================

        preview_heading = QLabel(
            "Preview"
        )

        preview_heading.setObjectName(
            "settingsPreviewTitle"
        )

        main_layout.addWidget(
            preview_heading
        )

        self.preview_label = QLabel(
            (
                "Plan something wonderful ✨\n\n"
                "The quick brown fox jumps over "
                "the lazy dog.\n"
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ\n"
                "abcdefghijklmnopqrstuvwxyz\n"
                "0123456789\n\n"
                "Español: mañana  •  "
                "עברית: שלום"
            )
        )

        self.preview_label.setObjectName(
            "fontPreview"
        )

        self.preview_label.setTextFormat(
            Qt.TextFormat.PlainText
        )

        self.preview_label.setWordWrap(
            True
        )

        self.preview_label.setAlignment(
            (
                Qt.AlignmentFlag.AlignLeft
                | Qt.AlignmentFlag.AlignVCenter
            )
        )

        self.preview_label.setContentsMargins(
            14,
            14,
            14,
            14
        )

        self.preview_label.setMinimumHeight(
            180
        )

        main_layout.addWidget(
            self.preview_label
        )

        # =========================================================
        # SAVE / CANCEL
        # =========================================================

        self.button_box = QDialogButtonBox(
            (
                QDialogButtonBox
                .StandardButton
                .Save
            )
            |
            (
                QDialogButtonBox
                .StandardButton
                .Cancel
            )
        )

        self.button_box.accepted.connect(
            self.accept
        )

        self.button_box.rejected.connect(
            self.reject
        )

        main_layout.addWidget(
            self.button_box
        )

        # =========================================================
        # LIVE PREVIEW
        # =========================================================

        self.font_combo.currentIndexChanged.connect(
            self.update_preview
        )

        (
            self.text_size_combo
            .currentIndexChanged
            .connect(
                self.update_preview
            )
        )

        self.update_preview()

    def update_preview(
            self,
            *_args
    ):
        font_family = (
            self.get_selected_font_family()
        )

        text_size = (
            self.get_selected_text_size()
        )

        if (
            font_family is None
            or text_size is None
        ):
            return

        preview_font = (
            self.font_manager
            .build_font(
                font_family,
                text_size
            )
        )

        self.preview_label.setFont(
            preview_font
        )

    def get_selected_theme(self):
        return self.theme_combo.currentText()

    def get_selected_font_family(self):
        return self.font_combo.currentData()

    def get_selected_text_size(self):
        return (
            self.text_size_combo
            .currentData()
        )