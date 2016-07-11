import os

from PyQt5.uic import loadUi

from api.models import MemoryThoughtsStorage, Brain
from api.plugins import SectionPlugin

from .plex import PlexController


class BrainSectionPlugin(SectionPlugin):
    def __init__(self):
        super().__init__()
        self.widget = None
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.plex_controller = None
        self.brain = None
        self.storage = None

    def activate(self):
        path = os.path.join(self.path, 'section.ui')
        self.widget = loadUi(path)
        self.storage = MemoryThoughtsStorage()
        self.brain = Brain(self.storage)

        self.plex_controller = PlexController(self.brain, self.widget.graphicsView)

    def get_widget(self):
        return self.widget

    def get_section_name(self):
        return 'Brain'
