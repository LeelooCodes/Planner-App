from PySide6.QtCore import QDate

from PySide6.QtWidgets import (
    QCheckBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add task")
        self.setModal(True)
        self.setMinimumWidth(460)

        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText(
            "Enter the task name"
        )

        form_layout.addRow(
            "Task name: ",
            self.title_input
        )

        self.has_deadline_checkbox = QCheckBox(
            "This task has a deadline"
        )

        form_layout.addRow(
            "",
            self.has_deadline_checkbox
        )

        self.deadline_input = QDateEdit()
        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setDate(
            QDate.currentDate()
        )
        self.deadline_input.setDisplayFormat(
            "yyyy-MM-dd"
        )
        self.deadline_input.setEnabled(False)

        form_layout.addRow(
            "Deadline: ",
            self.deadline_input
        )

        self.has_dependency_checkbox = QCheckBox(
            "This task has a dependency"
        )

        form_layout.addRow(
            "",
            self.has_dependency_checkbox
        )

        self.dependency_input = QLineEdit()
        self.dependency_input.setPlaceholderText(
            "Who or what does this task depend on?"
        )
        self.dependency_input.setEnabled(False)

        form_layout.addRow(
            "Dependency: ",
            self.dependency_input
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

        self.has_deadline_checkbox.toggled.connect(
            self.deadline_input.setEnabled
        )

        self.has_dependency_checkbox.toggled.connect(
            self.dependency_input.setEnabled
        )

    def validate_and_accept(self):
        title = self.title_input.text().strip()

        if not title:
            QMessageBox.warning(
                self,
                "Missing task name",
                "Please enter a task name."
            )
            return
        if (
            self.has_dependency_checkbox.isChecked()
            and not self.dependency_input.text().strip()
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
            deadline = self.deadline_input.date().toString(
                "yyyy-MM-dd"
            )
        else:
            deadline = ""

        if self.has_dependency_checkbox.isChecked():
            dependency = self.dependency_input.text().strip()
        else:
            dependency = ""

        return {
            "title": self.title_input.text().strip(),
            "deadline": deadline,
            "dependency": dependency
        }