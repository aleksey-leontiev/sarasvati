class PlexStateDiffLine:
    def __init__(self, thought, old_state, new_state):
        self.thought = thought
        self.old_state = old_state
        self.new_state = new_state

    def __eq__(self, other):
        return self.thought == other.thought and \
            self.old_state == other.old_state and \
            self.new_state == other.new_state