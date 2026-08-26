PINK_THEME = """

    /* =========================================================
       GLOBAL APPLICATION

       #fff7fa - Main application background
       #68415f - Default foreground / text colour
       ========================================================= */

    QMainWindow {
        background-color: #fff7fa;
    }

    QWidget {
        color: #68415f;
    }


    /* =========================================================
       APPLICATION MENUS

       #fceff3 - Menu bar background
       #fffafb - Dropdown menu background
       #68415f - Normal menu text
       #56354f - Active / selected menu text
       #f0ccd8 - Menu bar border
       #e8b5c7 - Dropdown menu border
       #ffe3ec - Hovered menu item background
       #ffc9db - Pressed menu bar item background
       #ffe3ec - Selected dropdown menu item background
       #f3dce4 - Menu separators
       ========================================================= */

    QMenuBar {
        background-color: #fceff3;
        color: #68415f;
        border-bottom: 1px solid #f0ccd8;
        padding: 4px 8px;
        spacing: 4px;
    }

    QMenuBar::item {
        background-color: transparent;
        color: #68415f;
        padding: 6px 10px;
        border-radius: 6px;
    }

    QMenuBar::item:selected {
        background-color: #ffe3ec;
        color: #56354f;
    }

    QMenuBar::item:pressed {
        background-color: #ffc9db;
        color: #56354f;
    }

    QMenu {
        background-color: #fffafb;
        color: #68415f;
        border: 1px solid #e8b5c7;
        padding: 4px;
    }

    QMenu::item {
        background-color: transparent;
        color: #68415f;
        padding: 7px 28px 7px 10px;
        border-radius: 5px;
    }

    QMenu::item:selected {
        background-color: #ffe3ec;
        color: #56354f;
    }

    QMenu::separator {
        height: 1px;
        background-color: #f3dce4;
        margin: 4px 8px;
    }


    /* =========================================================
       GENERAL LABELS AND HEADINGS

       #68415f - Standard application text
       #56354f - Strong / primary title text
       ========================================================= */

    QLabel {
        color: #68415f;
    }

    QLabel#appTitle {
        color: #56354f;
        font-size: 28px;
        font-weight: bold;
    }

    QLabel#sectionTitle {
        color: #68415f;
        font-size: 18px;
        font-weight: 600;
    }


    /* =========================================================
       MAIN PANELS

       #fffafb - Panel background
       #f0ccd8 - Panel border
       ========================================================= */

    QFrame#panel {
        background-color: #fffafb;
        border: 1px solid #f0ccd8;
        border-radius: 12px;
    }


    /* =========================================================
       GENERAL PUSH BUTTONS

       #d0618d - Normal primary button background
       #ba4f7a - Hovered primary button background
       #9f3e67 - Pressed primary button background
       #ffffff - Button text
       ========================================================= */

    QPushButton {
        background-color: #d0618d;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 8px;
    }

    QPushButton:hover {
        background-color: #ba4f7a;
    }

    QPushButton:pressed {
        background-color: #9f3e67;
    }


    /* =========================================================
       TEXT AND DATE INPUTS

       #fffafb - Editable field background
       #56354f - Editable field text
       #e8b5c7 - Normal input border
       #d0618d - Focused input border
       #f4dfe6 - Disabled field background
       #8f657f - Disabled field text
       #e8b5c7 - Disabled field border
       ========================================================= */

    QLineEdit,
    QDateEdit {
        background-color: #fffafb;
        color: #56354f;
        border: 1px solid #e8b5c7;
        border-radius: 8px;
        padding: 8px 10px;
    }

    QLineEdit:focus,
    QDateEdit:focus {
        border: 1px solid #d0618d;
    }

    QLineEdit:disabled,
    QDateEdit:disabled {
        background-color: #f4dfe6;
        color: #8f657f;
        border: 1px solid #e8b5c7;
    }


    /* =========================================================
       CALENDAR POPUP

       #fffafb - Calendar background
       #fceff3 - Calendar navigation / header background
       #56354f - Primary calendar text
       #68415f - Secondary navigation text
       #e8b5c7 - Calendar borders
       #fffafb - Month / year control background
       #e8b5c7 - Month / year control border
       #ffe3ec - Navigation hover background
       #d0618d - Selected date background
       #ffffff - Selected date text
       #bd91a3 - Disabled / out-of-range date text
       ========================================================= */

    QCalendarWidget {
        background-color: #fffafb;
        color: #56354f;
    }

    QCalendarWidget QWidget#qt_calendar_navigationbar {
        background-color: #fceff3;
        border-bottom: 1px solid #e8b5c7;
    }

    QCalendarWidget QToolButton {
        background-color: transparent;
        color: #68415f;
        border: none;
        border-radius: 6px;
        padding: 6px;
    }

    QCalendarWidget QToolButton:hover {
        background-color: #ffe3ec;
        color: #56354f;
    }

    QCalendarWidget QSpinBox {
        background-color: #fffafb;
        color: #56354f;
        border: 1px solid #e8b5c7;
        border-radius: 6px;
        padding: 4px;
    }

    QCalendarWidget QAbstractItemView:enabled {
        background-color: #fffafb;
        color: #56354f;
        selection-background-color: #d0618d;
        selection-color: #ffffff;
        outline: none;
    }

    QCalendarWidget QAbstractItemView:disabled {
        color: #bd91a3;
    }


    /* =========================================================
       COMBO BOXES / DROPDOWN SELECTORS

       #fffafb - Closed dropdown background
       #fffafb - Open dropdown list background
       #56354f - Dropdown text
       #e8b5c7 - Standard border
       #bd91a3 - Hover border
       #d0618d - Focus border
       #fff0f5 - Dropdown item hover background
       #ffe3ec - Selected dropdown item background
       ========================================================= */

    QComboBox {
        background-color: #fffafb;
        color: #56354f;
        border: 1px solid #e8b5c7;
        border-radius: 8px;
        padding: 8px 10px;
        min-height: 18px;
    }

    QComboBox:hover {
        border: 1px solid #bd91a3;
    }

    QComboBox:focus {
        border: 1px solid #d0618d;
    }

    QComboBox::drop-down {
        border: none;
        width: 28px;
    }

    QComboBox QAbstractItemView {
        background-color: #fffafb;
        color: #56354f;
        border: 1px solid #e8b5c7;
        outline: none;
    }

    QComboBox QAbstractItemView::item {
        background-color: #fffafb;
        color: #56354f;
        padding: 6px 10px;
    }

    QComboBox QAbstractItemView::item:hover {
        background-color: #fff0f5;
        color: #56354f;
    }

    QComboBox QAbstractItemView::item:selected {
        background-color: #ffe3ec;
        color: #56354f;
    }


    /* =========================================================
       DIALOGS AND MESSAGE BOXES

       #fceff3 - Dialog / message box background
       #68415f - Dialog text and checkbox label text
       ========================================================= */

    QDialog,
    QMessageBox {
        background-color: #fceff3;
        color: #68415f;
    }

    QDialog QLabel,
    QMessageBox QLabel {
        color: #68415f;
    }

    QDialog QCheckBox {
        color: #68415f;
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
        color: #56354f;
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
        color: #56354f;
    }


    /* =========================================================
       CUSTOM DRAG AND DROP INDICATORS

       #d0618d - Insertion line shown between cards while
                  reordering tasks or steps
       ========================================================= */

    QFrame#customDropIndicator {
        background-color: #d0618d;
        border: none;
        border-radius: 1px;
    }


    /* =========================================================
       TASK AND STEP CARDS

       #fffafb - Normal card background
       #f0ccd8 - Normal card border
       #ffe8f0 - Hovered card background
       #ffb7ce - Hovered card border
       #ffd7e4 - Selected card background
       #d0618d - Selected card border
       ========================================================= */

    QFrame#taskCard,
    QFrame#stepCard {
        background-color: #fffafb;
        border: 1px solid #f0ccd8;
        border-radius: 10px;
    }

    QFrame#taskCard:hover,
    QFrame#stepCard:hover {
        background-color: #ffe8f0;
        border: 1px solid #ffb7ce;
    }

    QFrame#taskCard[selected="true"],
    QFrame#stepCard[selected="true"],
    QFrame#taskCard[selected="true"]:hover,
    QFrame#stepCard[selected="true"]:hover {
        background-color: #ffd7e4;
        border: 2px solid #d0618d;
    }


    /* =========================================================
       TASK CARD TEXT

       #56354f - Task title / primary text
       #8f657f - Secondary task details
       ========================================================= */

    QLabel#taskCardTitle {
        color: #56354f;
        font-size: 16px;
        font-weight: 700;
    }

    QLabel#taskCardDetails {
        color: #8f657f;
        font-size: 13px;
    }


    /* =========================================================
       TASK STATUS BADGES

       #765667 / #f4dfe6 - TBD text / background
       #9f3e67 / #ffd7e4 - WIP text / background
       #a84d72 / #ffe3ec - Awaiting text / background
       #68415f / #eadce6 - Completed text / background
       ========================================================= */

    QLabel#statusBadge {
        border-radius: 8px;
        padding: 4px 8px;
        font-weight: 600;
    }

    QLabel#statusBadge[status="TBD"] {
        color: #765667;
        background-color: #f4dfe6;
    }

    QLabel#statusBadge[status="WIP"] {
        color: #9f3e67;
        background-color: #ffd7e4;
    }

    QLabel#statusBadge[status="Awaiting"] {
        color: #a84d72;
        background-color: #ffe3ec;
    }

    QLabel#statusBadge[status="Completed"] {
        color: #68415f;
        background-color: #eadce6;
    }


    /* =========================================================
       STEP CARD TEXT

       #56354f - Step description / primary text
       ========================================================= */

    QLabel#stepDescription {
        color: #56354f;
        font-size: 15px;
        font-weight: 600;
    }


    /* =========================================================
       CHECKBOX LABELS AND SPACING

       #68415f - Inline "Add dependency" label text

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
        color: #68415f;
        font-size: 14px;
        spacing: 7px;
    }


    /* =========================================================
       STANDARD CHECKBOX INDICATORS

       Used by:
       - Dialog checkboxes
       - Step completion checkbox
       - Inline "Add dependency" checkbox

       #fffafb - Unchecked indicator background
       #a9788d - Normal indicator border
       ========================================================= */

    QDialog QCheckBox::indicator,
    QCheckBox#stepCheckbox::indicator,
    QCheckBox#addStepDependencyCheckbox::indicator {
        width: 18px;
        height: 18px;
        border: 2px solid #a9788d;
        border-radius: 4px;
        background-color: #fffafb;
    }


    /* =========================================================
       DEPENDENCY-RESOLUTION CHECKBOX INDICATORS

       These use a smaller 16px indicator to distinguish the
       subordinate dependency control from the main checkbox.

       #fffafb - Unresolved indicator background
       #a9788d - Normal indicator border
       ========================================================= */

    QCheckBox#stepDependencyResolvedCheckbox::indicator,
    QCheckBox#taskDependencyResolvedCheckbox::indicator {
        width: 16px;
        height: 16px;
        border: 2px solid #a9788d;
        border-radius: 4px;
        background-color: #fffafb;
    }


    /* =========================================================
       CHECKBOX HOVER STATE

       #d0618d - Hover border for every interactive
                  checkbox
       ========================================================= */

    QDialog QCheckBox::indicator:hover,
    QCheckBox#stepCheckbox::indicator:hover,
    QCheckBox#addStepDependencyCheckbox::indicator:hover,
    QCheckBox#stepDependencyResolvedCheckbox::indicator:hover,
    QCheckBox#taskDependencyResolvedCheckbox::indicator:hover {
        border: 2px solid #d0618d;
    }


    /* =========================================================
       CHECKBOX CHECKED STATE

       #d0618d - Checked background and border
       check.svg - White checkmark icon

       All checkboxes use the same checked-state visual language.
       ========================================================= */

    QDialog QCheckBox::indicator:checked,
    QCheckBox#stepCheckbox::indicator:checked,
    QCheckBox#addStepDependencyCheckbox::indicator:checked,
    QCheckBox#stepDependencyResolvedCheckbox::indicator:checked,
    QCheckBox#taskDependencyResolvedCheckbox::indicator:checked {
        background-color: #d0618d;
        border: 2px solid #d0618d;
        image: url(assets/icons/check.svg);
    }


    /* =========================================================
       DEPENDENCY TEXT

       #a84d72 - Warning / waiting-for-dependency text
       ========================================================= */

    QLabel#stepDependencyText,
    QLabel#taskDependencyText {
        color: #a84d72;
        font-size: 13px;
    }


    /* =========================================================
       EDIT / DELETE TOOL BUTTONS

       Transparent - Normal button background
       #ffe3ec - Edit hover background
       #ffbfd3 - Edit hover border
       #ffbfd3 - Edit pressed background
       #fee7eb - Delete hover background
       #f6b5c0 - Delete hover border
       #f6b5c0 - Delete pressed background
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
        background-color: #ffe3ec;
        border: 1px solid #ffbfd3;
    }

    QToolButton#stepEditButton:pressed,
    QToolButton#taskEditButton:pressed {
        background-color: #ffbfd3;
    }

    QToolButton#stepDeleteButton:hover,
    QToolButton#taskDeleteButton:hover {
        background-color: #fee7eb;
        border: 1px solid #f6b5c0;
    }

    QToolButton#stepDeleteButton:pressed,
    QToolButton#taskDeleteButton:pressed {
        background-color: #f6b5c0;
    }

"""