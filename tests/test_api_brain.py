import unittest

from api.models import Thought, Brain, Link
# noinspection PyUnresolvedReferences
from assets import MemoryStorage


class TestApiBrain(unittest.TestCase):
    def setUp(self):
        self.storage = MemoryStorage()
        self.brain = Brain(self.storage)

    def test_add_thought(self):
        t = Thought()
        self.brain.add_thought(t)
        self.assertIsNotNone(self.brain.get_thought(t.get_id()))

    def test_create_thought(self):
        c = self.brain.create_thought("test")
        t = self.brain.get_thought(c.get_id())
        self.assertEqual(c, t)

    def test_create_linked_thought(self):
        c1 = self.brain.create_thought("test")
        c2 = self.brain.create_linked_thought(c1, "parent->child", "test_2")
        c3 = self.brain.create_thought("test_another")

        self.assertIsNotNone(c2)
        self.assertEqual(self.brain.get_link_type(c1, c2), "child")
        self.assertEqual(self.brain.get_link_type(c2, c1), "parent")
        self.assertIsNone(self.brain.get_link_type(c1, c3))

    def test_is_linked(self):
        c1 = self.brain.create_thought("test")
        c2 = self.brain.create_linked_thought(c1, "parent->child", "test_2")
        c3 = self.brain.create_thought("test_another")

        self.assertIsNotNone(c2)
        self.assertTrue(self.brain.is_linked(c1, c2))
        self.assertTrue(self.brain.is_linked(c2, c1))
        self.assertFalse(self.brain.is_linked(c1, c3))

    def test_link_thoughts(self):
        t1 = Thought()
        t2 = Thought()
        self.brain.link_thoughts(t1, t2, "parent->child")

        self.assertEqual(self.brain.get_link_type(t1, t2), "child")
        self.assertEqual(self.brain.get_link_type(t2, t1), "parent")

    def test_link_thoughts_wrong_kind(self):
        t1 = Thought()
        t2 = Thought()
        with self.assertRaises(ValueError):
            self.brain.link_thoughts(t1, t2, "WRONG_KIND")

    def test_get_links(self):
        t1 = self.brain.create_thought("root")
        t2 = self.brain.create_linked_thought(t1, "parent->child", "child_1")
        t3 = self.brain.create_linked_thought(t1, "parent->child", "child_2")
        t4 = self.brain.create_linked_thought(t2, "parent->child", "child_3")

        self.assertEqual(self.brain.get_links(t2), [
            Link(t2, t1, "parent"),
            Link(t2, t4, "child"),
        ])

    def test_eq(self):
        t1 = Thought()
        t2 = Thought()

        l1 = Link(t1, t2, "child")
        l2 = Link(t1, t2, "child")

        self.assertEqual(l1, l1)
        self.assertEqual(l1, l2)

    def test_not_eq(self):
        t1 = Thought()
        t2 = Thought()

        l1 = Link(t1, t2, "child")
        l2 = Link(t2, t1, "child")

        self.assertNotEqual(l1, l2)
