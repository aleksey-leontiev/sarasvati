from .plex_state import PlexState

from ..brain import Brain
from ..thought import Thought


class Plex:
    """
    Plex is a slice of the brain
    """
    def __init__(self, brain: Brain):
        """
        Initializes new instance of the Brain class
        :param brain: Brain to get data from
        """
        self.brain = brain

    def activate(self, thought: Thought) -> PlexState:
        """
        Activate thought
        :param thought: Thought
        :return: State of the plex
        """
        state = PlexState()
        state.add(thought, "root")

        for link in thought.get_links():
            loading_thought_id = link["id"]
            link_kind = link["kind"]
            loaded_thought = self.brain.get_thought(loading_thought_id)
            state.add(loaded_thought, link_kind)

        return state
