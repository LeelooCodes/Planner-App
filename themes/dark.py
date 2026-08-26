DARK_ICON_COLORS = {
    "edit": {
        "fill": "#1e3a5f",
        "stroke": "#60a5fa",
    },
    "delete": {
        "fill": "#451a1a",
        "stroke": "#f87171",
    },
}

DARK_THEME = """

    /* =========================================================
       GLOBAL APPLICATION

       #0f172a - Main application background
       #e2e8f0 - Default foreground / text colour
       ========================================================= */

    QMainWindow {
        background-color: #0f172a;
    }

    QWidget {
        color: #e2e8f0;
    }


    /* =========================================================
       APPLICATION MENUS

       #111827 - Menu bar background
       #111827 - Dropdown menu background
       #e2e8f0 - Normal menu text
       #f8fafc - Active / selected menu text
       #334155 - Menu bar border
       #334155 - Dropdown menu border
       #1e293b - Hovered menu item background
       #1e3a5f - Pressed menu bar item background
       #1e3a5f - Selected dropdown menu item background
       #334155 - Menu separators
       ========================================================= */

    QMenuBar {
        background-color: #111827;
        color: #e2e8f0;
        border-bottom: 1px solid #334155;
        padding: 4px 8px;
        spacing: 4px;
    }

    QMenuBar::item {
        background-color: transparent;
        color: #e2e8f0;
        padding: 6px 10px;
        border-radius: 6px;
    }

    QMenuBar::item:selected {
        background-color: #1e293b;
        color: #f8fafc;
    }

    QMenuBar::item:pressed {
        background-color: #1e3a5f;
        color: #f8fafc;
    }

    QMenu {
        background-color: #111827;
        color: #e2e8f0;
        border: 1px solid #334155;
        padding: 4px;
    }

    QMenu::item {
        background-color: transparent;
        color: #e2e8f0;
        padding: 7px 28px 7px 10px;
        border-radius: 5px;
    }

    QMenu::item:selected {
        background-color: #1e3a5f;
        color: #f8fafc;
    }

    QMenu::separator {
        height: 1px;
        background-color: #334155;
        margin: 4px 8px;
    }


    /* =========================================================
       GENERAL LABELS AND HEADINGS

       #e2e8f0 - Standard application text
       #f8fafc - Strong / primary title text
       ========================================================= */

    QLabel {
        color: #e2e8f0;
    }

    QLabel#appTitle {
        color: #f8fafc;
        font-size: 28px;
        font-weight: bold;
    }

    QLabel#sectionTitle {
        color: #e2e8f0;
        font-size: 18px;
        font-weight: 600;
    }


    /* =========================================================
       MAIN PANELS

       #111827 - Panel background
       #334155 - Panel border
       ========================================================= */

    QFrame#panel {
        background-color: #111827;
        border: 1px solid #334155;
        border-radius: 12px;
    }


    /* =========================================================
       GENERAL PUSH BUTTONS

       #3b82f6 - Normal primary button background
       #2563eb - Hovered primary button background
       #1d4ed8 - Pressed primary button background
       #ffffff - Button text
       ========================================================= */

    QPushButton {
        background-color: #3b82f6;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 8px;
    }

    QPushButton:hover {
        background-color: #2563eb;
    }

    QPushButton:pressed {
        background-color: #1d4ed8;
    }


    /* =========================================================
       TEXT AND DATE INPUTS

       #0f172a - Editable field background
       #f8fafc - Editable field text
       #475569 - Normal input border
       #3b82f6 - Focused input border
       #1e293b - Disabled field background
       #64748b - Disabled field text
       #334155 - Disabled field border
       ========================================================= */

    QLineEdit,
    QDateEdit {
        background-color: #0f172a;
        color: #f8fafc;
        border: 1px solid #475569;
        border-radius: 8px;
        padding: 8px 10px;
    }

    QLineEdit:focus,
    QDateEdit:focus {
        border: 1px solid #3b82f6;
    }

    QLineEdit:disabled,
    QDateEdit:disabled {
        background-color: #1e293b;
        color: #64748b;
        border: 1px solid #334155;
    }


    /* =========================================================
       CALENDAR POPUP

       #111827 - Calendar background
       #0f172a - Calendar navigation / header background
       #f8fafc - Primary calendar text
       #e2e8f0 - Secondary navigation text
       #334155 - Calendar borders
       #0f172a - Month / year control background
       #475569 - Month / year control border
       #1e293b - Navigation hover background
       #3b82f6 - Selected date background
       #ffffff - Selected date text
       #64748b - Disabled / out-of-range date text
       ========================================================= */

    QCalendarWidget {
        background-color: #111827;
        color: #f8fafc;
    }

    QCalendarWidget QWidget#qt_calendar_navigationbar {
        background-color: #0f172a;
        border-bottom: 1px solid #334155;
    }

    QCalendarWidget QToolButton {
        background-color: transparent;
        color: #e2e8f0;
        border: none;
        border-radius: 6px;
        padding: 6px;
    }

    QCalendarWidget QToolButton:hover {
        background-color: #1e293b;
        color: #f8fafc;
    }

    QCalendarWidget QSpinBox {
        background-color: #0f172a;
        color: #f8fafc;
        border: 1px solid #475569;
        border-radius: 6px;
        padding: 4px;
    }

    QCalendarWidget QAbstractItemView:enabled {
        background-color: #111827;
        color: #f8fafc;
        selection-background-color: #3b82f6;
        selection-color: #ffffff;
        outline: none;
    }

    QCalendarWidget QAbstractItemView:disabled {
        color: #64748b;
    }


    /* =========================================================
       COMBO BOXES / DROPDOWN SELECTORS

       #0f172a - Closed dropdown background
       #111827 - Open dropdown list background
       #f8fafc - Dropdown text
       #475569 - Standard border
       #64748b - Hover border
       #3b82f6 - Focus border
       #172554 - Dropdown item hover background
       #1e3a5f - Selected dropdown item background
       ========================================================= */

    QComboBox {
        background-color: #0f172a;
        color: #f8fafc;
        border: 1px solid #475569;
        border-radius: 8px;
        padding: 8px 10px;
        min-height: 18px;
    }

    QComboBox:hover {
        border: 1px solid #64748b;
    }

    QComboBox:focus {
        border: 1px solid #3b82f6;
    }

    QComboBox::drop-down {
        border: none;
        width: 28px;
    }

    QComboBox QAbstractItemView {
        background-color: #111827;
        color: #f8fafc;
        border: 1px solid #475569;
        outline: none;
    }

    QComboBox QAbstractItemView::item {
        background-color: #111827;
        color: #f8fafc;
        padding: 6px 10px;
    }

    QComboBox QAbstractItemView::item:hover {
        background-color: #172554;
        color: #f8fafc;
    }

    QComboBox QAbstractItemView::item:selected {
        background-color: #1e3a5f;
        color: #f8fafc;
    }


    /* =========================================================
       DIALOGS AND MESSAGE BOXES

       #111827 - Dialog / message box background
       #e2e8f0 - Dialog text and checkbox label text
       ========================================================= */

    QDialog,
    QMessageBox {
        background-color: #111827;
        color: #e2e8f0;
    }

    QDialog QLabel,
    QMessageBox QLabel {
        color: #e2e8f0;
    }

    QDialog QCheckBox {
        color: #e2e8f0;
        spacing: 7px;
    }


    /* =========================================================
       GENERAL LIST WIDGETS

       List backgrounds remain transparent so the surrounding panel
       and custom card colours remain visible.
       ========================================================= */

    QListWidget {
        background-color: transparent;
        border: none;
        outline: none;
    }

    QListWidget#stepList {
        color: #f8fafc;
    }


    /* =========================================================
       TASK AND STEP LIST ITEMS

       List items are deliberately transparent because the embedded
       TaskCard and StepCard widgets own their visual states.
       ========================================================= */

    QListWidget#taskList::item,
    QListWidget#stepList::item {
        background-color: transparent;
        padding: 0px;
    }

    QListWidget#stepList::item {
        color: #f8fafc;
    }


    /* =========================================================
       CUSTOM DRAG AND DROP INDICATORS

       #3b82f6 - Insertion line shown between cards while
                  reordering tasks or steps
       ========================================================= */

    QFrame#customDropIndicator {
        background-color: #3b82f6;
        border: none;
        border-radius: 1px;
    }


    /* =========================================================
       TASK AND STEP CARDS

       #1e293b - Normal card background
       #334155 - Normal card border
       #172554 - Hovered card background
       #3b82f6 - Hovered card border
       #1e3a5f - Selected card background
       #3b82f6 - Selected card border
       ========================================================= */

    QFrame#taskCard,
    QFrame#stepCard {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 10px;
    }

    QFrame#taskCard:hover,
    QFrame#stepCard:hover {
        background-color: #172554;
        border: 1px solid #3b82f6;
    }

    QFrame#taskCard[selected="true"],
    QFrame#stepCard[selected="true"],
    QFrame#taskCard[selected="true"]:hover,
    QFrame#stepCard[selected="true"]:hover {
        background-color: #1e3a5f;
        border: 2px solid #3b82f6;
    }


    /* =========================================================
       TASK CARD TEXT

       #f8fafc - Task title / primary text
       #94a3b8 - Secondary task details
       ========================================================= */

    QLabel#taskCardTitle {
        color: #f8fafc;
        font-size: 16px;
        font-weight: 700;
    }

    QLabel#taskCardDetails {
        color: #94a3b8;
        font-size: 13px;
    }


    /* =========================================================
       TASK STATUS BADGES

       #cbd5e1 / #334155 - TBD text / background
       #bfdbfe / #1e3a8a - WIP text / background
       #fed7aa / #7c2d12 - Awaiting text / background
       #bbf7d0 / #14532d - Completed text / background
       ========================================================= */

    QLabel#statusBadge {
        border-radius: 8px;
        padding: 4px 8px;
        font-weight: 600;
    }

    QLabel#statusBadge[status="TBD"] {
        color: #cbd5e1;
        background-color: #334155;
    }

    QLabel#statusBadge[status="WIP"] {
        color: #bfdbfe;
        background-color: #1e3a8a;
    }

    QLabel#statusBadge[status="Awaiting"] {
        color: #fed7aa;
        background-color: #7c2d12;
    }

    QLabel#statusBadge[status="Completed"] {
        color: #bbf7d0;
        background-color: #14532d;
    }


    /* =========================================================
       STEP CARD TEXT

       #f8fafc - Step description / primary text
       ========================================================= */

    QLabel#stepDescription {
        color: #f8fafc;
        font-size: 15px;
        font-weight: 600;
    }


    /* =========================================================
       CHECKBOX LABELS AND SPACING

       #e2e8f0 - Inline "Add dependency" label text

       Step completion and dependency-resolution checkboxes have no
       label spacing because their text is rendered separately.

       "Add dependency" includes its own label and therefore uses
       normal spacing.
       ========================================================= */

    QCheckBox#stepCheckbox,
    QCheckBox#stepDependencyResolvedCheckbox,
    QCheckBox#taskDependencyResolvedCheckbox {
        spacing: 0px;
    }

    QCheckBox#addStepDependencyCheckbox {
        color: #e2e8f0;
        font-size: 14px;
        spacing: 7px;
    }


    /* =========================================================
       STANDARD CHECKBOX INDICATORS

       Used by:
       - Dialog checkboxes
       - Step completion checkbox
       - Inline "Add dependency" checkbox

       #0f172a - Unchecked indicator background
       #64748b - Normal indicator border
       ========================================================= */

    QDialog QCheckBox::indicator,
    QCheckBox#stepCheckbox::indicator,
    QCheckBox#addStepDependencyCheckbox::indicator {
        width: 18px;
        height: 18px;
        border: 2px solid #64748b;
        border-radius: 4px;
        background-color: #0f172a;
    }


    /* =========================================================
       DEPENDENCY-RESOLUTION CHECKBOX INDICATORS

       These use a smaller 16px indicator to distinguish the
       subordinate dependency control from the main checkbox.

       #0f172a - Unresolved indicator background
       #64748b - Normal indicator border
       ========================================================= */

    QCheckBox#stepDependencyResolvedCheckbox::indicator,
    QCheckBox#taskDependencyResolvedCheckbox::indicator {
        width: 16px;
        height: 16px;
        border: 2px solid #64748b;
        border-radius: 4px;
        background-color: #0f172a;
    }


    /* =========================================================
       CHECKBOX HOVER STATE

       #3b82f6 - Hover border for every interactive
                  checkbox
       ========================================================= */

    QDialog QCheckBox::indicator:hover,
    QCheckBox#stepCheckbox::indicator:hover,
    QCheckBox#addStepDependencyCheckbox::indicator:hover,
    QCheckBox#stepDependencyResolvedCheckbox::indicator:hover,
    QCheckBox#taskDependencyResolvedCheckbox::indicator:hover {
        border: 2px solid #3b82f6;
    }


    /* =========================================================
       CHECKBOX CHECKED STATE

       #3b82f6 - Checked background and border
       check.svg - White checkmark icon

       All checkboxes use the same checked-state visual language.
       ========================================================= */

    QDialog QCheckBox::indicator:checked,
    QCheckBox#stepCheckbox::indicator:checked,
    QCheckBox#addStepDependencyCheckbox::indicator:checked,
    QCheckBox#stepDependencyResolvedCheckbox::indicator:checked,
    QCheckBox#taskDependencyResolvedCheckbox::indicator:checked {
        background-color: #3b82f6;
        border: 2px solid #3b82f6;
        image: url(assets/icons/check.svg);
    }


    /* =========================================================
       DEPENDENCY TEXT

       #fb923c - Warning / waiting-for-dependency text
       ========================================================= */

    QLabel#stepDependencyText,
    QLabel#taskDependencyText {
        color: #fb923c;
        font-size: 13px;
    }


    /* =========================================================
       EDIT / DELETE TOOL BUTTONS

       Transparent - Normal button background
       #172554 - Edit hover background
       #1e40af - Edit hover border
       #1e3a5f - Edit pressed background
       #451a1a - Delete hover background
       #7f1d1d - Delete hover border
       #7f1d1d - Delete pressed background
       ========================================================= */

    QToolButton#stepEditButton,
    QToolButton#stepDeleteButton,
    QToolButton#taskEditButton,
    QToolButton#taskDeleteButton {
        background-color: transparent;
        border: 1px solid transparent;
        border-radius: 8px;
        padding: 4px;
    }

    QToolButton#stepEditButton:hover,
    QToolButton#taskEditButton:hover {
        background-color: #172554;
        border: 1px solid #1e40af;
    }

    QToolButton#stepEditButton:pressed,
    QToolButton#taskEditButton:pressed {
        background-color: #1e3a5f;
    }

    QToolButton#stepDeleteButton:hover,
    QToolButton#taskDeleteButton:hover {
        background-color: #451a1a;
        border: 1px solid #7f1d1d;
    }

    QToolButton#stepDeleteButton:pressed,
    QToolButton#taskDeleteButton:pressed {
        background-color: #7f1d1d;
    }

"""