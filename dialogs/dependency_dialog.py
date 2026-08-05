from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)

class DependencyDialog(QDialog):
    def __init__(
        self,
        parent=None,
        dependency="",
        title="Add dependency"
    ):
        super().__init__(parent)

        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(440)

        self._allow_empty_close = False

        main_layout = QVBoxLayout(self)

        instruction_label = QLabel(
            "Enter dependency."
        )

        instruction_label.setWordWrap(True)

        main_layout.addWidget(instruction_label)

        self.dependency_input = QLineEdit()

        self.dependency_input.setPlaceholderText(
            "For example: Waiting for finance"
        )

        self.dependency_input.setText(
            dependency
        )

        main_layout.addWidget(
            self.dependency_input
        )

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )

        self.button_box.accepted.connect(
            self.validate_and_accept
        )

        self.button_box.rejected.connect(
            self.attempt_close
        )

        main_layout.addWidget(
            self.button_box
        )

        self.dependency_input.returnPressed.connect(
            self.validate_and_accept
        )

        self.dependency_input.setFocus()
        self.dependency_input.selectAll()

    def validate_and_accept(self):
        dependency = (
            self.dependency_input
            .text()
            .strip()
        )

        if not dependency:
            QMessageBox.warning(
                self,
                "Missing dependency",
                "Please enter a dependency before saving."
            )
            return

        self.accept()

    def attempt_close(self):
        dependency = (
            self.dependency_input
            .text()
            .strip()
        )

        if dependency:
            self.reject()
            return

        should_close = QMessageBox.question(
            self,
            "Close without dependency?",
            (
                "No dependency has been entered. \n\n"
                "Are you sure you want to close "
                "without adding one?"
            ),
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
            ),
            QMessageBox.StandardButton.No
        )

        if should_close == QMessageBox.StandardButton.Yes:
            self._allow_empty_close = True
            self.reject()

    def closeEvent(self, event):
        dependency = (
            self.dependency_input
            .text()
            .strip()
        )

        if dependency or self._allow_empty_close:
            event.accept()
            return

        should_close = QMessageBox.question(
            self,
            "Close without dependency?",
            (
                "No dependency has been entered. \n\n"
                "Are you sure you want to close "
                "without adding one?"
            ),
            (
                QMessageBox.StandardButton.Yes
                | QMessageBox.StandardButton.No
            ),
            QMessageBox.StandardButton.No
        )

        if should_close == QMessageBox.StandardButton.Yes:
            self._allow_empty_close = True
            event.accept()
        else:
            event.ignore()

    def get_dependency(self):
        return (
            self.dependency_input
            .text()
            .strip()
        )

if __name__ == "__main__":
    import sys

    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    dialog = DependencyDialog()

    result = dialog.exec()

    if result == QDialog.DialogCode.Accepted:
        print(
            "Dependency: ",
            dialog.get_dependency()
        )
    else:
        print("Dialog cancelled.")

    sys.exit(0)