import uuid

from .interfaces import Model


class Thought(Model):
    def __init__(self):
        """
        Initializes new instance of the Thought class
        """
        super().__init__()
        self.set_title("")
        self.set_field("id", uuid.uuid4().hex)
        self.set_field("links", [])

    def get_id(self):
        """
        Return id of the thought
        :return: Id
        """
        return self.get_field("id")

    def get_title(self):
        """
        Returns title of the thought
        :return: Title
        """
        return self.get_field("title")

    def set_title(self, title):
        """
        Sets title of the thought
        :param title: Tile to set
        """
        self.set_field("title", title)

    def get_links(self):
        """
        Returns links
        :return: List of links
        """
        return self.get_field("links")

    def get_links_by_kind(self, kind):
        """
        Returns links
        :return: List of links
        """
        return [link for link in self.get_links() if link["kind"] == kind]

    def add_link(self, thought_id, kind):
        """
        Adds link. If link with same id exist ValueError will raise
        :param thought_id: Thought id to link to
        :param kind: Kind of link
        """
        link = {"id": thought_id, "kind": kind}
        links = self.dictionary["links"]
        if link in links:
            raise ValueError("Link with same id already exist")
        links.append(link)

    def remove_link(self, thought_id):
        """
        Removes link
        :param thought_id: Thought id
        """
        for link in self.get_links():
            if link["id"] == thought_id:
                self.dictionary["links"].remove(link)

    def __eq__(self, other):
        return self.get_id() == other.get_id()

    def __repr__(self):
        """
        Returns string representation of instance
        :return:
        """
        return "<" + str(self.get_id()) + ": " + self.get_title() + ">"
