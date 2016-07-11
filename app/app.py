import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi
from yapsy.PluginManager import PluginManager

from api.api import api
from api.event import Event
from api.models import Brain
from api.plugins import SectionPlugin
from app.memory_storage import MemoryThoughtsStorage


class App:
    pluginManager = Event()
    thoughtSelected = Event()
    brain = None

    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.pluginManager = self.__set_up_plugins_manager()
        self.thoughtSelected = Event()
        self.storage = MemoryThoughtsStorage()
        self.brain = Brain(self.storage)

        api.brain = self.brain

    def run(self):
        app = QApplication(sys.argv)
        widget = loadUi(os.path.join(self.path, 'main.ui'))

        for pluginInfo in self.pluginManager.getPluginsOfCategory("section"):
            po = pluginInfo.plugin_object
            po.app = self
            po.activate()

            widget.tabWidget.addTab(po.get_widget(), po.get_section_name())

        widget.show()
        sys.exit(app.exec_())

    @staticmethod
    def __set_up_plugins_manager():
        plugin_manager = PluginManager()
        plugin_manager.setPluginPlaces(["plugins"])
        plugin_manager.setCategoriesFilter({
            "section": SectionPlugin
        })
        plugin_manager.getPluginLocator().setPluginInfoExtension("plugin")
        plugin_manager.collectPlugins()
        return plugin_manager
