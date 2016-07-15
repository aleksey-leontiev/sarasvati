import unittest

from api.models import Brain
# noinspection PyUnresolvedReferences
from assets import MemoryStorage

from plugins.brain.plex import PlexLayout, Plex, PlexLayoutAction


class PlexLayoutMethods(unittest.TestCase):
    def setUp(self):
        self.storage = MemoryStorage()
        self.brain = Brain(self.storage)
        self.plex = Plex(self.brain)
        self.layout = PlexLayout()

        # root -> 1child -> child_of_child
        # root -> 2child
        self.root = self.brain.create_thought("root")
        self.child1 = self.brain.create_linked_thought(self.root, "parent->child", "1child")
        self.child2 = self.brain.create_linked_thought(self.root, "parent->child", "2child")
        self.child3 = self.brain.create_linked_thought(self.child1, "parent->child", "3child")

    def test_root(self):
        state = self.plex.activate(self.root)
        actions = self.layout.change_to(state)
        expected = [
            PlexLayoutAction(self.root, "add", None),
            PlexLayoutAction(self.root, "move_to", [0, 0]),
            PlexLayoutAction(self.child1, "add", None),
            PlexLayoutAction(self.child1, "move_to",  [100, 100]),
            PlexLayoutAction(self.child2, "add", None),
            PlexLayoutAction(self.child2, "move_to", [200, 100])
        ]
        self.assertEqual(actions, expected)

    def test_child1(self):
        state = self.plex.activate(self.child1)
        actions = self.layout.change_to(state)
        expected = [
            PlexLayoutAction(self.child1, "add", None),
            PlexLayoutAction(self.child1, "move_to", [0, 0]),
            PlexLayoutAction(self.root, "add", None),
            PlexLayoutAction(self.root, "move_to", [0, -100]),
            PlexLayoutAction(self.child3, "add", None),
            PlexLayoutAction(self.child3, "move_to", [100, 100])
        ]
        self.assertEqual(actions, expected)

    def test_child3(self):
        state = self.plex.activate(self.child3)
        actions = self.layout.change_to(state)
        expected = [
            PlexLayoutAction(self.child3, "add", None),
            PlexLayoutAction(self.child3, "move_to", [0, 0]),
            PlexLayoutAction(self.child1, "add", None),
            PlexLayoutAction(self.child1, "move_to", [0, -100]),
        ]
        self.assertEqual(actions, expected)

    def test_root_and_child1(self):
        state = self.plex.activate(self.root)
        self.layout.change_to(state)
        state = self.plex.activate(self.child1)
        actions = self.layout.change_to(state)

        expected = [
            PlexLayoutAction(self.root, "move_to", [0, -100]),
            PlexLayoutAction(self.child1, "move_to", [0, 0]),
            PlexLayoutAction(self.child2, "move_to", self.root),
            PlexLayoutAction(self.child2, "remove", None),
            PlexLayoutAction(self.child3, "add", None),
            PlexLayoutAction(self.child3, "set_pos_to", self.child1),
            PlexLayoutAction(self.child3, "move_to", [100, 100]),
        ]
        self.assertEqual(actions, expected)

    def test_root_and_child3(self):
        state = self.plex.activate(self.root)
        self.layout.change_to(state)
        state = self.plex.activate(self.child3)
        actions = self.layout.change_to(state)

        expected = [
            PlexLayoutAction(self.root, "remove"),
            PlexLayoutAction(self.child1, "move_to", [0, -100]),
            PlexLayoutAction(self.child2, "move_to", self.root),
            PlexLayoutAction(self.child2, "remove"),
            PlexLayoutAction(self.child3, "add", None),
            PlexLayoutAction(self.child3, "set_pos_to", self.child1),
            PlexLayoutAction(self.child3, "move_to", [0, 0]),
        ]
        self.assertEqual(actions, expected)

    def test_twice_empty(self):
        state = self.plex.activate(self.root)
        self.layout.change_to(state)
        state = self.plex.activate(self.root)
        actions = self.layout.change_to(state)

        self.assertEqual(actions, [])