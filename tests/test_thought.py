import unittest

from api.models import Thought


class ThoughtMethods(unittest.TestCase):
    def setUp(self):
        self.root = Thought()
        self.child = Thought()
        self.second_child = Thought()

    def test_init_id_generated(self):
        self.assertIsNotNone(self.root.get_id())

    def test_init_links_generated(self):
        self.assertIsNotNone(self.root.get_links())

    def test_title(self):
        self.root.set_title("test")
        self.assertEqual(self.root.get_title(), "test")

    def test_add_link(self):
        self.root.add_link(self.child.get_id(), "child")
        self.assertEqual(
            self.root.get_links(),
            [{"id": self.child.get_id(), "kind": "child"}])

    def test_remove_link(self):
        self.root.add_link(self.child.get_id(), "child")
        self.root.remove_link(self.child.get_id())
        self.assertEqual(self.root.get_links(), [])

    def test_add_link_twice(self):
        self.root.add_link(self.child.get_id(), "child")
        with self.assertRaises(ValueError):
            self.root.add_link(self.child.get_id(), "child")

    def test_get_links_by_kind(self):
        parent = Thought()

        self.root.add_link(parent.get_id(), "parent")
        self.root.add_link(self.child.get_id(), "child")
        self.root.add_link(self.second_child.get_id(), "child")

        self.assertEqual(self.root.get_links_by_kind("child"), [
            {"id": self.child.get_id(), "kind": "child"},
            {"id": self.second_child.get_id(), "kind": "child"},
        ])

    def test_eq(self):
        self.child.set_field("id", self.root.get_id())
        self.assertEqual(self.root, self.root)
        self.assertEqual(self.root, self.child)

    def test_not_eq(self):
        self.assertNotEqual(self.root, self.child)
