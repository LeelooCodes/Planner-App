from PySide6.QtCore import QDate, Qt

from PySide6.QtWidgets import (
    QCheckBox,
    QDateEdit,
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

class EditTaskDialog(QDialog):
    def __init__(self, task, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Edit task")
        self.setModal(True)
        self.setMinimumWidth(460)

        self.pending_dependency = (
            task["dependency"]
        )

        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        #Task name

        self.title_input = QLineEdit()

        self.title_input.setText(
            task["title"]
        )

        self.title_input.setPlaceholderText(
            "Enter the task name"
        )

        form_layout.addRow(
            "Task name:",
            self.title_input
        )

        #Deadline

        self.has_deadline_checkbox = QCheckBox(
            "This task has a deadline"
        )

        has_deadline = bool(
            task["deadline"]
        )

        self.has_deadline_checkbox.setChecked(
            has_deadline
        )

        form_layout.addRow(
            "",
            self.has_deadline_checkbox
        )

        self.deadline_input = QDateEdit()

        self.deadline_input.setCalendarPopup(
            True
        )

        self.deadline_input.setDisplayFormat(
            "yyyy-MM-dd"
        )

        if has_deadline:
            saved_deadline = QDate.fromString(
                task["deadline"],
                "yyyy-MM-dd"
            )

            if saved_deadline.isValid():
                self.deadline_input.setDate(
                    saved_deadline
                )

            else:
                self.deadline_input.setDate(
                    QDate.currentDate()
                )

        else:
            self.deadline_input.setDate(
                QDate.currentDate()
            )

        self.deadline_input.setEnabled(
            has_deadline
        )

        form_layout.addRow(
            "Deadline:",
            self.deadline_input
        )


        #Dependency

        self.has_dependency_checkbox = QCheckBox(
            "This task has a dependency"
        )

        has_dependency = bool(
            task["dependency"]
        )

        self.has_dependency_checkbox.setChecked(
            has_dependency
        )

        form_layout.addRow(
            "",
            self.has_dependency_checkbox
        )

        self.dependency_value_label = QLabel()

        self.dependency_value_label.setTextFormat(
            Qt.TextFormat.PlainText
        )

        self.dependency_value_label.setWordWrap(
            True
        )

        form_layout.addRow(
            "Dependency",
            self.dependency_value_label
        )

        self.edit_dependency_button = QPushButton()

        form_layout.addRow(
            "",
            self.edit_dependency_button
        )


        #Save / Cancel

        main_layout.addLayout(
            form_layout
        )

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

        main_layout.addWidget(
            button_box
        )


        #Connections

        self.has_deadline_checkbox.toggled.connect(
            self.deadline_input.setEnabled
        )

        self.has_dependency_checkbox.toggled.connect(
            self.on_dependency_toggled
        )

        self.edit_dependency_button.clicked.connect(
            self.open_dependency_dialog
        )

        self.update_dependency_display()

        self.title_input.setFocus()
        self.title_input.selectAll()


    def on_dependency_toggled(
            self,
            checked
    ):
        if checked:
            if not self.pending_dependency:
                self.open_dependency_dialog()
        else:
            self.pending_dependency = ""

        self.update_dependency_display()

    def open_dependency_dialog(self):
        if not self.has_dependency_checkbox.isChecked():
            return

        previous_dependency = (
            self.pending_dependency
        )

        dialog = DependencyDialog(
            parent=self,
            dependency=previous_dependency,
            title="Edit task dependency"
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

        if (
            has_dependency
            and self.pending_dependency
        ):
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
        title = (
            self.title_input.text().strip()
        )

        if not title:
            QMessageBox.warning(
                self,
                "Missing Task Name",
                "Please enter a task name."
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

    def get_task_data(self):
        if self.has_deadline_checkbox.isChecked():
            deadline = (
                self.deadline_input
                .date()
                .toString("yyyy-MM-dd")
            )

        else:
            deadline = ""

        has_dependency = (
            self.has_dependency_checkbox.isChecked()
        )

        dependency = (
            self.pending_dependency
            if has_dependency
            else ""
        )

        return{
            "title": (
                self.title_input.text().strip()
            ),
            "deadline": deadline,
            "dependency": dependency
        }


