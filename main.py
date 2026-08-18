import sys

from PySide6.QtCore import QDate, Qt, QSize

from PySide6.QtWidgets import (
    QAbstractItemView,
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
from dialogs.edit_task_dialog import EditTaskDialog
from themes.theme_manager import ThemeManager
from menus.app_menu_bar import AppMenuBar
from dialogs.settings_dialog import SettingsDialog


class PlannerWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.database = PlannerDatabase()

        self.pending_step_dependency = ""

        self.is_loading_steps = False
        self.is_loading_tasks = False

        self.setWindowTitle("Task Planner")

        self.app_menu_bar = AppMenuBar(self)

        self.setMenuBar(
            self.app_menu_bar
        )

        self.app_menu_bar.settings_requested.connect(
            self.on_settings_requested
        )

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

        self.task_list.setDragEnabled(True)
        self.task_list.setAcceptDrops(True)
        self.task_list.setDropIndicatorShown(True)
        self.task_list.setDragDropMode(
            QAbstractItemView.DragDropMode.InternalMove
        )
        self.task_list.setDefaultDropAction(
            Qt.DropAction.MoveAction
        )
        self.task_list.model().rowsMoved.connect(
            self.on_tasks_reordered
        )


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

        self.add_step_dependency_checkbox.setObjectName(
            "addStepDependencyCheckbox"
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

        self.step_list.setDragEnabled(
            True
        )

        self.step_list.setAcceptDrops(
            True
        )

        self.step_list.setDropIndicatorShown(
            True
        )

        self.step_list.setDragDropMode(
            QAbstractItemView.DragDropMode.InternalMove
        )

        self.step_list.setDefaultDropAction(
            Qt.DropAction.MoveAction
        )

        self.step_list.model().rowsMoved.connect(
            self.on_steps_reordered
        )

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

        self.load_tasks()

    def on_settings_requested(self):
        dialog = SettingsDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        selected_theme = dialog.get_selected_theme()

        print(
            f"Selected theme: {selected_theme}"
        )

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
        self.is_loading_tasks = True

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

            card.selected_requested.connect(
                self.select_task_by_id
            )

            card.dependency_resolved_changed.connect(
                self.on_task_dependency_resolved_changed
            )

            card.edit_requested.connect(
                self.on_task_edit_requested
            )

            card.delete_requested.connect(
                self.on_task_delete_requested
            )

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

        self.is_loading_tasks = False

    def on_tasks_reordered(
            self,
            parent,
            start,
            end,
            destination,
            row
    ):
        if self.is_loading_tasks:
            return

        ordered_task_ids = []

        for index in range(
            self.task_list.count()
        ):
            item = self.task_list.item(
                index
            )

            task_id = item.data(
                Qt.ItemDataRole.UserRole
            )

            ordered_task_ids.append(
                task_id
            )

        try:
            self.database.reorder_tasks(
                ordered_task_ids
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Unable to reorder tasks",
                str(error)
            )

            self.load_tasks()

    def on_task_dependency_resolved_changed(
            self,
            task_id,
            is_resolved
    ):
        try:
            self.database.set_task_dependency_resolved(
                task_id,
                is_resolved
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Unable to update dependency",
                str(error)
            )
            return

        self.load_tasks()
        self.select_task_by_id(
            task_id
        )

    def on_task_edit_requested(
            self,
            task_id
    ):
        task = self.database.get_task(
            task_id
        )

        if task is None:
            QMessageBox.warning(
                self,
                "Unable to edit task",
                "The selected task no longer exists."
            )
            return

        dialog = EditTaskDialog(
            task,
            self
        )

        if (
            dialog.exec()
            != QDialog.DialogCode.Accepted
        ):
            return

        task_data = dialog.get_task_data()

        try:
            self.database.update_task(
                task_id=task_id,
                title=task_data["title"],
                deadline=task_data["deadline"],
                dependency=task_data["dependency"]
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Unable to edit task",
                str(error)
            )
            return

        self.load_tasks()
        self.select_task_by_id(
            task_id
        )

    def on_task_delete_requested(
            self,
            task_id
    ):
        task = self.database.get_task(
            task_id
        )

        if task is None:
            QMessageBox.warning(
                self,
                "Unable to delete task",
                "The selected task no longer exists."
            )
            return

        confirmation = QMessageBox.question(
            self,
            "Delete task?",
            (
                "Are you sure you want to delete "
                "the task: "
                f"{task['title']}?\n\n"
                "All steps belonging to this task "
                "will also be deleted. \n\n"
                "This action cannot be undone."
            ),
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
            ),
            QMessageBox.StandardButton.No
        )

        if (
            confirmation
            != QMessageBox.StandardButton.Yes
        ):
            return

        try:
            self.database.delete_task(
                task_id
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Unable to delete task",
                str(error)
            )
            return

        self.load_tasks()

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
        self.is_loading_steps = True

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

            card.dependency_resolved_changed.connect(
                self.on_step_dependency_resolved_changed
            )

            card.edit_requested.connect(
                self.on_step_edit_requested
            )

            card.delete_requested.connect(
                self.on_step_delete_requested
            )

            estimated_height = max(
                card.sizeHint().height() + 12,
                72
            )

            item.setSizeHint(
                QSize(
                    0,
                    estimated_height
                )
            )

            self.step_list.addItem(item)

            self.step_list.setItemWidget(
                item,
                card
            )

        self.is_loading_steps = False

    def on_steps_reordered(
            self,
            parent,
            start,
            end,
            destination,
            row
    ):
        if self.is_loading_steps:
            return

        current_task_item = (
            self.task_list.currentItem()
        )

        if current_task_item is None:
            return

        task_id = current_task_item.data(
            Qt.ItemDataRole.UserRole
        )

        ordered_step_ids = []

        for index in range(
            self.step_list.count()
        ):
            item = self.step_list.item(
                index
            )

            step_id = item.data(
                Qt.ItemDataRole.UserRole
            )

            ordered_step_ids.append(
                step_id
            )

        try:
            self.database.reorder_steps(
                task_id,
                ordered_step_ids
            )

        except ValueError as error:
            QMessageBox.warning(
                self,
                "Unable to reorder steps",
                str(error)
            )

            self.load_steps(
                task_id
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

    def on_step_dependency_resolved_changed(
            self,
            step_id,
            is_resolved
    ):
        try:
            task_id = (
                self.database
                .set_step_dependency_resolved(
                    step_id,
                    is_resolved
                )
            )
        except ValueError as error:
            QMessageBox.warning(
                self,
                "Unable to update dependency",
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

    theme_manager = ThemeManager(
        app
    )

    theme_manager.apply_theme(
        ThemeManager.DEFAULT_THEME
    )

    window = PlannerWindow()
    window.showMaximized()

    sys.exit(app.exec())