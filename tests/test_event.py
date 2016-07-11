import unittest
from unittest.mock import Mock

from api import Event


class EventMethods(unittest.TestCase):
    def setUp(self):
        self.event = Event()

    def test_subscribe(self):
        f = Mock()
        self.event.subscribe(f)
        self.event.notify("data")
        f.assert_called_once_with("data")

    def test_unsubscribe(self):
        f = Mock()
        self.event.subscribe(f)
        self.event.unsubscribe(f)
        self.event.notify("data")
        f.assert_not_called()
