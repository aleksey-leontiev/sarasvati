import os

from PyQt5.uic import loadUi

from api import api
from api.plugins import SectionPlugin
from .plex import PlexController


class BrainSectionPlugin(SectionPlugin):
    def __init__(self):
        super().__init__()
        self.widget = None
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.plex_controller = None

    def activate(self):
        path = os.path.join(self.path, 'section.ui')
        self.widget = loadUi(path)
        self.widget.toolBox.removeItem(0)  # remove dummy page

        plugins = api.pluginManager.getPluginsOfCategory("toolbox")
        plugins.sort(key=lambda x: x.plugin_object.get_order())
        for plugin in plugins:
            po = plugin.plugin_object
            po.activate()
            self.widget.toolBox.addItem(po.get_widget(), po.get_section_name())

        self.plex_controller = PlexController(api.brain, self.widget.graphicsView)

    def get_widget(self):
        return self.widget

    def get_section_name(self):
        return 'Brain'
