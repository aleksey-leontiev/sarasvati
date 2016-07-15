from api.models import Storage, Thought
from tinydb import TinyDB, Query


class FileStorage(Storage):
    def __init__(self, thoughts=None):
        self.db = TinyDB('database.json')
        if thoughts is not None:
            raise ValueError("not implemented")

    def get_root(self):
        q = Query()
        result = self.db.search(q.root == True)
        if len(result) > 0:
            t = Thought()
            t.from_dictionary(result[0])
            return t
        else:
            return None

    def get(self, tid):
        q = Query()
        result = self.db.search(q.id == tid)
        if len(result) > 0:
            t = Thought()
            t.from_dictionary(result[0])
            return t
        else:
            return None

    def add(self, thought):
        self.db.insert(thought.to_dictionary())

    def update(self, thought):
        q = Query()
        self.db.update(self.__update_operation(thought.to_dictionary()), q.id == thought.get_id())

    def find(self, query):
        raise Exception("Not implemented")

    @staticmethod
    def __update_operation(thought):
        def transform(element):
            element.update(thought)
        return transform

