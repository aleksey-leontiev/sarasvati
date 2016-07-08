import unittest
from unittest.mock import Mock, call

from api.models import Model


class ModelMethods(unittest.TestCase):
    def test_init(self):
        m = Model()
        self.assertEqual(m.to_dictionary(), {})

    def test_init_with_dictionary(self):
        dictionary = {"init":True}
        m = Model(dictionary)
        self.assertEqual(m.to_dictionary(), dictionary)

    def test_get_field(self):
        dictionary = {"init": True}
        m = Model(dictionary)
        self.assertEqual(m.get_field("init"), True)

    def test_set_field(self):
        m = Model()
        m.set_field("test", True)
        self.assertEqual(m.get_field("test"), True)

    def test_event_changed_called(self):
        f = Mock()
        m = Model()
        m.changed.subscribe(f)
        m.set_field("test", 1234)
        f.assert_called_once_with((None, 1234))

    def test_event_changed_old_and_new_values(self):
        f = Mock()
        m = Model()
        m.changed.subscribe(f)
        m.set_field("test", 1234)
        m.set_field("test", 9876)
        m.set_field("test", 9876)
        f.assert_has_calls([call((None, 1234)), call((1234, 9876))])

    def test_event_changed_not_called_with_no_changes(self):
        f = Mock()
        m = Model()
        m.changed.subscribe(f)
        m.set_field("test", 9876)
        m.set_field("test", 9876)
        f.assert_called_once_with((None, 9876))
