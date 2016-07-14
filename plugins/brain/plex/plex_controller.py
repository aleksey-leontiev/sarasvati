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
        self.active_thought = None

        api.events.thoughtSelected.subscribe(self.__on_thought_selected)
        api.events.thoughtCreated.subscribe(self.__on_thought_created)
        api.events.thoughtChanged.subscribe(self.__on_thought_changed)

        self.__set_up_view_widget()
        self.actions_executor = PlexLayoutActionExecutor(self.scene)

        root_thought = self.brain.get_root_thought()
        #self.activate(root_thought)
        api.events.thoughtSelected.notify(root_thought)

    def activate(self, thought):
        self.active_thought = thought
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

    def __on_thought_created(self, thought):
        if self.active_thought:
            self.activate(self.active_thought)
        else:
            self.activate(thought)

    def __on_thought_changed(self, thought):
        node = self.scene.get_node(thought)
        if node:
            node.update()
