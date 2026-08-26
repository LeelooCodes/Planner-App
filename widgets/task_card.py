from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon

from utils.paths import resource_path

from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
)

class TaskCard(QFrame):
    selected_requested = Signal(int)
    dependency_resolved_changed = Signal(int, bool)
    edit_requested = Signal(int)
    delete_requested = Signal(int)

    def __init__(self, task):
        super().__init__()

        self.task_id = task["id"]

        self.setObjectName("taskCard")

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

        title_row = QHBoxLayout()

        title_row.setContentsMargins(
            0,
            0,
            0,
            0
        )

        title_row.setSpacing(8)

        title_label = QLabel(
            task["title"]
        )

        title_label.setObjectName(
            "taskCardTitle"
        )

        title_label.setWordWrap(True)

        title_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )

        title_row.addWidget(
            title_label,
            stretch=1
        )

        self.edit_button = QToolButton()

        self.edit_button.setObjectName(
            "taskEditButton"
        )

        self.edit_button.setIcon(
            QIcon(
                str(
                    resource_path(
                        "assets/icons/edit.svg"
                    )
                )
            )
        )

        self.edit_button.setIconSize(
            QSize(20, 20)
        )

        self.edit_button.setFixedSize(
            32,
            32
        )

        self.edit_button.setToolTip(
            "Edit this task"
        )

        self.edit_button.setAccessibleName(
            "Edit task"
        )

        self.delete_button = QToolButton()

        self.delete_button.setObjectName(
            "taskDeleteButton"
        )

        self.delete_button.setIcon(
            QIcon(
                str(
                    resource_path(
                        "assets/icons/delete.svg"
                    )
                )
            )
        )

        self.delete_button.setIconSize(
            QSize(20, 20)
        )

        self.delete_button.setFixedSize(
            32,
            32
        )

        self.delete_button.setToolTip(
            "Delete this task"
        )

        self.delete_button.setAccessibleName(
            "Delete task"
        )

        title_row.addWidget(
            self.edit_button,
            alignment=Qt.AlignmentFlag.AlignTop
        )

        title_row.addWidget(
            self.delete_button,
            alignment=Qt.AlignmentFlag.AlignTop
        )

        card_layout.addLayout(
            title_row
        )

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

        if details:
            details_label = QLabel(
                "\n".join(details)
            )

            details_label.setObjectName(
                "taskCardDetails"
            )

            details_label.setWordWrap(True)

            card_layout.addWidget(details_label)

        if task["dependency"]:
            dependency_row = QHBoxLayout()

            dependency_row.setContentsMargins(
                0,
                0,
                0,
                0
            )

            dependency_row.setSpacing(7)

            self.dependency_resolved_checkbox = QCheckBox()

            self.dependency_resolved_checkbox.setObjectName(
                "taskDependencyResolvedCheckbox"
            )

            self.dependency_resolved_checkbox.setChecked(
                task["dependency_resolved"]
            )

            self.dependency_resolved_checkbox.setToolTip(
                "Mark this dependency as resolved"
            )

            self.dependency_resolved_checkbox.setFixedSize(
                20,
                20
            )

            dependency_text_label = QLabel(
                f"Waiting for: {task['dependency']}"
            )

            dependency_text_label.setObjectName(
                "taskDependencyText"
            )

            dependency_text_label.setWordWrap(True)

            dependency_text_label.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Minimum
            )

            dependency_row.addWidget(
                self.dependency_resolved_checkbox,
                alignment=Qt.AlignmentFlag.AlignVCenter
            )

            dependency_row.addWidget(
                dependency_text_label,
                stretch=1,
                alignment=Qt.AlignmentFlag.AlignVCenter
            )

            card_layout.addLayout(
                dependency_row
            )

        if task["dependency"]:
            self.dependency_resolved_checkbox.toggled.connect(
                self.emit_dependency_resolved_changed
            )

        self.edit_button.clicked.connect(
            self.emit_edit_requested
        )

        self.delete_button.clicked.connect(
            self.emit_delete_requested
        )

    def emit_dependency_resolved_changed(
            self,
            checked
    ):
        self.dependency_resolved_changed.emit(
            self.task_id,
            checked
        )

    def emit_edit_requested(self):
        self.edit_requested.emit(
            self.task_id
        )

    def emit_delete_requested(self):
        self.delete_requested.emit(
            self.task_id
        )

    def set_selected(self, selected):
        self.setProperty(
            "selected",
            selected
        )

        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.selected_requested.emit(
                self.task_id
            )

        super().mousePressEvent(event)

    def apply_status_style(
            self,
            label,
            status
    ):
        label.setProperty(
            "status",
            status
        )

        label.style().unpolish(
            label
        )

        label.style().polish(
            label
        )

        label.update()
