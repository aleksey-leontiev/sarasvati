from api.models import Storage


class MemoryStorage(Storage):
    def __init__(self, thoughts=None):
        if thoughts is None:
            self.storage = {}
        else:
            self.storage = thoughts

    def get(self, tid):
        return self.storage[tid]

    def add(self, thought):
        self.storage[thought.get_id()] = thought
