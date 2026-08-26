from PySide6.QtCore import QByteArray, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QApplication, QToolButton

from utils.paths import resource_path


ICON_FILES = {
    "edit": "assets/icons/edit.svg",
    "delete": "assets/icons/delete.svg",
}


SOURCE_ICON_COLORS = {
    "edit": {
        "fill": "#DBEAFE",
        "stroke": "#2563EB",
    },
    "delete": {
        "fill": "#FEE2E2",
        "stroke": "#DC2626",
    },
}


BUTTON_ICON_NAMES = {
    "taskEditButton": "edit",
    "stepEditButton": "edit",
    "taskDeleteButton": "delete",
    "stepDeleteButton": "delete",
}


def get_current_icon_colors():
    app = QApplication.instance()

    if app is None:
        return SOURCE_ICON_COLORS

    icon_colors = app.property(
        "themeIconColors"
    )

    if not isinstance(
            icon_colors,
            dict
    ):
        return SOURCE_ICON_COLORS

    return icon_colors


def themed_icon(icon_name):
    if icon_name not in ICON_FILES:
        raise ValueError(
            f"Unknown themed icon: {icon_name}"
        )

    svg_path = resource_path(
        ICON_FILES[icon_name]
    )

    svg_data = svg_path.read_text(
        encoding="utf-8"
    )

    source_colors = SOURCE_ICON_COLORS[
        icon_name
    ]

    theme_colors = (
        get_current_icon_colors()
        .get(
            icon_name,
            source_colors
        )
    )

    svg_data = svg_data.replace(
        source_colors["fill"],
        theme_colors["fill"]
    )

    svg_data = svg_data.replace(
        source_colors["stroke"],
        theme_colors["stroke"]
    )

    renderer = QSvgRenderer(
        QByteArray(
            svg_data.encode(
                "utf-8"
            )
        )
    )

    icon = QIcon()

    for size in (
        16,
        20,
        24,
        32,
        48,
        64,
    ):
        pixmap = QPixmap(
            size,
            size
        )

        pixmap.fill(
            Qt.GlobalColor.transparent
        )

        painter = QPainter(
            pixmap
        )

        renderer.render(
            painter
        )

        painter.end()

        icon.addPixmap(
            pixmap
        )

    return icon


def refresh_themed_icons():
    app = QApplication.instance()

    if app is None:
        return

    for widget in app.allWidgets():
        if not isinstance(
                widget,
                QToolButton
        ):
            continue

        icon_name = BUTTON_ICON_NAMES.get(
            widget.objectName()
        )

        if icon_name is None:
            continue

        widget.setIcon(
            themed_icon(
                icon_name
            )
        )

