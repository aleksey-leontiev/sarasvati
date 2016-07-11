from .plex_thought_state import PlexThoughtState


class PlexState:
    def __init__(self):
        """
        Initializes new instance of the PlexState class
        """
        self.state = []

    def add(self, thought, state):
        """
        Adds thought using specified state
        :param thought: Thought
        :param state: State
        """
        self.state.append(PlexThoughtState(thought, state))

    def get_state(self):
        """
        Returns state
        :return: Array of PlexThoughtState
        """
        return self.state

    def get_thoughts_by_state(self, state):
        """
        Returns array of thoughts using specified state
        :param state: State
        :return: Array of thoughts
        """
        return [e.thought for e in self.state if e.state == state]

    def get_state_by_thought_id(self, id):
        # TODO: refactor using next()
        """
        Returns state by specified thought id
        :param id: Thought id
        :return: PlexThoughtState
        """
        for ptp in self.state:
            if ptp.thought.get_id() == id:
                return ptp
