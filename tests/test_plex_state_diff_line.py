import unittest

from api.models import Thought
from plugins.brain.plex import PlexStateDiffLine


class PlexStateDiffLineMethods(unittest.TestCase):
    def test_init(self):
        t1 = Thought()
        state1 = PlexStateDiffLine(t1, "root", "child")
        self.assertEqual(state1.thought, t1)
        self.assertEqual(state1.old_state, "root")
        self.assertEqual(state1.new_state, "child")

    def test_eq(self):
        t1 = Thought()
        state1 = PlexStateDiffLine(t1, "root", "child")
        state2 = PlexStateDiffLine(t1, "root", "child")
        self.assertEqual(state1, state2)

    def test_not_eq(self):
        t1 = Thought()
        t2 = Thought()
        state1 = PlexStateDiffLine(t1, "root", "child")
        state2 = PlexStateDiffLine(t2, "root", "child")
        self.assertNotEqual(state1, state2)
