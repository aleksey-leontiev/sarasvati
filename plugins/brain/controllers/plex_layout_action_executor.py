from PyQt5.QtCore import QPointF

from api.models import Thought
from ..models import PlexLayoutAction
from ..widgets import Node


class PlexLayoutActionExecutor:
    def __init__(self, scene):
        self.scene = scene

    def run(self, actions):
        for action in actions:
            if action.name == "add":
                self.add_thought(action.thought)
            if action.name == "move_to":
                node = self.get_node(action.thought)
                node.setPos(QPointF(action.data[0], action.data[1]))
            if action.name == "remove":
                self.remove_thought(action.thought)

    def add_thought(self, thought):
        node = Node(thought)
        self.scene.addItem(node)

    def remove_thought(self, thought):
        node = self.get_node(thought)
        self.scene.removeItem(node)
        pass

    def change_thought_state(self, thought, new_state):
        node = self.get_node(thought)
        pass

    def get_node(self, thought) -> Node:
        for item in self.scene.items():
            if item.thought.get_id() == thought.get_id():
                return item
