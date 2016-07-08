import uuid

from .interfaces import Model


class Thought(Model):
    def __init__(self):
        super().__init__()
        self.set_title("")
        self.set_field("id", uuid.uuid4().hex)
        self.set_field("links", [])

    def get_id(self):
        return self.get_field("id")

    def get_title(self):
        return self.get_field("title")

    def set_title(self, title):
        self.set_field("title", title)

    def get_links(self):
        return self.get_field("links")

    def add_link(self, thought_id, kind):
        self.dictionary["links"].append({
            "id": thought_id, "kind": kind
        })

    def __repr__(self):
        return "<" + str(self.get_id()) + ": " + self.get_title() + ">"
