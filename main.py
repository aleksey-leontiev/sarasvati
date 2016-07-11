from api import App
from api.models import Brain
from memory_thoughts_storage import MemoryThoughtsStorage

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi


qtapp = QApplication(sys.argv)
widget = loadUi('main.ui')


storage = MemoryThoughtsStorage()
App.brain = Brain(storage)


for pluginInfo in App.pluginManager.getPluginsOfCategory("section"):
    po = pluginInfo.plugin_object
    po.activate()
    widget.tabWidget.addTab(po.get_widget(), po.get_section_name())
    # pluginManager.activatePluginByName(pluginInfo.name)

widget.show()

sys.exit(qtapp.exec_())
