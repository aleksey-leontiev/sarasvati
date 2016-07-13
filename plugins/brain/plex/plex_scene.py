from PyQt5.QtCore import QPointF, QMarginsF
from PyQt5.QtGui import QPainter, QPainterPath, QPen, QColor
from PyQt5.QtWidgets import QGraphicsScene

from .plex_node import PlexNode


class PlexScene(QGraphicsScene):
    def get_node(self, thought) -> PlexNode:
        for item in self.items():
            if item.thought.get_id() == thought.get_id():
                return item

    def get_node_by_id(self, thought_id) -> PlexNode:
        for item in self.items():
            if item.thought.get_id() == thought_id:
                return item

    def drawBackground(self, painter, rect):
        painter.setRenderHint(QPainter.Antialiasing)
        for item in self.items():
            for link in item.thought.get_links():
                link_id = link["id"]
                link_kind = link["kind"]
                if link_kind == "child":
                    node = self.get_node_by_id(link_id)
                    if node:
                        self.__draw_link(painter, item, node)

    @staticmethod
    def __draw_link(painter, src, dst):
        margins = QMarginsF(10, 10, 10, 10)
        opacity = min(dst.opacity(), src.opacity()) * 255

        src_geometry = src.geometry().marginsAdded(margins)
        dst_geometry = dst.geometry().marginsAdded(margins)
        src_center = src_geometry.center()
        dst_center = dst_geometry.center()
        src_offset = QPointF(0, src_geometry.height() / 2)
        dst_offset = QPointF(0, dst_geometry.height() / 2)

        start_point = src_center + src_offset
        end_point = dst_center - dst_offset
        control_point1 = start_point + QPointF(0, 50)
        control_point2 = end_point - QPointF(0, 50)

        cubic_path = QPainterPath(start_point)
        cubic_path.cubicTo(control_point1, control_point2, end_point)

        painter.setPen(QPen(QColor(0, 0, 0, opacity)))
        painter.drawPath(cubic_path)
