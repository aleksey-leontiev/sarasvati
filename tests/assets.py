from api.models import ThoughtsStorage


class MemoryThoughtsStorage(ThoughtsStorage):
    def __init__(self, thoughts=None):
        if thoughts is None:
            self.storage = {}
        else:
            self.storage = thoughts

    def get_thought(self, id):
        return self.storage[id]

    def add_thought(self, thought):
        self.storage[thought.get_id()] = thought