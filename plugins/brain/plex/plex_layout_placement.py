from api.models import Thought
from . import PlexState


class PlexLayoutPlacement:
    def __init__(self):
        self.offset = {"child_x":0}
        self.result = {}

    def place(self, plex_state: PlexState):
        self.offset = {"child_x": 0}
        self.result = {}
        for state in ["root", "parent", "child"]:
            thoughts = plex_state.get_thoughts_by_state(state)
            for thought in thoughts:
                pos = self.__get_pos(state)
                self.result[thought] = pos
        return self.result

    def get_pos(self, thought: Thought):
        return self.result[thought]

    def __get_pos(self, state):
        if state == "root":
            return [0, 0]

        if state == "parent":
            return [0, -100]

        if state == "child":
            x = self.offset["child_x"]
            x += 100
            self.offset["child_x"] += 100
            return [x, 100]