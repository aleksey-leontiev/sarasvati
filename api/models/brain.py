from .interfaces import ThoughtsStorage
from .thought import Thought
from .link import Link


class Brain:
    """
    Brain
    """
    def __init__(self, storage: ThoughtsStorage):
        """
        Initializes new instance of the Brain
        :param storage: Place to store thoughts in
        """
        self.storage = storage

        # init root thought
        self.root = storage.get_root()
        if self.root is None:
            self.root = self.create_thought("Root")
            self.root.set_field("root", True)

    def get_root_thought(self) -> Thought:
        """
        Returns root thought
        :return: Thought
        """
        return self.root

    def get_thought(self, tid) -> Thought:
        """
        Returns thought by specified id. None if does not exist.
        :rtype: Thought
        :param tid: Id of the thought
        :return: Thought
        """
        return self.storage.get(tid)

    def get_links(self, thought: Thought):
        """
        Returns links of specified thought
        :param thought: Thought to get links from
        :return: Array of Link
        """
        result = []
        for link in thought.get_links():
            destination = self.get_thought(link["id"])
            kind = link["kind"]
            link = Link(thought, destination, kind)
            result.append(link)
        return result

    def add_thought(self, thought: Thought):
        # TODO: looks like useless (no references found)
        """
        Adds thought to the brain
        :param thought: Thought to be added
        """
        if not self.storage.exist(thought.get_id()):
            self.storage.add(thought)

    def create_thought(self, title) -> Thought:
        """
        Creates new thought using specified title
        :rtype: Thought
        :param title: Title
        :return: Thought
        """
        new_thought = Thought()
        new_thought.set_title(title)
        self.storage.add(new_thought)
        return new_thought

    def create_linked_thought(self, root: Thought, kind, title) -> Thought:
        """
        Creates linked thought
        :rtype: Thought
        :param root: Linked thought
        :param kind: Kind of link
        :param title: New thought title
        :return: Thought
        """
        new_thought = Thought()
        new_thought.set_title(title)
        self.link_thoughts(root, new_thought, kind)
        self.storage.add(new_thought)
        self.storage.update(root)
        return new_thought

    def update_thought(self, thought):
        self.storage.update(thought)

    def find_thoughts(self, query):
        return self.storage.find(query)

    @staticmethod
    def link_thoughts(source: Thought, destination: Thought, kind):
        """
        Links two thoughts
        :param source: Link from
        :param destination: Link to
        :param kind: Kind of link
        """
        if kind == "parent->child":
            source.add_link(destination.get_id(), "child")
            destination.add_link(source.get_id(), "parent")
        elif kind == "child->parent":
            source.add_link(destination.get_id(), "parent")
            destination.add_link(source.get_id(), "child")
        elif kind == "jump":
            source.add_link(destination.get_id(), "jump")
            destination.add_link(source.get_id(), "jump")
        else:
            raise ValueError("Wrong link kind")

    @staticmethod
    def get_link_type(source: Thought, destination: Thought):
        """
        Returns link type
        :param source: Source thought
        :param destination: Destination thought
        :return: Kind of link
        """
        for link in source.get_links():
            if link["id"] == destination.get_id():
                return link["kind"]
        return None

    @staticmethod
    def is_linked(source: Thought, destination: Thought):
        """
        Are thoughts linked?
        :param source: Source thought
        :param destination: Destination thought
        :return: True if thoughts connected, otherwise False
        """
        return Brain.get_link_type(source, destination) is not None
