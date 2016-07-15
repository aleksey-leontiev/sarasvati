from yapsy.IPlugin import IPlugin


class ToolboxPlugin(IPlugin):
    def get_widget(self):
        pass

    def get_section_name(self):
        pass

    def get_order(self):
        return 0
