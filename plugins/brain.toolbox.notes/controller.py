from api import api


class Controller:
    def __init__(self, widget):
        self.widget = widget
        self.active_thought = None

        # subscribe for widget's events
        self.widget.text.textChanged.connect(self.__on_text_changed)

        # app's events
        api.events.thoughtSelected.subscribe(self.__on_thought_selected)

    def __update_controls(self, thought):
        self.widget.text.setText(thought.get_field("notes"))

    def __on_thought_selected(self, thought):
        self.active_thought = thought
        self.__update_controls(thought)

    def __on_text_changed(self):
        if self.active_thought is not None:
            self.active_thought.set_field("notes", self.widget.text.toPlainText())
            api.actions.update_thought(self.active_thought)