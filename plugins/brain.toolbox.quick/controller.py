from api.api import api


class Controller:
    def __init__(self, widget):
        self.widget = widget

        self.widget.createChildButton.clicked.connect(self.on_create_child_button_clicked)
        self.widget.createParentButton.clicked.connect(self.on_create_parent_button_clicked)

        self.selected_thought = None

        api.events.thoughtSelected.subscribe(self.on_thought_selected)

    def on_thought_selected(self, thought):
        self.selected_thought = thought

    def on_create_child_button_clicked(self):
        if self.selected_thought is None:
            thought = api.brain.create_thought("New Node")
            #api.events.thoughtCreated.notify(thought)
            self.selected_thought = thought
        else:
            thought = api.brain.create_linked_thought(self.selected_thought, "parent->child", "Child Node")
            #api.events.thoughtCreated.notify(thought)

    def on_create_parent_button_clicked(self):
        if self.selected_thought is not None:
            thought = api.brain.create_linked_thought(self.selected_thought, "child->parent", "Parent Node")
            #api.events.thoughtCreated.notify(thought)

