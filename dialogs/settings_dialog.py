from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QVBoxLayout,
)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setMinimumWidth(420)

        main_layout = QVBoxLayout(self)

        heading = QLabel("Appearance")
        heading.setObjectName("settingsSectionTitle")

        main_layout.addWidget(heading)

        form_layout = QFormLayout()

        self.theme_combo = QComboBox()
        self.theme_combo.setObjectName(
            "themeSelector"
        )

        self.theme_combo.addItem(
            "Light"
        )

        form_layout.addRow(
            "Theme:",
            self.theme_combo
        )

        main_layout.addLayout(
            form_layout
        )

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
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

    def get_selected_theme(self):
        return self.theme_combo.currentText()