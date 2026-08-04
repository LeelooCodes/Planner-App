from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QLabel,
    QVBoxLayout,
)

class StepCard(QFrame):
    done_changed = Signal(int, bool)

    def __init__(self, step):
        super().__init__()

        self.step_id = step["id"]

        self.setObjectName("stepCard")

        card_layout = QVBoxLayout(self)

        card_layout.setContentsMargins(
            12,
            10,
            12,
            10
        )

        card_layout.setSpacing(6)

        self.done_checkbox = QCheckBox(
            step["description"]
        )

        self.done_checkbox.setObjectName(
            "stepCheckbox"
        )

        self.done_checkbox.setChecked(
            step["is_done"]
        )

        self.done_checkbox.setToolTip(
            "Mark this step as done"
        )

        card_layout.addWidget(
            self.done_checkbox
        )

        if step["has_dependency"]:
            dependency_label = QLabel(
                f"Dependent on: {step['dependency']}"
            )

            dependency_label.setObjectName(
                "stepDependency"
            )

            dependency_label.setWordWrap(True)

            dependency_label.setContentsMargins(
                32,
                0,
                0,
                0
            )

            card_layout.addWidget(
                dependency_label
            )

        self.done_checkbox.toggled.connect(
            self.emit_done_changed
        )
    

    def emit_done_changed(self, checked):
        self.done_changed.emit(
            self.step_id,
            checked
        )