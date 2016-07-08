import unittest

from api.models import Plex, Brain, PlexStateDiff
# noinspection PyUnresolvedReferences
from assets import MemoryThoughtsStorage


class PlexStateDiffMethods(unittest.TestCase):
    def setUp(self):
        self.storage = MemoryThoughtsStorage()
        self.brain = Brain(self.storage)
        self.plex = Plex(self.brain)
        self.diff = PlexStateDiff()

        # root -> first_child -> child_of_child
        # root -> second_child
        self.root_thought = self.brain.create_thought("root")
        self.first_child = self.brain.create_linked_thought(self.root_thought, "parent->child", "1child")
        self.second_child = self.brain.create_linked_thought(self.root_thought, "parent->child", "2child")
        self.child_of_child = self.brain.create_linked_thought(self.first_child, "parent->child", "child_of_child")

        # required for right ordering. expected array should go in same order
        self.root_thought.set_field("id", "1")
        self.first_child.set_field("id", "2")
        self.second_child.set_field("id", "3")
        self.child_of_child.set_field("id", "4")

    def test_activate_same_no_diff(self):
        state1 = self.plex.activate(self.root_thought)
        state2 = self.plex.activate(self.root_thought)
        self.assertEqual(self.diff.diff(state1, state2), [])

    def test_activate_root_and_child(self):
        state1 = self.plex.activate(self.root_thought)
        state2 = self.plex.activate(self.first_child)
        expected = [
            [self.root_thought, "root", "parent"],
            [self.first_child, "child", "root"],
            [self.second_child, "child", None],
            [self.child_of_child, None, "child"],
        ]
        diff = self.diff.diff(state1, state2)
        self.assertEqual(diff, expected)

    def test_activate_root_and_second_child(self):
        state1 = self.plex.activate(self.root_thought)
        state2 = self.plex.activate(self.second_child)
        expected = [
            [self.root_thought, "root", "parent"],
            [self.first_child, "child", None],
            [self.second_child, "child", "root"]
        ]
        diff = self.diff.diff(state1, state2)
        self.assertEqual(diff, expected)

    def test_activate_child_of_child_and_first_child(self):
        state1 = self.plex.activate(self.child_of_child)
        state2 = self.plex.activate(self.first_child)
        expected = [
            [self.root_thought, None, "parent"],
            [self.first_child, "parent", "root"],
            [self.child_of_child, "root", "child"]
        ]
        diff = self.diff.diff(state1, state2)
        self.assertEqual(diff, expected)