import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi
from yapsy.PluginManager import PluginManager

from api.sarasvati_api import api
from api.models import Brain
from api.plugins import SectionPlugin, ToolboxPlugin
from app.memory_storage import MemoryThoughtsStorage


class App:
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.pluginManager = self.__set_up_plugins_manager()
        self.storage = MemoryThoughtsStorage()
        self.brain = Brain(self.storage)

        api.brain = self.brain
        api.pluginManager = self.pluginManager

    def run(self):
        app = QApplication(sys.argv)
        widget = loadUi(os.path.join(self.path, 'main.ui'))
        section_plugins = self.pluginManager.getPluginsOfCategory("section")
        self.__init_sections(widget, section_plugins)

        widget.show()
        sys.exit(app.exec_())

    @staticmethod
    def __init_sections(widget, plugins):
        for plugin_info in plugins:
            po = plugin_info.plugin_object
            po.activate()
            widget.tabWidget.addTab(po.get_widget(), po.get_section_name())

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
