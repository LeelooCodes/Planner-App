LIGHT_THEME = """
    QMainWindow {
        background-color: #eef2f7;
    }

    QWidget {
        color: #334155;
    }

    QDialog, QMessageBox {
        background-color: #f8fafc;
        color: #334155;
    }

    QDialog QLabel,
    QMessageBox QLabel {
        color: #334155;
    }

    QDialog QCheckBox {
        color: #334155;
        spacing: 7px;
    }

    QDialog QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border: 2px solid #64748b;
        border-radius: 4px;
        background-color: #ffffff;
    }

    QDialog QCheckBox::indicator:hover {
        border: 2px solid #2563eb;
    }

    QDialog QCheckBox::indicator:checked {
        background-color: #2563eb;
        border: 2px solid #2563eb;
        image: url(assets/icons/check.svg);
    }

    QDialog QLineEdit,
    QDialog QDateEdit {
        background-color: #ffffff;
        color: #0f172a;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 8px 10px;
    }

    QDialog QLineEdit::disabled,
    QDialog QDateEdit::diabled{
        background-color: #e2e8f0;
        color: #64748b;
        border: 1px solid #cbd5e1;
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

    QCheckBox#addStepDependencyCheckbox{
        color: #334155;
        font-size: 14px;
        spacing: 7px;
    }

    QCheckBox#addStepDependencyCheckbox::indicator {
        width: 18px;
        height: 18px;
        border: 2px solid #64748b;
        border-radius: 4px;
        background-color: #ffffff;
    }

    QCheckBox#addStepDependencyCheckbox::indicator:hover {
        border: 2px solid #2563eb;
    }

    QCheckBox#addStepDependencyCheckbox::indicator:checked {
        background-color: #2563eb;
        border: 2px solid #2563eb;
        image: url(assets/icons/check.svg);
    }

    QCheckBox#stepDependencyResolvedCheckbox,
    QCheckBox#taskDependencyResolvedCheckbox {
        spacing: 0px;
    }

    QCheckBox#stepDependencyResolvedCheckbox::indicator,
    QCheckBox#taskDependencyResolvedCheckbox::indicator {
        width: 16px;
        height: 16px;
        border: 2px solid #64748b;
        border-radius: 4px;
        background-color: #ffffff;
    }

    QCheckBox#stepDependencyResolvedCheckbox::indicator:hover,
    QCheckBox#taskDependencyResolvedCheckbox::indicator:hover {
        border: 2px solid #2563eb;
    }

    QCheckBox#stepDependencyResolvedCheckbox::indicator:checked,
    QCheckBox#taskDependencyResolvedCheckbox::indicator:checked {
        background-color: #2563eb;
        border: 2px solid #2563eb;
        image: url(assets/icons/check.svg);
    }

    QLabel#stepDependencyText {
        color: #9a3412;
        font-size: 13px;
    }

            
    QLabel#taskDependencyText {
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

    QListWidget#stepList::drop-indicator {
        border: 10px solid #2563eb;
    }

    QListWidget#taskList::drop-indicator {
        border: 10px solid #2563eb;
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

    QToolButton#taskEditButton,
    QToolButton#taskDeleteButton {
        background-color: transparent;
        border: 1px solid transparent;
        border-radius: 8px;
        padding: 4px;
    }

    QToolButton#taskEditButton:hover {
        background-color: #dbeafe;
        border: 1px solid #bfdbfe;
    }

    QToolButton#taskEditButton:pressed {
        background-color: #bfdbfe;
    }

    QToolButton#taskDeleteButton:hover {
        background-color: #fee2e2;
        border: 1px solid #fecaca;
    }

    QToolButton#taskDeleteButton:pressed {
        background-color: #fecaca;
    }

    """