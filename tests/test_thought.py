import unittest

from api.models import Thought


class ThoughtMethods(unittest.TestCase):
    def test_init_id_generated(self):
        t = Thought()
        self.assertIsNotNone(t.get_id())

    def test_init_links_generated(self):
        t = Thought()
        self.assertIsNotNone(t.get_links())

    def test_title(self):
        t = Thought()
        t.set_title("test")
        self.assertEqual(t.get_title(), "test")

    def test_add_link(self):
        t1 = Thought()
        t2 = Thought()
        t1.add_link(t2.get_id(), "child")
        self.assertEqual(t1.get_links(), [{"id": t2.get_id(), "kind": "child"}])

    def test_remove_link(self):
        t1 = Thought()
        t2 = Thought()
        t1.add_link(t2.get_id(), "child")
        t1.remove_link(t2.get_id())
        self.assertEqual(t1.get_links(), [])

    @unittest.expectedFailure
    def test_add_link_twice(self):
        t1 = Thought()
        t2 = Thought()
        t1.add_link(t2.get_id(), "child")
        t1.add_link(t2.get_id(), "child")
        self.assertEqual(t1.get_links(), [{"id": t2.get_id(), "kind": "child"}])

    def test_eq(self):
        t1 = Thought()
        t2 = Thought()

        t2.set_field("id", t1.get_id())

        self.assertEqual(t1, t1)
        self.assertEqual(t1, t2)

    def test_not_eq(self):
        t1 = Thought()
        t2 = Thought()

        self.assertNotEqual(t1, t2)
