import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi
from yapsy.PluginManager import PluginManager

from api.api import api
from api.models import Brain
from api.plugins import SectionPlugin, ToolboxPlugin
from app.memory_storage import MemoryThoughtsStorage


class App:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.pluginManager = self.__set_up_plugins_manager()
        self.storage = MemoryThoughtsStorage()
        self.brain = Brain(self.storage)
        self.root = None
        self.app = None

        api.brain = self.brain
        api.pluginManager = self.pluginManager

    def run(self, test=False):
        self.app = QApplication(sys.argv)
        widget = loadUi(os.path.join(self.path, 'main.ui'))
        self.root = widget

        for pluginInfo in self.pluginManager.getPluginsOfCategory("section"):
            po = pluginInfo.plugin_object
            po.app = self
            po.activate()

            widget.tabWidget.addTab(po.get_widget(), po.get_section_name())

        if not test:
            widget.show()
            sys.exit(self.app.exec_())

    @staticmethod
    def __set_up_plugins_manager():
        plugin_manager = PluginManager()
        plugin_manager.setPluginPlaces(["plugins"])
        plugin_manager.setCategoriesFilter({
            "section": SectionPlugin,
            "toolbox": ToolboxPlugin
        })
        plugin_manager.getPluginLocator().setPluginInfoExtension("plugin")
        plugin_manager.collectPlugins()
        return plugin_manager
