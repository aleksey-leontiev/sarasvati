from api import api


class Controller:
    def __init__(self, widget):
        self.widget = widget
        self.active_thought = None

        # subscribe for widget's events
        self.widget.createChildButton.clicked.connect(self.__on_create_child_button_clicked)
        self.widget.createParentButton.clicked.connect(self.__on_create_parent_button_clicked)
        self.widget.createJumpButton.clicked.connect(self.__on_create_jump_button_clicked)
        self.widget.title.textChanged.connect(self.__on_title_text_changed)
        self.widget.description.textChanged.connect(self.__on_description_text_changed)

        # app's events
        api.events.thoughtSelected.subscribe(self.__on_thought_selected)
        api.events.thoughtChanged.subscribe(self.__on_thought_updated)

    def __update_controls(self, thought):
        self.widget.title.setText(thought.get_title())
        self.widget.description.setText(thought.get_field("description"))

    def __on_thought_selected(self, thought):
        self.active_thought = thought
        self.__update_controls(thought)

    def __on_thought_updated(self, thought):
        if thought == self.active_thought: # TODO update controls if section tab is not active
            pass

    def __on_create_child_button_clicked(self):
        if self.active_thought is None:
            self.active_thought = api.actions.create_thought("New Node")
        else:
            api.actions.create_linked_thought(self.active_thought, "parent->child", "Child Node")

    def __on_create_parent_button_clicked(self):
        if self.active_thought is not None:
            api.actions.create_linked_thought(self.active_thought, "child->parent", "Parent Node")

    def __on_create_jump_button_clicked(self):
        if self.active_thought is not None:
            api.actions.create_linked_thought(self.active_thought, "jump", "Jump Node")

    def __on_title_text_changed(self):
        if self.active_thought:
            self.active_thought.set_title(self.widget.title.toPlainText())
            api.actions.update_thought(self.active_thought)

    def __on_description_text_changed(self):
        if self.active_thought:
            self.active_thought.set_field("description", self.widget.title.toPlainText())
            api.actions.update_thought(self.active_thought)
