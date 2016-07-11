from PyQt5.QtCore import QPointF


from .actions import MovePlexNodeAction, OpacityPlexNodeAction
from .plex_node import PlexNode


class PlexLayoutActionExecutor:
    def __init__(self, scene):
        self.scene = scene
        self.actions = []

    def run(self, actions):
        for action in actions:
            if action.name == "add":
                self.add_thought(action.thought)
            if action.name == "move_to":
                pos = QPointF(action.data[0], action.data[1])
                self.move_thought(action.thought, pos)
            if action.name == "remove":
                self.remove_thought(action.thought)

    def add_thought(self, thought):
        node = PlexNode(thought)
        action = OpacityPlexNodeAction(node, 0, 1)
        action.completed.subscribe(self.__on_action_completed)
        self.actions.append(action)
        self.scene.addItem(node)

    def remove_thought(self, thought):
        node = self.scene.get_node(thought)
        action = OpacityPlexNodeAction(node, node.opacity(), 0)
        action.completed.subscribe(self.__remove_node)
        action.completed.subscribe(self.__on_action_completed)
        self.actions.append(action)

    def move_thought(self, thought, point):
        node = self.scene.get_node(thought)
        action = MovePlexNodeAction(node, point)
        action.completed.subscribe(self.__on_action_completed)
        self.actions.append(action)

    def __on_action_completed(self, action):
        action.completed.unsubscribe(self.__on_action_completed)
        self.actions.remove(action)

    def __remove_node(self, action):
        self.scene.removeItem(action.node)

