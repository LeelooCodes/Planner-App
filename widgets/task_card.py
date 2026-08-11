from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
)

class TaskCard(QFrame):
    selected_requested = Signal(int)
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
            QIcon("assets/icons/edit.svg")
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
            QIcon("assets/icons/delete.svg")
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

        self.edit_button.clicked.connect(
            self.emit_edit_requested
        )

        self.delete_button.clicked.connect(
            self.emit_delete_requested
        )

    def emit_edit_requested(self):
        self.edit_requested.emit(
            self.task_id
        )

    def emit_delete_requested(self):
        self.delete_requested.emit(
            self.task_id
        )

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