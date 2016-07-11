from PyQt5.QtWidgets import QGraphicsScene

from .plex_node import PlexNode


class PlexScene(QGraphicsScene):
    def get_node(self, thought) -> PlexNode:
        for item in self.items():
            if item.thought.get_id() == thought.get_id():
                return item
