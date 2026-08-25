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
    selected_requested = Signal(int)
    done_changed = Signal(int, bool)

    dependency_resolved_changed = Signal(int, bool)
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

        self.done_checkbox.setMinimumSize(
            22,
            22
        )

        content_layout = QVBoxLayout()

        content_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        content_layout.setSpacing(6)

        step_row = QHBoxLayout()

        step_row.setContentsMargins(
            0,
            0,
            0,
            0
        )

        step_row.setSpacing(10)

        step_row.setAlignment(
            Qt.AlignmentFlag.AlignVCenter
        )

        step_row.addWidget(
            self.done_checkbox,
            alignment=Qt.AlignmentFlag.AlignVCenter
        )

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

        step_row.addWidget(
            description_label,
            stretch=1,
            alignment=Qt.AlignmentFlag.AlignVCenter
        )

        content_layout.addLayout(
            step_row
        )

        if step ["has_dependency"]:
            dependency_row = QHBoxLayout()

            dependency_row.setContentsMargins(
                28,
                0,
                0,
                0
            )

            dependency_row.setSpacing(7)

            self.dependency_resolved_checkbox = QCheckBox()

            self.dependency_resolved_checkbox.setObjectName(
                "stepDependencyResolvedCheckbox"
            )

            self.dependency_resolved_checkbox.setChecked(
                step["dependency_resolved"]
            )

            self.dependency_resolved_checkbox.setToolTip(
                "Mark this dependency as resolved."
            )

            self.dependency_resolved_checkbox.setFixedSize(
                20,
                20
            )

            dependency_text_label = QLabel(
                f"Waiting for: {step['dependency']}"
            )

            dependency_text_label.setObjectName(
                "stepDependencyText"
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

            content_layout.addLayout(
                dependency_row
            )

        outer_layout.addLayout(
            content_layout,
            stretch=1
        )

        outer_layout.setAlignment(
            content_layout,
            Qt.AlignmentFlag.AlignVCenter
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

        if step["has_dependency"]:
            self.dependency_resolved_checkbox.toggled.connect(
                self.emit_dependency_resolved_changed
            )

        self.edit_button.clicked.connect(
            self.emit_edit_requested
        )

        self.delete_button.clicked.connect(
            self.emit_delete_requested
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
                self.step_id
            )

        super().mousePressEvent(event)

    def emit_done_changed(self, checked):
        self.done_changed.emit(
            self.step_id,
            checked
        )

    def emit_dependency_resolved_changed(
            self,
            checked
    ):
        self.dependency_resolved_changed.emit(
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