from .plex_state import PlexState


class PlexStateDiff:
    @staticmethod
    def diff(old: PlexState, new: PlexState):
        """
        Return difference between two specified view states
        :param old: Old state
        :param new: New state
        :return: Array of PlexThoughtState
        """
        result = []
        ids = PlexStateDiff.get_ids(new, old)

        for tid in ids:
            o = old.get_state_by_thought_id(tid)
            n = new.get_state_by_thought_id(tid)
            t = PlexStateDiff.get_thought_from_states(o, n, tid)

            if o is None or n is None:
                if o is None:
                    result.append([t, None, n.state])
                else:
                    result.append([t, o.state, None])
            elif o.state != n.state:
                result.append([t, o.state, n.state])

        result.sort(key=lambda t: t[0].get_id())
        print(result)
        return result

    @staticmethod
    def get_ids(new, old):
        ids = []
        for state in old.get_state():
            if state.thought.get_id() not in ids:
                ids.append(state.thought.get_id())
        for state in new.get_state():
            if state.thought.get_id() not in ids:
                ids.append(state.thought.get_id())
        # a = old.get_state()[:]
        # a.extend(new.get_state())
        # ids = list(set(map(lambda x: x.thought.get_id(), a)))
        # print(ids)
        return ids

    @staticmethod
    def get_thought_from_states(old, new, tid):
        if old is not None:
            return old.thought
        if new is not None:
            return new.thought
