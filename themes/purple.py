PURPLE_ICON_COLORS = {
    "edit": {
        "fill": "#32145c",
        "stroke": "#c7a2ea",
    },
    "delete": {
        "fill": "#4a103f",
        "stroke": "#e38ac0",
    },
}

PURPLE_THEME = """

    /* =========================================================
       GLOBAL APPLICATION

       #080121 - Main application background
       #d9c8ee - Default foreground / text colour
       ========================================================= */

    QMainWindow {
        background-color: #080121;
    }

    QWidget {
        color: #d9c8ee;
    }


    /* =========================================================
       APPLICATION MENUS

       #120239 - Menu bar background
       #120239 - Dropdown menu background
       #d9c8ee - Normal menu text
       #f7f0ff - Active / selected menu text
       #260656 - Menu bar border
       #260656 - Dropdown menu border
       #260656 - Hovered menu item background
       #4A1985 - Pressed menu bar item background
       #260656 - Selected dropdown menu item background
       #260656 - Menu separators
       ========================================================= */

    QMenuBar {
        background-color: #120239;
        color: #d9c8ee;
        border-bottom: 1px solid #260656;
        padding: 4px 8px;
        spacing: 4px;
    }

    QMenuBar::item {
        background-color: transparent;
        color: #d9c8ee;
        padding: 6px 10px;
        border-radius: 6px;
    }

    QMenuBar::item:selected {
        background-color: #260656;
        color: #f7f0ff;
    }

    QMenuBar::item:pressed {
        background-color: #4A1985;
        color: #f7f0ff;
    }

    QMenu {
        background-color: #120239;
        color: #d9c8ee;
        border: 1px solid #260656;
        padding: 4px;
    }

    QMenu::item {
        background-color: transparent;
        color: #d9c8ee;
        padding: 7px 28px 7px 10px;
        border-radius: 5px;
    }

    QMenu::item:selected {
        background-color: #260656;
        color: #f7f0ff;
    }

    QMenu::separator {
        height: 1px;
        background-color: #260656;
        margin: 4px 8px;
    }


    /* =========================================================
       GENERAL LABELS AND HEADINGS

       #d9c8ee - Standard application text
       #f1e6ff - Strong / primary title text
       ========================================================= */

    QLabel {
        color: #d9c8ee;
    }

    QLabel#appTitle {
        color: #f1e6ff;
        font-size: 28px;
        font-weight: bold;
    }

    QLabel#sectionTitle {
        color: #d9c8ee;
        font-size: 18px;
        font-weight: 600;
    }


    /* =========================================================
       MAIN PANELS

       #120239 - Panel background
       #260656 - Panel border
       ========================================================= */

    QFrame#panel {
        background-color: #120239;
        border: 1px solid #260656;
        border-radius: 12px;
    }


    /* =========================================================
       GENERAL PUSH BUTTONS

       #4A1985 - Normal primary button background
       #5d259d - Hovered primary button background
       #260656 - Pressed primary button background
       #f7f0ff - Button text
       ========================================================= */

    QPushButton {
        background-color: #4A1985;
        color: #f7f0ff;
        border: none;
        border-radius: 8px;
        padding: 8px;
    }

    QPushButton:hover {
        background-color: #5d259d;
    }

    QPushButton:pressed {
        background-color: #260656;
    }


    /* =========================================================
       TEXT AND DATE INPUTS

       #120239 - Editable field background
       #f7f0ff - Editable field text
       #260656 - Normal input border
       #A580CA - Focused input border
       #080121 - Disabled field background
       #80659f - Disabled field text
       #260656 - Disabled field border
       ========================================================= */

    QLineEdit,
    QDateEdit {
        background-color: #120239;
        color: #f7f0ff;
        border: 1px solid #260656;
        border-radius: 8px;
        padding: 8px 10px;
    }

    QLineEdit:focus,
    QDateEdit:focus {
        border: 1px solid #A580CA;
    }

    QLineEdit:disabled,
    QDateEdit:disabled {
        background-color: #080121;
        color: #80659f;
        border: 1px solid #260656;
    }


    /* =========================================================
       CALENDAR POPUP

       #120239 - Calendar background
       #080121 - Calendar navigation / header background
       #f7f0ff - Primary calendar text
       #d9c8ee - Secondary navigation text
       #260656 - Calendar borders
       #120239 - Month / year control background
       #260656 - Month / year control border
       #260656 - Navigation hover background
       #4A1985 - Selected date background
       #f7f0ff - Selected date text
       #80659f - Disabled / out-of-range date text
       ========================================================= */

    QCalendarWidget {
        background-color: #120239;
        color: #f7f0ff;
    }

    QCalendarWidget QWidget#qt_calendar_navigationbar {
        background-color: #080121;
        border-bottom: 1px solid #260656;
    }

    QCalendarWidget QToolButton {
        background-color: transparent;
        color: #d9c8ee;
        border: none;
        border-radius: 6px;
        padding: 6px;
    }

    QCalendarWidget QToolButton:hover {
        background-color: #260656;
        color: #f7f0ff;
    }

    QCalendarWidget QSpinBox {
        background-color: #120239;
        color: #f7f0ff;
        border: 1px solid #260656;
        border-radius: 6px;
        padding: 4px;
    }

    QCalendarWidget QAbstractItemView:enabled {
        background-color: #120239;
        color: #f7f0ff;
        selection-background-color: #4A1985;
        selection-color: #f7f0ff;
        outline: none;
    }

    QCalendarWidget QAbstractItemView:disabled {
        color: #80659f;
    }


    /* =========================================================
       COMBO BOXES / DROPDOWN SELECTORS

       #120239 - Closed dropdown background
       #120239 - Open dropdown list background
       #f7f0ff - Dropdown text
       #260656 - Standard border
       #4A1985 - Hover border
       #A580CA - Focus border
       #1b0445 - Dropdown item hover background
       #260656 - Selected dropdown item background
       ========================================================= */

    QComboBox {
        background-color: #120239;
        color: #f7f0ff;
        border: 1px solid #260656;
        border-radius: 8px;
        padding: 8px 10px;
        min-height: 18px;
    }

    QComboBox:hover {
        border: 1px solid #4A1985;
    }

    QComboBox:focus {
        border: 1px solid #A580CA;
    }

    QComboBox::drop-down {
        border: none;
        width: 28px;
    }

    QComboBox QAbstractItemView {
        background-color: #120239;
        color: #f7f0ff;
        border: 1px solid #260656;
        outline: none;
    }

    QComboBox QAbstractItemView::item {
        background-color: #120239;
        color: #f7f0ff;
        padding: 6px 10px;
    }

    QComboBox QAbstractItemView::item:hover {
        background-color: #1b0445;
        color: #f7f0ff;
    }

    QComboBox QAbstractItemView::item:selected {
        background-color: #260656;
        color: #f7f0ff;
    }


    /* =========================================================
       DIALOGS AND MESSAGE BOXES

       #120239 - Dialog / message box background
       #d9c8ee - Dialog text and checkbox label text
       ========================================================= */

    QDialog,
    QMessageBox {
        background-color: #120239;
        color: #d9c8ee;
    }

    QDialog QLabel,
    QMessageBox QLabel {
        color: #d9c8ee;
    }

    QDialog QCheckBox {
        color: #d9c8ee;
        spacing: 7px;
    }

     /* =========================================================
    SETTINGS - FONT PREVIEW
    ========================================================= */

    QLabel#settingsPreviewTitle {
        color: #c4a8dc;
        font-size: 14px;
        font-weight: 600;
    }

    QLabel#fontPreview {
        background-color: #1a0338;
        color: #e9dcf7;

        border: 1px solid #4A1985;
        border-radius: 10px;
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
        color: #f1e6ff;
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
        color: #f1e6ff;
    }


    /* =========================================================
       CUSTOM DRAG AND DROP INDICATORS

       #A580CA - Insertion line shown between cards while
                  reordering tasks or steps
       ========================================================= */

    QFrame#customDropIndicator {
        background-color: #A580CA;
        border: none;
        border-radius: 1px;
    }


    /* =========================================================
       TASK AND STEP CARDS

       #120239 - Normal card background
       #260656 - Normal card border
       #1b0445 - Hovered card background
       #4A1985 - Hovered card border
       #260656 - Selected card background
       #A580CA - Selected card border
       ========================================================= */

    QFrame#taskCard,
    QFrame#stepCard {
        background-color: #120239;
        border: 1px solid #260656;
        border-radius: 10px;
    }

    QFrame#taskCard:hover,
    QFrame#stepCard:hover {
        background-color: #1b0445;
        border: 1px solid #4A1985;
    }

    QFrame#taskCard[selected="true"],
    QFrame#stepCard[selected="true"],
    QFrame#taskCard[selected="true"]:hover,
    QFrame#stepCard[selected="true"]:hover {
        background-color: #260656;
        border: 2px solid #A580CA;
    }


    /* =========================================================
       TASK CARD TEXT

       #c4a8dc - Task title / primary text
       #A580CA - Secondary task details
       ========================================================= */

    QLabel#taskCardTitle {
        color: #c4a8dc;
        font-size: 16px;
        font-weight: 700;
    }

    QLabel#taskCardDetails {
        color: #A580CA;
        font-size: 13px;
    }


    /* =========================================================
       TASK STATUS BADGES

       #d9c8ee / #1a0338 - TBD text / background
       #080121 - TBD border
       #f1e6ff / #4A1985 - WIP text / background
       #e6b8f2 / #3a0b5c - Awaiting text / background
       #e9dcf7 / #32145c - Completed text / background
       ========================================================= */

    QLabel#statusBadge {
        border-radius: 8px;
        padding: 4px 8px;
        font-weight: 600;
    }

    QLabel#statusBadge[status="TBD"] {
        color: #d9c8ee;
        background-color: #1a0338;
        border: 1px solid #080121;
    }

    QLabel#statusBadge[status="WIP"] {
        color: #f1e6ff;
        background-color: #4A1985;
    }

    QLabel#statusBadge[status="Awaiting"] {
        color: #e6b8f2;
        background-color: #3a0b5c;
    }

    QLabel#statusBadge[status="Completed"] {
        color: #e9dcf7;
        background-color: #32145c;
    }


    /* =========================================================
       STEP CARD TEXT

       #c4a8dc - Step description / primary text
       ========================================================= */

    QLabel#stepDescription {
        color: #c4a8dc;
        font-size: 15px;
        font-weight: 600;
    }


    /* =========================================================
       CHECKBOX LABELS AND SPACING

       #d9c8ee - Inline "Add dependency" label text

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
        color: #d9c8ee;
        font-size: 14px;
        spacing: 7px;
    }


    /* =========================================================
       STANDARD CHECKBOX INDICATORS

       Used by:
       - Dialog checkboxes
       - Step completion checkbox
       - Inline "Add dependency" checkbox

       #120239 - Unchecked indicator background
       #80659f - Normal indicator border
       ========================================================= */

    QDialog QCheckBox::indicator,
    QCheckBox#stepCheckbox::indicator,
    QCheckBox#addStepDependencyCheckbox::indicator {
        width: 18px;
        height: 18px;
        border: 2px solid #80659f;
        border-radius: 4px;
        background-color: #120239;
    }


    /* =========================================================
       DEPENDENCY-RESOLUTION CHECKBOX INDICATORS

       These use a smaller 16px indicator to distinguish the
       subordinate dependency control from the main checkbox.

       #120239 - Unresolved indicator background
       #80659f - Normal indicator border
       ========================================================= */

    QCheckBox#stepDependencyResolvedCheckbox::indicator,
    QCheckBox#taskDependencyResolvedCheckbox::indicator {
        width: 16px;
        height: 16px;
        border: 2px solid #80659f;
        border-radius: 4px;
        background-color: #120239;
    }


    /* =========================================================
       CHECKBOX HOVER STATE

       #A580CA - Hover border for every interactive
                  checkbox
       ========================================================= */

    QDialog QCheckBox::indicator:hover,
    QCheckBox#stepCheckbox::indicator:hover,
    QCheckBox#addStepDependencyCheckbox::indicator:hover,
    QCheckBox#stepDependencyResolvedCheckbox::indicator:hover,
    QCheckBox#taskDependencyResolvedCheckbox::indicator:hover {
        border: 2px solid #A580CA;
    }


    /* =========================================================
       CHECKBOX CHECKED STATE

       #4A1985 - Checked background and border
       check.svg - White checkmark icon

       All checkboxes use the same checked-state visual language.
       ========================================================= */

    QDialog QCheckBox::indicator:checked,
    QCheckBox#stepCheckbox::indicator:checked,
    QCheckBox#addStepDependencyCheckbox::indicator:checked,
    QCheckBox#stepDependencyResolvedCheckbox::indicator:checked,
    QCheckBox#taskDependencyResolvedCheckbox::indicator:checked {
        background-color: #4A1985;
        border: 2px solid #4A1985;
        image: url(assets/icons/check.svg);
    }


    /* =========================================================
       DEPENDENCY TEXT

       #A580CA - Warning / waiting-for-dependency text
       ========================================================= */

    QLabel#stepDependencyText,
    QLabel#taskDependencyText {
        color: #A580CA;
        font-size: 13px;
    }


    /* =========================================================
       EDIT / DELETE TOOL BUTTONS

       Transparent - Normal button background
       #260656 - Edit hover background
       #4A1985 - Edit hover border
       #4A1985 - Edit pressed background
       #2f0b4a - Delete hover background
       #75377f - Delete hover border
       #75377f - Delete pressed background
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
        background-color: #260656;
        border: 1px solid #4A1985;
    }

    QToolButton#stepEditButton:pressed,
    QToolButton#taskEditButton:pressed {
        background-color: #4A1985;
    }

    QToolButton#stepDeleteButton:hover,
    QToolButton#taskDeleteButton:hover {
        background-color: #2f0b4a;
        border: 1px solid #75377f;
    }

    QToolButton#stepDeleteButton:pressed,
    QToolButton#taskDeleteButton:pressed {
        background-color: #75377f;
    }

"""