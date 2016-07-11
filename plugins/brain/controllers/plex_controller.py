from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView

from api.app import App
from ..controllers.plex_layout_action_executor import PlexLayoutActionExecutor  # TODO ..controllers.plex_layout_action_executor ??
from ..models import Plex, PlexStateDiff, PlexLayout


class PlexController:
    def __init__(self, brain, view):
        self.scene = None
        self.brain = brain
        self.view = view
        self.plex = Plex(self.brain)
        self.differ = PlexStateDiff()
        self.layout = PlexLayout()

        App.thoughtSelected.subscribe(self.on_thought_selected)

        self.__set_up_view_widget()
        self.actions_executor = PlexLayoutActionExecutor(self.scene)

        self.r = brain.create_thought("root")
        self.c = brain.create_linked_thought(self.r, "parent->child", "child")
        self.c2 = brain.create_linked_thought(self.r, "parent->child", "child2")
        self.c3 = brain.create_linked_thought(self.c, "parent->child", "child3")
        self.activate(self.r)

    def on_thought_selected(self, thought):
        self.activate(thought)

    def activate(self, thought):
        new_state = self.plex.activate(thought)
        actions = self.layout.change_to(new_state)
        self.actions_executor.run(actions)

    def __set_up_view_widget(self):
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.view.setSceneRect(0, 0, 25, 25)
        self.view.show()
