import sys

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from database import PlannerDatabase


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

        task_layout.addWidget(self.add_task_button)

        self.task_list = QListWidget()

        self.task_list.setWordWrap(True)

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

            QListWidget::item {
                background-color: #f8fafc;
                color: #1e293b;
                border: 1px solid #d7dee8;
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 8px;
            }

            QListWidget::item:selected {
                background-color: #dbeafe;
                border: 1px solid #2563eb;
            }

            QListWidget::item:hover {
                background-color: #eff6ff;
            }
            """
        )

        self.load_tasks()

    def load_tasks(self):
        self.task_list.clear()

        tasks = self.database.get_tasks()

        for task in tasks:
            title = task["title"]
            status = task["display_status"]
            deadline = task["deadline"]
            dependency = task["dependency"]

            lines = [
                title,
                status
            ]

            if deadline:
                lines.append(
                    f"Deadline: {deadline}"
                )

            if dependency:
                lines.append(
                    f"Dependent on: {dependency}"
                )

            display_text = "\n".join(lines)

            item = QListWidgetItem(display_text)

            item.setData(
                Qt.ItemDataRole.UserRole,
                task["id"]
            )

            self.task_list.addItem(item)

        if self.task_list.count() > 0:
            self.task_list.setCurrentRow(0)

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

        for step in steps:
            done_text = "Done" if step["is_done"] else "Not done"

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

            self.step_list.addItem(item)

    def closeEvent(self, event):
        self.database.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = PlannerWindow()
    window.showMaximized()

    sys.exit(app.exec())