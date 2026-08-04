from PySide6.QtCore import Qt, Signal

from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
)

class StepCard(QFrame):
    done_changed = Signal(int, bool)

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

        self.done_checkbox.toggled.connect(
            self.emit_done_changed
        )

    def emit_done_changed(self, checked):
        self.done_changed.emit(
            self.step_id,
            checked
        )