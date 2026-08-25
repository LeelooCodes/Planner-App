LIGHT_THEME = """

    /* =========================================================
       GLOBAL APPLICATION

       #eef2f7 - Main application background
       #334155 - Default foreground / text colour
       ========================================================= */

    QMainWindow {
        background-color: #eef2f7;
    }

    QWidget {
        color: #334155;
    }


    /* =========================================================
       APPLICATION MENUS

       #f8fafc - Menu bar background
       #ffffff - Dropdown menu background
       #334155 - Normal menu text
       #0f172a - Active / selected menu text
       #d7dee8 - Menu bar border
       #cbd5e1 - Dropdown menu border
       #dbeafe - Hovered menu item background
       #bfdbfe - Pressed menu bar item background
       #dbeafe - Selected dropdown menu item background
       #e2e8f0 - Menu separators
       ========================================================= */

    QMenuBar {
        background-color: #f8fafc;
        color: #334155;
        border-bottom: 1px solid #d7dee8;
        padding: 4px 8px;
        spacing: 4px;
    }

    QMenuBar::item {
        background-color: transparent;
        color: #334155;
        padding: 6px 10px;
        border-radius: 6px;
    }

    QMenuBar::item:selected {
        background-color: #dbeafe;
        color: #0f172a;
    }

    QMenuBar::item:pressed {
        background-color: #bfdbfe;
        color: #0f172a;
    }

    QMenu {
        background-color: #ffffff;
        color: #334155;
        border: 1px solid #cbd5e1;
        padding: 4px;
    }

    QMenu::item {
        background-color: transparent;
        color: #334155;
        padding: 7px 28px 7px 10px;
        border-radius: 5px;
    }

    QMenu::item:selected {
        background-color: #dbeafe;
        color: #0f172a;
    }

    QMenu::separator {
        height: 1px;
        background-color: #e2e8f0;
        margin: 4px 8px;
    }


    /* =========================================================
       GENERAL LABELS AND HEADINGS

       #334155 - Standard application text
       #1e293b - Strong / primary title text
       ========================================================= */

    QLabel {
        color: #334155;
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


    /* =========================================================
       MAIN PANELS

       #ffffff - Panel background
       #d7dee8 - Panel border
       ========================================================= */

    QFrame#panel {
        background-color: #ffffff;
        border: 1px solid #d7dee8;
        border-radius: 12px;
    }


    /* =========================================================
       GENERAL PUSH BUTTONS

       #2563eb - Normal primary button background
       #1d4ed8 - Hovered primary button background
       #1e40af - Pressed primary button background
       #ffffff - Button text
       ========================================================= */

    QPushButton {
        background-color: #2563eb;
        color: #ffffff;
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


    /* =========================================================
       TEXT AND DATE INPUTS

       #ffffff - Editable field background
       #0f172a - Editable field text
       #cbd5e1 - Normal input border
       #2563eb - Focused input border
       #e2e8f0 - Disabled field background
       #64748b - Disabled field text
       #cbd5e1 - Disabled field border
       ========================================================= */

    QLineEdit,
    QDateEdit {
        background-color: #ffffff;
        color: #0f172a;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 8px 10px;
    }

    QLineEdit:focus,
    QDateEdit:focus {
        border: 1px solid #2563eb;
    }

    QLineEdit:disabled,
    QDateEdit:disabled {
        background-color: #e2e8f0;
        color: #64748b;
        border: 1px solid #cbd5e1;
    }


    /* =========================================================
       CALENDAR POPUP

       #ffffff - Calendar background
       #f8fafc - Calendar navigation / header background
       #0f172a - Primary calendar text
       #334155 - Secondary navigation text
       #cbd5e1 - Calendar borders
       #ffffff - Month / year control background
       #cbd5e1 - Month / year control border
       #dbeafe - Navigation hover background
       #2563eb - Selected date background
       #ffffff - Selected date text
       #94a3b8 - Disabled / out-of-range date text
       ========================================================= */

    QCalendarWidget {
        background-color: #ffffff;
        color: #0f172a;
    }

    QCalendarWidget QWidget#qt_calendar_navigationbar {
        background-color: #f8fafc;
        border-bottom: 1px solid #cbd5e1;
    }

    QCalendarWidget QToolButton {
        background-color: transparent;
        color: #334155;
        border: none;
        border-radius: 6px;
        padding: 6px;
    }

    QCalendarWidget QToolButton:hover {
        background-color: #dbeafe;
        color: #0f172a;
    }

    QCalendarWidget QSpinBox {
        background-color: #ffffff;
        color: #0f172a;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 4px;
    }

    QCalendarWidget QAbstractItemView:enabled {
        background-color: #ffffff;
        color: #0f172a;
        selection-background-color: #2563eb;
        selection-color: #ffffff;
        outline: none;
    }

    QCalendarWidget QAbstractItemView:disabled {
        color: #94a3b8;
    }


    /* =========================================================
       COMBO BOXES / DROPDOWN SELECTORS

       #ffffff - Closed dropdown background
       #ffffff - Open dropdown list background
       #0f172a - Dropdown text
       #cbd5e1 - Standard border
       #94a3b8 - Hover border
       #2563eb - Focus border
       #eff6ff - Dropdown item hover background
       #dbeafe - Selected dropdown item background
       ========================================================= */

    QComboBox {
        background-color: #ffffff;
        color: #0f172a;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 8px 10px;
        min-height: 18px;
    }

    QComboBox:hover {
        border: 1px solid #94a3b8;
    }

    QComboBox:focus {
        border: 1px solid #2563eb;
    }

    QComboBox::drop-down {
        border: none;
        width: 28px;
    }

    QComboBox QAbstractItemView {
        background-color: #ffffff;
        color: #0f172a;
        border: 1px solid #cbd5e1;
        outline: none;
    }

    QComboBox QAbstractItemView::item {
        background-color: #ffffff;
        color: #0f172a;
        padding: 6px 10px;
    }

    QComboBox QAbstractItemView::item:hover {
        background-color: #eff6ff;
        color: #0f172a;
    }

    QComboBox QAbstractItemView::item:selected {
        background-color: #dbeafe;
        color: #0f172a;
    }


    /* =========================================================
       DIALOGS AND MESSAGE BOXES

       #f8fafc - Dialog / message box background
       #334155 - Dialog text and checkbox label text
       ========================================================= */

    QDialog,
    QMessageBox {
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
        color: #1e293b;
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
        color: #1e293b;
    }


    /* =========================================================
       CUSTOM DRAG AND DROP INDICATORS

       #2563eb - Insertion line shown between cards while
                  reordering tasks or steps
       ========================================================= */

    QFrame#customDropIndicator {
        background-color: #2563eb;
        border: none;
        border-radius: 1px;
    }


    /* =========================================================
       TASK AND STEP CARDS

       #f8fafc - Normal card background
       #d7dee8 - Normal card border
       #e0eaff - Hovered card background
       #93c5fd - Hovered card border
       #dbeafe - Selected card background
       #2563eb - Selected card border
       ========================================================= */

    QFrame#taskCard,
    QFrame#stepCard {
        background-color: #f8fafc;
        border: 1px solid #d7dee8;
        border-radius: 10px;
    }

    QFrame#taskCard:hover,
    QFrame#stepCard:hover {
        background-color: #e0eaff;
        border: 1px solid #93c5fd;
    }

    QFrame#taskCard[selected="true"],
    QFrame#stepCard[selected="true"],
    QFrame#taskCard[selected="true"]:hover,
    QFrame#stepCard[selected="true"]:hover {
        background-color: #dbeafe;
        border: 2px solid #2563eb;
    }


    /* =========================================================
       TASK CARD TEXT

       #0f172a - Task title / primary text
       #64748b - Secondary task details
       ========================================================= */

    QLabel#taskCardTitle {
        color: #0f172a;
        font-size: 16px;
        font-weight: 700;
    }

    QLabel#taskCardDetails {
        color: #64748b;
        font-size: 13px;
    }


    /* =========================================================
       STEP CARD TEXT

       #0f172a - Step description / primary text
       ========================================================= */

    QLabel#stepDescription {
        color: #0f172a;
        font-size: 15px;
        font-weight: 600;
    }


    /* =========================================================
       CHECKBOX LABELS AND SPACING

       #334155 - Inline "Add dependency" label text

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
        color: #334155;
        font-size: 14px;
        spacing: 7px;
    }


    /* =========================================================
       STANDARD CHECKBOX INDICATORS

       Used by:
       - Dialog checkboxes
       - Step completion checkbox
       - Inline "Add dependency" checkbox

       #ffffff - Unchecked indicator background
       #64748b - Normal indicator border
       ========================================================= */

    QDialog QCheckBox::indicator,
    QCheckBox#stepCheckbox::indicator,
    QCheckBox#addStepDependencyCheckbox::indicator {
        width: 18px;
        height: 18px;
        border: 2px solid #64748b;
        border-radius: 4px;
        background-color: #ffffff;
    }


    /* =========================================================
       DEPENDENCY-RESOLUTION CHECKBOX INDICATORS

       These use a smaller 16px indicator to distinguish the
       subordinate dependency control from the main checkbox.

       #ffffff - Unresolved indicator background
       #64748b - Normal indicator border
       ========================================================= */

    QCheckBox#stepDependencyResolvedCheckbox::indicator,
    QCheckBox#taskDependencyResolvedCheckbox::indicator {
        width: 16px;
        height: 16px;
        border: 2px solid #64748b;
        border-radius: 4px;
        background-color: #ffffff;
    }


    /* =========================================================
       CHECKBOX HOVER STATE

       #2563eb - Hover border for every interactive
                  checkbox
       ========================================================= */

    QDialog QCheckBox::indicator:hover,
    QCheckBox#stepCheckbox::indicator:hover,
    QCheckBox#addStepDependencyCheckbox::indicator:hover,
    QCheckBox#stepDependencyResolvedCheckbox::indicator:hover,
    QCheckBox#taskDependencyResolvedCheckbox::indicator:hover {
        border: 2px solid #2563eb;
    }


    /* =========================================================
       CHECKBOX CHECKED STATE

       #2563eb - Checked background and border
       check.svg - White checkmark icon

       All checkboxes use the same checked-state visual language.
       ========================================================= */

    QDialog QCheckBox::indicator:checked,
    QCheckBox#stepCheckbox::indicator:checked,
    QCheckBox#addStepDependencyCheckbox::indicator:checked,
    QCheckBox#stepDependencyResolvedCheckbox::indicator:checked,
    QCheckBox#taskDependencyResolvedCheckbox::indicator:checked {
        background-color: #2563eb;
        border: 2px solid #2563eb;
        image: url(assets/icons/check.svg);
    }


    /* =========================================================
       DEPENDENCY TEXT

       #9a3412 - Warning / waiting-for-dependency text
       ========================================================= */

    QLabel#stepDependencyText,
    QLabel#taskDependencyText {
        color: #9a3412;
        font-size: 13px;
    }


    /* =========================================================
       EDIT / DELETE TOOL BUTTONS

       Transparent - Normal button background
       #dbeafe - Edit hover background
       #bfdbfe - Edit hover border
       #bfdbfe - Edit pressed background
       #fee2e2 - Delete hover background
       #fecaca - Delete hover border
       #fecaca - Delete pressed background
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
        background-color: #dbeafe;
        border: 1px solid #bfdbfe;
    }

    QToolButton#stepEditButton:pressed,
    QToolButton#taskEditButton:pressed {
        background-color: #bfdbfe;
    }

    QToolButton#stepDeleteButton:hover,
    QToolButton#taskDeleteButton:hover {
        background-color: #fee2e2;
        border: 1px solid #fecaca;
    }

    QToolButton#stepDeleteButton:pressed,
    QToolButton#taskDeleteButton:pressed {
        background-color: #fecaca;
    }

"""