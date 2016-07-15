from api import api


class Controller:
    def __init__(self, widget):
        self.widget = widget
        self.active_thought = None
        self.brain = api.brain

        # prepare form
        self.widget.linkType.addItem("parent")
        self.widget.linkType.addItem("child")
        self.widget.linkType.addItem("jump")

        # subscribe for widget's events
        self.widget.thoughtTitle.currentTextChanged.connect(self.__on_text_changed)
        self.widget.createLink.clicked.connect(self.__on_create_link_clicked)

        # app's events
        api.events.thoughtSelected.subscribe(self.__on_thought_selected)

    def __on_thought_selected(self, thought):
        self.active_thought = thought

    def __on_text_changed(self):
        pass

    def __on_create_link_clicked(self):
        to_title = self.widget.thoughtTitle.currentText()
        result = self.brain.find_thoughts({"title": to_title})

        if len(result) == 1:
            kind = self.widget.linkType.currentText()
            self.brain.link_thoughts(self.active_thought, result[0], kind)
            api.actions.update_thought(self.active_thought)
            api.actions.update_thought(result[0])
