from .plex import PlexState
from .plex_state_diff import PlexStateDiff
from .plex_layout_action import PlexLayoutAction


class PlexLayout:
    def __init__(self):
        self.old_state = PlexState()
        self.state = PlexState()
        self.differ = PlexStateDiff()
        self.offset = self.clear_offset()

    def change_to(self, new_state) -> []:
        self.offset = self.clear_offset()
        result = []
        diffs = self.differ.diff(self.old_state, new_state)
        for diff in diffs:
            if diff.old_state is None:
                kind = "parent"
                if diff.new_state == "parent":
                    kind = "child"

                parent_thought = self.get_linked(diff.thought, kind)
                pos = self.get_pos(diff.new_state)
                result.append(PlexLayoutAction(diff.thought, "add"))
                if parent_thought:
                    result.append(PlexLayoutAction(diff.thought, "set_pos_to", parent_thought))
                result.append(PlexLayoutAction(diff.thought, "move_to", pos))
            elif diff.new_state is None:
                parent_thought = self.get_linked(diff.thought, "parent")
                if parent_thought:
                    result.append(PlexLayoutAction(diff.thought, "move_to", parent_thought))
                result.append(PlexLayoutAction(diff.thought, "remove"))
            else:
                pos = self.get_pos(diff.new_state)
                result.append(PlexLayoutAction(diff.thought, "move_to", pos))
        self.old_state = new_state
        return result

    def get_linked(self, thought, kind):
        parents = thought.get_links_by_kind(kind)
        for parent in parents:
            id = parent["id"]
            state = self.old_state.get_state_by_thought_id(id)
            if state is not None:
                return state.thought
        return None

    def get_pos(self, state):
        if state == "root":
            return [0, 0]

        if state == "parent":
            return [0, -100]

        if state == "child":
            x = self.offset["child_x"]
            x += 100
            self.offset["child_x"] += 100
            return [x, 100]

    def clear_offset(self):
        return {"child_x":0}