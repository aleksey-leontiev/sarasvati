import unittest

from api.models import Thought


class ThoughtMethods(unittest.TestCase):
    def test_init_id_generated(self):
        t = Thought()
        self.assertIsNotNone(t.get_id())

    def test_init_links_generated(self):
        t = Thought()
        self.assertIsNotNone(t.get_links())