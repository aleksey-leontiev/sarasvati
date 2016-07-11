from api import App

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.uic import loadUi


app = QApplication(sys.argv)
widget = loadUi('main.ui')



for pluginInfo in App.pluginManager.getPluginsOfCategory("section"):
    po = pluginInfo.plugin_object
    po.activate()
    widget.tabWidget.addTab(po.get_widget(), po.get_section_name())
    # pluginManager.activatePluginByName(pluginInfo.name)

widget.show()

sys.exit(app.exec_())
