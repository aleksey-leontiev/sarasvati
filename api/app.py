from yapsy.PluginManager import PluginManager

from .event import Event
from .plugins import SectionPlugin


class App:
    pluginManager = None
    thoughtSelected = None
    brain = None

    def __init__(self):
        App.pluginManager = self.__set_up_plugins_manager()
        App.thoughtSelected = Event()

    @staticmethod
    def select_thought(thought):
        App.thoughtSelected.notify(thought)

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

app = App()