import unittest

from api.models import Brain
from plugins.brain.plex import Plex, PlexStateDiff, PlexStateDiffLine
# noinspection PyUnresolvedReferences
from assets import MemoryStorage


class PlexStateDiffMethods(unittest.TestCase):
    def setUp(self):
        self.storage = MemoryStorage()
        self.brain = Brain(self.storage)
        self.plex = Plex(self.brain)
        self.differ = PlexStateDiff()

        # root -> first_child -> child_of_child
        # root -> second_child
        self.root_thought = self.brain.create_thought("root")
        self.first_child = self.brain.create_linked_thought(self.root_thought, "parent->child", "1child")
        self.second_child = self.brain.create_linked_thought(self.root_thought, "parent->child", "2child")
        self.child_of_child = self.brain.create_linked_thought(self.first_child, "parent->child", "child_of_child")

    def test_activate_same_no_diff(self):
        state1 = self.plex.activate(self.root_thought)
        state2 = self.plex.activate(self.root_thought)
        self.assertEqual(self.differ.diff(state1, state2), [])

    def test_activate_root_and_child(self):
        state1 = self.plex.activate(self.root_thought)
        state2 = self.plex.activate(self.first_child)
        expected = [
            PlexStateDiffLine(self.root_thought, "root", "parent"),
            PlexStateDiffLine(self.first_child, "child", "root"),
            PlexStateDiffLine(self.second_child, "child", None),
            PlexStateDiffLine(self.child_of_child, None, "child"),
        ]
        diff = self.differ.diff(state1, state2)

        self.__sort_by_id(diff)
        self.__sort_by_id(expected)
        self.assertEqual(diff, expected)

    def test_activate_root_and_second_child(self):
        state1 = self.plex.activate(self.root_thought)
        state2 = self.plex.activate(self.second_child)
        expected = [
            PlexStateDiffLine(self.root_thought, "root", "parent"),
            PlexStateDiffLine(self.first_child, "child", None),
            PlexStateDiffLine(self.second_child, "child", "root")
        ]
        diff = self.differ.diff(state1, state2)

        self.__sort_by_id(diff)
        self.__sort_by_id(expected)
        self.assertEqual(diff, expected)

    def test_activate_child_of_child_and_first_child(self):
        state1 = self.plex.activate(self.child_of_child)
        state2 = self.plex.activate(self.first_child)
        expected = [
            PlexStateDiffLine(self.root_thought, None, "parent"),
            PlexStateDiffLine(self.first_child, "parent", "root"),
            PlexStateDiffLine(self.child_of_child, "root", "child")
        ]
        diff = self.differ.diff(state1, state2)

        self.__sort_by_id(diff)
        self.__sort_by_id(expected)
        self.assertEqual(diff, expected)

    @staticmethod
    def __sort_by_id(array):
        array.sort(key=lambda t: t.thought.get_id())
