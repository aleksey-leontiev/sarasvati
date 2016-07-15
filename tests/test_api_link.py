import unittest

from api.models import Thought, Link


class TestApiLink(unittest.TestCase):
    def setUp(self):
        self.root = Thought()
        self.child1 = Thought()
        self.child2 = Thought()

    def test_init(self):
        l = Link(self.root, self.child1, "child")
        self.assertEqual(l.source, self.root)
        self.assertEqual(l.destination, self.child1)
        self.assertEqual(l.kind, "child")

    def test_eq(self):
        l1 = Link(self.root, self.child1, "child")
        l2 = Link(self.root, self.child1, "child")
        self.assertEqual(l1, l2)

    def test_eq_none(self):
        l1 = Link(self.root, self.child1, "child")
        self.assertNotEqual(l1, None)

    def test_not_eq(self):
        l1 = Link(self.root, self.child1, "child")
        l2 = Link(self.root, self.child2, "child")
        self.assertNotEqual(l1, l2)
