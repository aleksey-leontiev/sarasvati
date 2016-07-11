from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtWidgets import QGraphicsWidget

from api import api


class PlexNode(QGraphicsWidget):
    maxBounding = QRectF(0, 0, 150, 150)

    def __init__(self, thought):
        super(PlexNode, self).__init__()
        self.thought = thought
        self.boundingRect = QRectF(0, 0, 0, 0)
        self.animations = []

    # noinspection PyMethodOverriding
    def paint(self, painter, option, widget):
        self.boundingRect = painter.drawText(self.maxBounding, Qt.TextWordWrap, self.thought.get_title())

    def boundingRect(self):
        return self.boundingRect

    def mousePressEvent(self, event):
        api.events.thoughtSelected.notify(self.thought)
