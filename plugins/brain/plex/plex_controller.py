from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView

from api import api

from .plex import Plex
from .plex_layout import PlexLayout
from .plex_layout_action_executor import PlexLayoutActionExecutor
from .plex_state_diff import PlexStateDiff
from .plex_scene import PlexScene


class PlexController:
    def __init__(self, brain, view):
        self.scene = None
        self.brain = brain
        self.view = view
        self.plex = Plex(self.brain)
        self.differ = PlexStateDiff()
        self.layout = PlexLayout()

        api.events.thoughtSelected.subscribe(self.__on_thought_selected)

        self.__set_up_view_widget()
        self.actions_executor = PlexLayoutActionExecutor(self.scene)

        r = api.brain.create_thought("root")
        c1 = api.brain.create_linked_thought(r, "parent->child", "child")
        c2 = api.brain.create_linked_thought(c1, "parent->child", "child2")
        api.events.thoughtSelected.notify(r)

    def activate(self, thought):
        new_state = self.plex.activate(thought)
        actions = self.layout.change_to(new_state)
        self.actions_executor.run(actions)

    def __set_up_view_widget(self):
        self.scene = PlexScene()
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.view.setSceneRect(0, 0, 25, 25)
        self.view.show()

    def __on_thought_selected(self, thought):
        self.activate(thought)
