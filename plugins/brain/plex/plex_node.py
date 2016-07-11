from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QGraphicsWidget

from api.app import App


class PlexNode(QGraphicsWidget):
    maxBounding = QRectF(0, 0, 150, 150)

    def __init__(self, thought):
        super(PlexNode, self).__init__()
        self.thought = thought
        self.boundingRect = QRectF(0, 0, 0, 0)

    # noinspection PyMethodOverriding
    def paint(self, painter, option, widget):
        self.boundingRect = painter.drawText(self.maxBounding, Qt.TextWordWrap, self.thought.get_title())

    def boundingRect(self):
        return self.boundingRect

    def mousePressEvent(self, event):
        App.select_thought(self.thought)