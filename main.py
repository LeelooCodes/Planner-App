import sys

from PySide6.QtCore import QDate, Qt, QSize

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStyleFactory,
    QVBoxLayout,
    QWidget,
)

from database import PlannerDatabase

from widgets.task_card import TaskCard
from widgets.step_card import StepCard

from dialogs.add_task_dialog import AddTaskDialog
from dialogs.dependency_dialog import DependencyDialog
from dialogs.edit_step_dialog import EditStepDialog


class PlannerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.database = PlannerDatabase()

        self.pending_step_dependency = ""

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

        step_entry_layout = QHBoxLayout()

        self.new_step_input = QLineEdit()

        self.new_step_input.setPlaceholderText(
            "Type a new step and press enter."
        )

        self.add_step_button = QPushButton( "Add")

        self.add_step_dependency_checkbox = QCheckBox(
            "Add dependency"
        )

        self.new_step_input.setEnabled(False)
        self.add_step_button.setEnabled(False)
        self.add_step_dependency_checkbox.setEnabled(False)

        

        

        step_entry_layout.addWidget(
            self.new_step_input,
            stretch=1
        )

        step_entry_layout.addWidget(
            self.add_step_dependency_checkbox
        )

        step_entry_layout.addWidget(
            self.add_step_button
        )

        step_layout.addLayout(
            step_entry_layout
        )

        self.new_step_input.returnPressed.connect(
            self.add_step_inline
        )

        self.add_step_button.clicked.connect(
            self.add_step_inline
        )

        self.add_step_dependency_checkbox.toggled.connect(
            self.on_add_step_dependency_toggled
        )


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

            QFrame#stepCard {
                background-color: #f8fafc;
                border: 1px solid #d7dee8;
                border-radius: 10px;
            }

            QCheckBox#stepCheckbox {
                spacing: 0px;
            }

            QCheckBox#stepCheckbox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #64748b;
                border-radius: 4px;
                background-color: #ffffff;
            }

            QCheckBox#stepCheckbox::indicator:hover {
                border: 2px solid #2563eb;
            }

            QCheckBox#stepCheckbox::indicator:checked {
                background-color: #2563eb;
                border: 2px solid #2563eb;
                image: url(assets/icons/check.svg);
            }


            QLabel#stepDependency {
                color: #9a3412;
                font-size: 13px;
            }

            QLabel#stepDescription {
                color: #0f172a;
                font-size: 15px;
                font-weight: 600;
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
                background-color: transparent;
                color: #1e293b;
                padding: 0px;
                margin-bottom: 8px;
            }

            QListWidget#stepList::item:selected {
                background-color: #dbeafe;
                border: 1px solid #2563eb;
                border-radius: 10px;
            }

            QListWidget#stepList::item:hover {
                background-color: #eff6ff;
                border-radius: 10px;
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

            QLineEdit {
                background-color: #ffffff;
                color: #0f172a;
                border: 1px solid #cbd5e1;
                border-radius: 8px;
                padding: 8px 10px;
            }

            QLineEdit:focus {
                border: 1px solid #2563eb;
            }

            QToolButton#stepEditButton,
            QToolButton#stepDeleteButton {
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 8px;
                padding: 4px;
            }

            QToolButton#stepEditButton:hover {
                background-color: #dbeafe;
                border: 1px solid #bfdbfe;
            }

            QToolButton#stepEditButton:pressed {
                background-color: #bfdbfe;
            }

            QToolButton#stepDeleteButton:hover {
                background-color: #fee2e2;
                border: 1px solid #fecaca;
            }

            QToolButton#stepDeleteButton:pressed {
                background-color: #fecaca
            }

            """
        )

        self.load_tasks()

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
        for row in range(
            self.task_list.count()
        ):
            item = self.task_list.item(row)

            item_task_id = item.data(
                Qt.ItemDataRole.UserRole
            )

            if item_task_id == task_id:
                self.task_list.setCurrentItem(item)
                self.task_list.scrollToItem(item)
                return

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

    def on_task_selected(self, current, previous):
        if current is None:
            self.new_step_input.setEnabled(False)
            self.add_step_button.setEnabled(False)
            self.add_step_dependency_checkbox.setEnabled(False)

            self.pending_step_dependency = ""

            self.add_step_dependency_checkbox.blockSignals(True)
            self.add_step_dependency_checkbox.setChecked(False)
            self.add_step_dependency_checkbox.blockSignals(False)
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

        self.new_step_input.setEnabled(True)
        self.add_step_button.setEnabled(True)
        self.add_step_dependency_checkbox.setEnabled(True)

        self.load_steps(task_id)

    def on_add_step_dependency_toggled(self, checked):
        if not checked:
            self.pending_step_dependency = ""
            return

        previous_dependency = self.pending_step_dependency

        dialog = DependencyDialog(
            parent=self,
            dependency=previous_dependency,
            title="Add step dependency"
        )

        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            self.pending_step_dependency = (
                dialog.get_dependency()
            )
            return

        # The dialog was cancelled or closed.
        #
        # Restore the state that existed before it opened.
        # If there was no previously saved dependency, the
        # checkbox should return to unchecked.

        if not previous_dependency:
            self.add_step_dependency_checkbox.blockSignals(True)
            self.add_step_dependency_checkbox.setChecked(False)
            self.add_step_dependency_checkbox.blockSignals(False)
        else:
            self.pending_step_dependency = previous_dependency

    def add_step_inline(self):

        current_task_item = self.task_list.currentItem()

        if current_task_item is None:
            QMessageBox.warning(
                self,
                "No task selected",
                "Please select a task before adding a step."
            )
            return

        description = self.new_step_input.text().strip()

        if not description:
            return

        task_id = current_task_item.data(
            Qt.ItemDataRole.UserRole
        )

        try:
            has_dependency = (
                self.add_step_dependency_checkbox.isChecked()
                and bool(self.pending_step_dependency)
            )

            self.database.add_step(
                task_id=task_id,
                description=description,
                has_dependency=has_dependency,
                dependency=self.pending_step_dependency
            )
        except ValueError as error:
            QMessageBox.warning(
                self,
                "Unable to add step",
                str(error)
            )
            return

        self.new_step_input.clear()

        self.pending_step_dependency = ""

        self.add_step_dependency_checkbox.blockSignals(True)
        self.add_step_dependency_checkbox.setChecked(False)
        self.add_step_dependency_checkbox.blockSignals(False)

        self.load_tasks()
        self.select_task_by_id(task_id)

        self.new_step_input.setFocus()

    def load_steps(self, task_id):
        self.step_list.clear()

        steps = self.database.get_steps(task_id)

        for step in steps:
            item = QListWidgetItem()

            item.setData(
                Qt.ItemDataRole.UserRole,
                step["id"]
            )

            card = StepCard(step)

            card.done_changed.connect(
                self.on_step_done_changed
            )

            card.edit_requested.connect(
                self.on_step_edit_requested
            )

            card.delete_requested.connect(
                self.on_step_delete_requested
            )

            item.setSizeHint(
                QSize(
                    0,
                    max(card.sizeHint().height(), 64)
                )
            )

            self.step_list.addItem(item)

            self.step_list.setItemWidget(
                item,
                card
            )

    def on_step_edit_requested(self, step_id):
        step = self.database.get_step(step_id)

        if step is None:
            QMessageBox.warning(
                self,
                "Unable to edit step",
                "The selected step no longer exists."
            )
            return

        dialog = EditStepDialog(
            step,
            self
        )

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        step_data = dialog.get_step_data()

        try:
            task_id = self.database.update_step(
                step_id=step_id,
                description=step_data["description"],
                has_dependency=(
                    step_data["has_dependency"]
                ),
                dependency=step_data["dependency"]
            )
        except ValueError as error:
            QMessageBox.warning(
                self,
                "Unable to edit step",
                str(error)
            )
            return

        self.load_tasks()
        self.select_task_by_id(task_id)
        self.load_steps(task_id)

    def on_step_delete_requested(self, step_id):
        step = self.database.get_step(step_id)

        if step is None:
            QMessageBox.warning(
                self,
                "Unable to delete step",
                "The selected step no longer exists."
            )
            return

        confirmation = QMessageBox.question(
            self,
            "Delete step?",
            (
                f"Are you sure you want to delete "
                f"the step:\n\n"
                f"“{step['description']}”?\n\n"
                f"This action cannot be undone."
            ),
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
            ),
            QMessageBox.StandardButton.No
        )

        if confirmation != QMessageBox.StandardButton.Yes:
            return

        try:
            task_id = self.database.delete_step(
                step_id
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Unable to delete step",
                str(error)
            )
            return

        self.load_tasks()
        self.select_task_by_id(task_id)
        self.load_steps(task_id)

    def on_step_done_changed(
            self,
            step_id,
            is_done
    ):
        try:
            task_id = self.database.set_step_done(
                step_id,
                is_done
            )
        except ValueError as error:
            QMessageBox.warning(
                self,
                "Unable to update step",
                str(error)
            )
            return

        self.load_tasks()
        self.select_task_by_id(task_id)
        self.load_steps(task_id)



    def closeEvent(self, event):
        self.database.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle(
        QStyleFactory.create("Fusion")
    )

    window = PlannerWindow()
    window.showMaximized()

    sys.exit(app.exec())