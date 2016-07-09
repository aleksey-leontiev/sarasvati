from .thought import Thought


class Link:
    """
    Link between thoughts
    """
    def __init__(self, source: Thought, destination: Thought, kind):
        """
        Initializes new instance of the Link class
        :param source: Source thought
        :param destination: Destination thought
        :param kind: Kind of link
        """
        self.source = source
        self.destination = destination
        self.kind = kind

    def __eq__(self, other):
        return \
            self.source == other.source and \
            self.destination == other.destination and \
            self.kind == other.kind

    def __repr__(self):
        """
        Returns string representation of instance
        :return: String
        """
        return str(self.source) + " => " + str(self.destination) + " : " + self.kind
