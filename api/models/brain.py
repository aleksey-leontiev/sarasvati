from api.event import Event
from api.models.interfaces.thoughtsstorage import ThoughtsStorage
from .thought import Thought


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
        self.thoughtCreated = Event()

    def get_thought(self, tid) -> Thought:
        """
        Returns thought by specified id. None if does not exist.
        :rtype: Thought
        :param tid: Id of the thought
        :return: Thought
        """
        return self.storage.get_thought(tid)

    def add_thought(self, thought: Thought):
        # TODO: looks like useless (no references found
        """
        Adds thought to the brain
        :param thought: Thought to be added
        """
        if not self.storage.exist(thought.get_id()):
            self.storage.add_thought(thought)

    def create_thought(self, title) -> Thought:
        """
        Creates new thought using specified title
        :rtype: Thought
        :param title: Title
        :return: Thought
        """
        new_thought = Thought()
        new_thought.set_title(title)
        self.storage.add_thought(new_thought)
        self.thoughtCreated.notify(new_thought)
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
        self.storage.add_thought(new_thought)
        self.thoughtCreated.notify(new_thought)
        return new_thought

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