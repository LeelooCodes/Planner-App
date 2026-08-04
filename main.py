import sys

from PySide6.QtCore import QDate, Qt, QSize

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from database import PlannerDatabase

class TaskCard(QFrame):
    def __init__(self, task):
        super().__init__()

        self.task_id = task["id"]

        self.setObjectName("taskCard")

        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents, 
            True
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )

        card_layout = QVBoxLayout(self)

        card_layout.setContentsMargins(
            14,
            12,
            14,
            12
        )

        card_layout.setSpacing(8)

        title_label = QLabel(task["title"])

        title_label.setObjectName("taskCardTitle")
        title_label.setWordWrap(True)

        card_layout.addWidget(title_label)

        status_row = QHBoxLayout()

        status_row.setContentsMargins(
            0,
            0,
            0,
            0
        )

        status_label = QLabel(
            task["display_status"]
        )

        status_label.setObjectName("statusBadge")

        self.apply_status_style(
            status_label,
            task["status"]
        )

        status_row.addWidget(status_label)

        status_row.addStretch()

        card_layout.addLayout(status_row)

        details = []

        if task["deadline"]:
            details.append(
                f"Deadline: {task['deadline']}"
            )

        if task["dependency"]:
            details.append(
                f"Dependent on: {task['dependency']}"
            )

        if details:
            details_label = QLabel(
                "\n".join(details)
            )

            details_label.setObjectName(
                "taskCardDetails"
            )

            details_label.setWordWrap(True)

            card_layout.addWidget(details_label)

    def apply_status_style(
            self,
            label,
            status
    ):
        styles = {
            "TBD": (
                "#475569",
                "#e2e8f0"
            ),
            "WIP": (
                "#1d4ed8",
                "#dbeafe"
            ),
            "Awaiting": (
                "#9a3412",
                "#ffedd5"
            ),
            "Completed": (
                "#166534",
                "#dcfce7"
            )
        }

        text_colour, background_colour = (
            styles.get(
                status,
                styles["TBD"]
            )
        )

        label.setStyleSheet(
            f"""
            QLabel {{
                color: {text_colour};
                background-color: {background_colour};
                border-radius: 8px;
                padding: 4px 8px;
                font-weight: 600;
            }}
            """
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


class PlannerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.database = PlannerDatabase()

        self.setWindowTitle("Task Planner")

        central_widget = QWidget()

        main_layout = QVBoxLayout(central_widget)

        main_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        main_layout.setSpacing(16)

        self.setCentralWidget(central_widget)

        app_title = QLabel("Task Planner")

        app_title.setObjectName("appTitle")

        main_layout.addWidget(app_title)

        self.main_splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        main_layout.addWidget(
            self.main_splitter,
            stretch=1
        )

        task_panel = QFrame()

        task_panel.setObjectName("panel")

        task_layout = QVBoxLayout(task_panel)

        task_layout.setContentsMargins(
            16,
            16,
            16,
            16
        )

        task_layout.setSpacing(12)

        self.task_heading = QLabel("Tasks")

        self.task_heading.setObjectName("sectionTitle")

        task_layout.addWidget(self.task_heading)

        self.add_task_button = QPushButton("Add task")

        self.add_task_button.clicked.connect(
            self.open_add_task_dialog
        )

        task_layout.addWidget(self.add_task_button)

        self.task_list = QListWidget()
        self.task_list.setObjectName("taskList")

        self.task_list.setWordWrap(True)
        self.task_list.setUniformItemSizes(False)


        task_layout.addWidget(
            self.task_list,
            stretch=1
        )

        self.task_list.currentItemChanged.connect(
            self.on_task_selected
        )

        self.main_splitter.addWidget(task_panel)

        step_panel = QFrame()

        step_panel.setObjectName("panel")

        step_layout = QVBoxLayout(step_panel)

        step_layout.setContentsMargins(
            16,
            16,
            16,
            16
        )

        step_layout.setSpacing(12)

        self.step_heading = QLabel(
            "Select a task to view its steps."
        )

        self.step_heading.setObjectName("sectionTitle")

        self.step_heading.setWordWrap(True)

        step_layout.addWidget(self.step_heading)

        add_step_button = QPushButton("Add step")

        step_layout.addWidget(add_step_button)

        self.step_list = QListWidget()
        self.step_list.setObjectName("stepList")

        

        self.step_list.setWordWrap(True)

        step_layout.addWidget(
            self.step_list,
            stretch=1
        )

        self.main_splitter.addWidget(step_panel)

        self.main_splitter.setStretchFactor(0, 1)
        self.main_splitter.setStretchFactor(1, 2)

        self.main_splitter.setSizes(
            [400, 800]
        )

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #eef2f7;
            }

            QLabel#appTitle {
                color: #1e293b;
                font-size: 28px;
                font-weight: bold;
            }

            QLabel#sectionTitle {
                color: #334155;
                font-size: 18px;
                font-weight: 600;
            }

            QFrame#panel {
                background-color: #ffffff;
                border: 1px solid #d7dee8;
                border-radius: 12px;
            }

            QLabel {
                color: #334155;
            }

            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px;
            }

            QPushButton:hover {
                background-color: #1d4ed8;
            }

            QPushButton:pressed {
                background-color: #1e40af;
            }

            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }

            QListWidget#taskList::item {
            background-color: transparent;
            border: none;
            padding: 0px;
            margin-bottom: 8px;
            }

            QListWidget#taskList::item:selected{
            background-color: #dbeafe;
            border: 1px solid #2563eb;
            border-radius: 10px;
            }

            QListWidget#taskList::item:hover{
            background-color: #eff6ff;
            border-radius: 10px;
            }

            QListWidget#stepList {
            background-color: transparent;
            color: #1e293b;
            }

            QListWidget#stepList::item {
            background-color: #f8fafc;
            color: #1e293b;
            border: 1px solid #d7dee8;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 8px;
            }

            QListWidget#stepList::item:selected {
            background-color: #dbeafe;
            color: #1e293b;
            border: 1px solid #2563eb;
            }

            QListWidget#stepList::item:hover {
            background-color: #eff6ff;
            color: #1e293b;
            }

            QFrame#taskCard {
            background-color: #f8fafc;
            border: 1px solid #d7dee8;
            border-radius: 10px;
            }

            QLabel#taskCardTitle {
            color: #0f172a;
            font-size: 16px;
            font-weight: 700;
            }

            QLabel#taskCardDetails {
            color: #64748b;
            font-size: 13px;
            }
            """
        )

        self.load_tasks()


    def load_tasks(self):
        selected_task_id = None

        current_item = self.task_list.currentItem()

        if current_item is not None:
            selected_task_id = current_item.data(
                Qt.ItemDataRole.UserRole
            )

        self.task_list.clear()

        tasks = self.database.get_tasks()

        item_to_select = None

        for task in tasks:
            item = QListWidgetItem()

            item.setData(
                Qt.ItemDataRole.UserRole,
                task["id"]
            )

            card = TaskCard(task)

            estimated_height = max(
                card.sizeHint().height(),
                85
            )

            item.setSizeHint(
                QSize(
                    0,
                    estimated_height
                )
            )

            self.task_list.addItem(item)

            self.task_list.setItemWidget(
                item,
                card
            )

            if task["id"] == selected_task_id:
                item_to_select = item

        if item_to_select is not None:
            self.task_list.setCurrentItem(
                item_to_select
            )
        elif self.task_list.count() > 0:
            self.task_list.setCurrentRow(0)

    def open_add_task_dialog(self):
        dialog = AddTaskDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        task_data = dialog.get_task_data()

        try:
            new_task_id = self.database.add_task(
                title=task_data["title"],
                deadline=task_data["deadline"],
                dependency=task_data["dependency"]
            )
        except ValueError as error:
            QMessageBox.warning(
                self,
                "Unable to add task",
                str(error)
            )
            return

        self.load_tasks()
        self.select_task_by_id(new_task_id)

    def select_task_by_id(self, task_id):
        for row in range(self.task_list.count()):
            item = self.task_list.item(row)

            item_task_id = item.data(
                Qt.ItemDataRole.UserRole
            )

            if item_task_id == task_id:
                self.task_list.setCurrentItem(item)
                self.task_list.scrollToItem(item)
                return

    def on_task_selected(self, current, previous):
        if current is None:
            self.step_heading.setText(
                "Select a task to view its steps."
            )

            self.step_list.clear()
            return

        task_id = current.data(
            Qt.ItemDataRole.UserRole
        )

        task = self.database.get_task(task_id)

        if task is  None:
            self.step_heading.setText(
                "Select a task to view its steps."
            )

            self.step_list.clear()
            return

        self.step_heading.setText(
            f"Steps for: {task['title']}"
        )

        self.load_steps(task_id)

    def load_steps(self, task_id):
        self.step_list.clear()

        steps = self.database.get_steps(task_id)

        print("Selected task ID: ", task_id)
        print("Steps returned: ", len(steps))
        print(steps)

        for step in steps:
            done_text = (
                "Done" 
                if step["is_done"] 
                else "Not done"
            )

            lines = [
                step["description"],
                done_text
            ]

            if step["has_dependency"]:
                lines.append(
                    f"Dependent on: {step['dependency']}"
                )

            display_text = "\n".join(lines)

            item = QListWidgetItem(display_text)

            item.setData(
                Qt.ItemDataRole.UserRole,
                step["id"]
            )

            item.setSizeHint(
                QSize(
                    0,
                    80
                )
            )

            self.step_list.addItem(item)

    def closeEvent(self, event):
        self.database.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = PlannerWindow()
    window.showMaximized()

    sys.exit(app.exec())