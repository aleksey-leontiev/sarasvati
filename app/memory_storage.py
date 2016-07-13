from api.models import ThoughtsStorage


class MemoryThoughtsStorage(ThoughtsStorage):
    def __init__(self, thoughts=None):
        if thoughts is None:
            self.storage = {}
        else:
            self.storage = thoughts

    def get_thought(self, tid):
        return self.storage[tid]

    def add_thought(self, thought):
        self.storage[thought.get_id()] = thought

    def find(self, query):
        result = []
        for tid in self.storage:
            thought = self.storage[tid]
            if "title" in query:
                if thought.get_title() == query["title"]:
                    result.append(thought)
        return result

