from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from dialogs.dependency_dialog import DependencyDialog

class EditStepDialog(QDialog):
    def __init__(self, step, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Edit step")
        self.setModal(True)
        self.setMinimumWidth(460)

        self.pending_dependency = step["dependency"]

        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.description_input = QLineEdit()

        self.description_input.setText(
            step["description"]
        )

        self.description_input.setPlaceholderText(
            "Enter the step name"
        )

        form_layout.addRow(
            "Step name:",
            self.description_input
        )

        self.has_dependency_checkbox = QCheckBox(
            "This step has a dependency"
        )

        self.has_dependency_checkbox.setChecked(
            step["has_dependency"]
        )

        form_layout.addRow(
            "",
            self.has_dependency_checkbox
        )

        self.dependency_value_label = QLabel()
        self.dependency_value_label.setWordWrap(True)

        form_layout.addRow(
            "Dependency:",
            self.dependency_value_label
        )

        self.edit_dependency_button = QPushButton(
            "Set dependency"
        )

        form_layout.addRow(
            "",
            self.edit_dependency_button
        )

        main_layout.addLayout(form_layout)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        button_box.accepted.connect(
            self.validate_and_accept
        )

        button_box.rejected.connect(
            self.reject
        )

        main_layout.addWidget(button_box)

        self.has_dependency_checkbox.toggled.connect(
            self.on_dependency_toggled
        )

        self.edit_dependency_button.clicked.connect(
            self.open_dependency_dialog
        )

        self.update_dependency_display()

        self.description_input.setFocus()
        self.description_input.selectAll()

    def on_dependency_toggled(self, checked):
        self.edit_dependency_button.setEnabled(
            checked
        )

        if checked:
            if not self.pending_dependency:
                self.open_dependency_dialog()
            else:
                self.pending_dependency= ""

            self.update_dependency_display()

    def open_dependency_dialog(self):
        if not self.has_dependency_checkbox.isChecked():
            return

        previous_dependency = self.pending_dependency

        dialog = DependencyDialog(
            parent=self,
            dependency=previous_dependency,
            title="Edit step dependency"
        )

        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.pending_dependency = (
                dialog.get_dependency()
            )
        elif not previous_dependency:
            self.has_dependency_checkbox.blockSignals(
                True
            )

            self.has_dependency_checkbox.setChecked(
                False
            )

            self.has_dependency_checkbox.blockSignals(
                False
            )

            self.pending_dependency = ""

        self.update_dependency_display()

    def update_dependency_display(self):
        has_dependency = (
            self.has_dependency_checkbox.isChecked()
        )

        self.edit_dependency_button.setEnabled(
            has_dependency
        )

        if has_dependency and self.pending_dependency:
            self.dependency_value_label.setText(
                self.pending_dependency
            )

            self.edit_dependency_button.setText(
                "Change dependency"
            )
        else:
            self.dependency_value_label.setText(
                "None"
            )

            self.edit_dependency_button.setText(
                "Set dependency"
            )

    def validate_and_accept(self):
        description = (
            self.description_input.text().strip()
        )

        if not description:
            QMessageBox.warning(
                self,
                "Missing step name",
                "Please enter a step name."
            )
            return

        if (
            self.has_dependency_checkbox.isChecked()
            and not self.pending_dependency
        ):
            QMessageBox.warning(
                self,
                "Missing dependency",
                "Please enter a dependency."
            )
            return
        
        self.accept()

    def get_step_data(self):
        has_dependency = (
            self.has_dependency_checkbox.isChecked()
        )

        return {
            "description": (
                self.description_input.text().strip()
            ),
            "has_dependency": has_dependency,
            "dependency": (
                self.pending_dependency
                if has_dependency
                else ""
            )
        }