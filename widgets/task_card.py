from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
)

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