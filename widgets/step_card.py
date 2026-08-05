from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon

from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
)

class StepCard(QFrame):
    done_changed = Signal(int, bool)
    edit_requested = Signal(int)
    delete_requested = Signal(int)

    def __init__(self, step):
        super().__init__()

        self.step_id = step["id"]

        self.setObjectName("stepCard")

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )

        outer_layout = QHBoxLayout(self)

        outer_layout.setContentsMargins(
            12,
            10,
            12,
            10
        )

        outer_layout.setSpacing(10)

        self.done_checkbox = QCheckBox()

        self.done_checkbox.setObjectName(
            "stepCheckbox"
        )

        self.done_checkbox.setChecked(
            step["is_done"]
        )

        self.done_checkbox.setToolTip(
            "Mark this step as done?"
        )

        self.done_checkbox.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )

        outer_layout.addWidget(
            self.done_checkbox,
            alignment=Qt.AlignmentFlag.AlignTop
        )

        text_layout = QVBoxLayout()

        text_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        text_layout.setSpacing(4)

        description_label = QLabel(
            step["description"]
        )

        description_label.setObjectName(
            "stepDescription"
        )

        description_label.setWordWrap(True)

        description_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )

        text_layout.addWidget(
            description_label
        )

        if step["has_dependency"]:
            dependency_label = QLabel(
                f"Dependent on: {step['dependency']}"
            )

            dependency_label.setObjectName(
                "stepDependency"
            )

            dependency_label.setWordWrap(True)

            dependency_label.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Minimum
            )

            text_layout.addWidget(
                dependency_label
            )

        outer_layout.addLayout(
            text_layout,
            stretch=1
        )

        action_layout = QHBoxLayout()

        action_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        action_layout.setSpacing(4)

        self.edit_button = QToolButton()

        self.edit_button.setObjectName(
            "stepEditButton"
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
            "Edit this step"
        )

        self.edit_button.setAccessibleName(
            "Edit step"
        )

        self.delete_button = QToolButton()

        self.delete_button.setObjectName(
            "stepDeleteButton"
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
            "Delete this step"
        )

        self.delete_button.setAccessibleName(
            "Delete step"
        )

        action_layout.addWidget(
            self.edit_button
        )

        action_layout.addWidget(
            self.delete_button
        )

        outer_layout.addLayout(
            action_layout
        )

        self.done_checkbox.toggled.connect(
            self.emit_done_changed
        )

        self.edit_button.clicked.connect(
            self.emit_edit_requested
        )

        self.delete_button.clicked.connect(
            self.emit_delete_requested
        )

    def emit_done_changed(self, checked):
        self.done_changed.emit(
            self.step_id,
            checked
        )

    def emit_edit_requested(self):
        self.edit_requested.emit(
            self.step_id
        )

    def emit_delete_requested(self):
        self.delete_requested.emit(
            self.step_id
        )