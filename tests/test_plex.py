import unittest

from api.models import Brain
from plugins.brain.plex import Plex
# noinspection PyUnresolvedReferences
from assets import MemoryStorage


class TestPlex(unittest.TestCase):
    def setUp(self):
        self.storage = MemoryStorage()
        self.brain = Brain(self.storage)
        self.plex = Plex(self.brain)

        self.__init_brain_state_1()

    def test_activate_root(self):
        layout1 = self.plex.activate(self.root)
        self.assertEqual(layout1.get_thoughts_by_state("root"), [self.root])
        self.assertEqual(layout1.get_thoughts_by_state("child"), [self.child1, self.child2])
        self.assertEqual(layout1.get_thoughts_by_state("parent"), [])
        self.assertEqual(layout1.get_thoughts_by_state("jump"), [self.root_jump1, self.root_jump2])
        self.assertEqual(len(layout1.get_state()), 5)

    def test_activate_child1(self):
        layout1 = self.plex.activate(self.child1)
        self.assertEqual(layout1.get_thoughts_by_state("parent"), [self.root])
        self.assertEqual(layout1.get_thoughts_by_state("root"), [self.child1])
        self.assertEqual(layout1.get_thoughts_by_state("child"), [self.child3])
        self.assertEqual(len(layout1.get_state()), 3)

    def test_activate_child2(self):
        layout1 = self.plex.activate(self.child2)
        self.assertEqual(layout1.get_thoughts_by_state("parent"), [self.root])
        self.assertEqual(layout1.get_thoughts_by_state("root"), [self.child2])
        self.assertEqual(layout1.get_thoughts_by_state("child"), [])
        self.assertEqual(len(layout1.get_state()), 2)

    def test_activate_child3(self):
        layout1 = self.plex.activate(self.child3)
        self.assertEqual(layout1.get_thoughts_by_state("parent"), [self.child1])
        self.assertEqual(layout1.get_thoughts_by_state("root"), [self.child3])
        self.assertEqual(layout1.get_thoughts_by_state("child"), [])
        self.assertEqual(layout1.get_thoughts_by_state("jump"), [self.child3_jump1])
        self.assertEqual(len(layout1.get_state()), 3)

    def test_activate_root_jump1(self):
        layout1 = self.plex.activate(self.root_jump1)
        self.assertEqual(layout1.get_thoughts_by_state("parent"), [])
        self.assertEqual(layout1.get_thoughts_by_state("root"), [self.root_jump1])
        self.assertEqual(layout1.get_thoughts_by_state("child"), [])
        self.assertEqual(layout1.get_thoughts_by_state("jump"), [self.root])
        self.assertEqual(len(layout1.get_state()), 2)

    def test_activate_child3_jump1(self):
        layout1 = self.plex.activate(self.child3_jump1)
        self.assertEqual(layout1.get_thoughts_by_state("parent"), [])
        self.assertEqual(layout1.get_thoughts_by_state("root"), [self.child3_jump1])
        self.assertEqual(layout1.get_thoughts_by_state("child"), [self.child4])
        self.assertEqual(layout1.get_thoughts_by_state("jump"), [self.child3])
        self.assertEqual(len(layout1.get_state()), 3)

    def test_activate_child4(self):
        layout1 = self.plex.activate(self.child4)
        self.assertEqual(layout1.get_thoughts_by_state("parent"), [self.child3_jump1])
        self.assertEqual(layout1.get_thoughts_by_state("root"), [self.child4])
        self.assertEqual(layout1.get_thoughts_by_state("child"), [])
        self.assertEqual(layout1.get_thoughts_by_state("jump"), [])
        self.assertEqual(len(layout1.get_state()), 2)

    def __init_brain_state_1(self):
        # root -> child1 -> child3
        # root -> child2
        # root_jump1 <- root
        # root_jump2 <- root
        # child3_jump1 <- child3
        # child3_jump1 -> child4
        self.root = self.brain.create_thought("root")
        self.child1 = self.brain.create_linked_thought(self.root, "parent->child", "child1")
        self.child2 = self.brain.create_linked_thought(self.root, "parent->child", "child2")
        self.child3 = self.brain.create_linked_thought(self.child1, "parent->child", "child3")

        self.root_jump1 = self.brain.create_linked_thought(self.root, "jump", "root_jump1")
        self.root_jump2 = self.brain.create_linked_thought(self.root, "jump", "root_jump2")

        self.child3_jump1 = self.brain.create_linked_thought(self.child3, "jump", "child3_jump1")

        self.child4 = self.brain.create_linked_thought(self.child3_jump1, "parent->child", "child3_jump1_child1")
