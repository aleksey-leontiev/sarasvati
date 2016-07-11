import unittest

from api.models import Brain
from plugins.brain.plex import Plex
# noinspection PyUnresolvedReferences
from assets import MemoryThoughtsStorage


class PlexMethods(unittest.TestCase):
    def setUp(self):
        self.storage = MemoryThoughtsStorage()
        self.brain = Brain(self.storage)
        self.plex = Plex(self.brain)

        # root -> 1child -> child_of_child
        # root -> 2child
        self.root_thought = self.brain.create_thought("root")
        self.first_child = self.brain.create_linked_thought(self.root_thought, "parent->child", "1child")
        self.second_child = self.brain.create_linked_thought(self.root_thought, "parent->child", "2child")
        self.child_of_child = self.brain.create_linked_thought(self.first_child, "parent->child", "child_of_child")

    def test_activate_root(self):
        layout1 = self.plex.activate(self.root_thought)
        self.assertEqual(layout1.get_thoughts_by_state("root"), [self.root_thought])
        self.assertEqual(layout1.get_thoughts_by_state("child"), [self.first_child, self.second_child])
        self.assertEqual(len(layout1.get_state()), 3)

    def test_activate_first_child(self):
        layout1 = self.plex.activate(self.first_child)
        self.assertEqual(layout1.get_thoughts_by_state("parent"), [self.root_thought])
        self.assertEqual(layout1.get_thoughts_by_state("root"), [self.first_child])
        self.assertEqual(layout1.get_thoughts_by_state("child"), [self.child_of_child])
        self.assertEqual(len(layout1.get_state()), 3)

    def test_activate_second_child(self):
        layout1 = self.plex.activate(self.second_child)
        self.assertEqual(layout1.get_thoughts_by_state("parent"), [self.root_thought])
        self.assertEqual(layout1.get_thoughts_by_state("root"), [self.second_child])
        self.assertEqual(layout1.get_thoughts_by_state("child"), [])
        self.assertEqual(len(layout1.get_state()), 2)
