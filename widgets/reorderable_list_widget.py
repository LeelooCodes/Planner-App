from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import (
    QCursor,
    QDrag,
    QPainter,
    QPixmap,
)
from PySide6.QtWidgets import (
    QFrame,
    QListWidget,
)


class ReorderableListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Use real spacing between cards instead of QSS margins.
        self.setSpacing(10)

        # Hide Qt's native drop indicator.
        self.setDropIndicatorShown(False)

        # Custom insertion line drawn over the list viewport.
        self.drop_indicator = QFrame(
            self.viewport()
        )

        self.drop_indicator.setObjectName(
            "customDropIndicator"
        )

        self.drop_indicator.setFixedHeight(3)
        self.drop_indicator.hide()

    def startDrag(self, supported_actions):
        selected_items = self.selectedItems()

        if not selected_items:
            return

        item = selected_items[0]

        dragged_widget = self.itemWidget(
            item
        )

        drag = QDrag(self)

        mime_data = self.model().mimeData(
            self.selectedIndexes()
        )

        drag.setMimeData(
            mime_data
        )

        if dragged_widget is not None:
            source_pixmap = QPixmap(
                dragged_widget.size()
            )

            source_pixmap.fill(
                Qt.GlobalColor.transparent
            )

            dragged_widget.render(
                source_pixmap
            )

            transparent_pixmap = QPixmap(
                source_pixmap.size()
            )

            transparent_pixmap.fill(
                Qt.GlobalColor.transparent
            )

            painter = QPainter(
                transparent_pixmap
            )

            painter.setOpacity(
                0.5
            )

            painter.drawPixmap(
                0,
                0,
                source_pixmap
            )

            painter.end()

            drag.setPixmap(
                transparent_pixmap
            )

            cursor_position = (
                dragged_widget.mapFromGlobal(
                    QCursor.pos()
                )
            )

            drag.setHotSpot(
                QPoint(
                    cursor_position.x(),
                    cursor_position.y()
                )
            )

        drag.exec(
            Qt.DropAction.MoveAction
        )

    def dragEnterEvent(self, event):
        super().dragEnterEvent(event)

        if event.isAccepted():
            self._update_drop_indicator(
                event.position().toPoint()
            )

    def dragMoveEvent(self, event):
        super().dragMoveEvent(event)

        if event.isAccepted():
            self._update_drop_indicator(
                event.position().toPoint()
            )

    def dragLeaveEvent(self, event):
        self._hide_drop_indicator()

        super().dragLeaveEvent(event)

    def dropEvent(self, event):
        self._hide_drop_indicator()

        super().dropEvent(event)

    def _update_drop_indicator(
            self,
            position
    ):
        indicator_y = (
            self._calculate_indicator_y(
                position.y()
            )
        )

        indicator_height = (
            self.drop_indicator.height()
        )

        indicator_y = max(
            0,
            min(
                indicator_y,
                (
                    self.viewport().height()
                    - indicator_height
                )
            )
        )

        self.drop_indicator.setGeometry(
            8,
            indicator_y,
            max(
                0,
                self.viewport().width() - 16
            ),
            indicator_height
        )

        self.drop_indicator.raise_()
        self.drop_indicator.show()

    def _calculate_indicator_y(
            self,
            pointer_y
    ):
        if self.count() == 0:
            return 2

        spacing = self.spacing()

        for row in range(
            self.count()
        ):
            current_rect = (
                self.visualItemRect(
                    self.item(row)
                )
            )

            if (
                pointer_y
                < current_rect.center().y()
            ):
                if row == 0:
                    return max(
                        1,
                        current_rect.top()
                        - spacing // 2
                    )

                previous_rect = (
                    self.visualItemRect(
                        self.item(row - 1)
                    )
                )

                return (
                    previous_rect.bottom()
                    + current_rect.top()
                ) // 2

        last_rect = self.visualItemRect(
            self.item(
                self.count() - 1
            )
        )

        return (
            last_rect.bottom()
            + spacing // 2
        )

    def _hide_drop_indicator(self):
        self.drop_indicator.hide()