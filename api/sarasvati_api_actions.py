
class SarasvatiApiActions:
    def __init__(self, api):
        self.api = api

    def create_thought(self, title):
        thought = self.api.brain.create_thought(title)
        self.api.events.thoughtCreated.notify(thought)
        return thought

    def create_linked_thought(self, root, kind, title):
        thought = self.api.brain.create_linked_thought(root, kind, title)
        self.api.events.thoughtCreated.notify(thought)
        return thought

    def update_thought(self, thought):
        self.api.brain.update_thought(thought)
        self.api.events.thoughtChanged.notify(thought)
