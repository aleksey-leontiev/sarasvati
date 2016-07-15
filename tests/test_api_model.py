import unittest
from unittest.mock import Mock, call

from api.models import Model


class TestApiModel(unittest.TestCase):
    def setUp(self):
        self.model = Model()

    def test_init(self):
        self.assertEqual(self.model.to_dictionary(), {})

    def test_set_field(self):
        self.model.set_field("test", True)
        self.assertEqual(self.model.get_field("test"), True)

    def test_get_field_none(self):
        self.assertEqual(self.model.get_field("does_not_exist"), None)

    def test_event_changed_called(self):
        f = Mock()
        self.model.changed.subscribe(f)
        self.model.set_field("test", 1234)
        f.assert_called_once_with((None, 1234))

    def test_event_changed_old_and_new_values(self):
        f = Mock()
        self.model.changed.subscribe(f)
        self.model.set_field("test", 1234)
        self.model.set_field("test", 9876)
        f.assert_has_calls([call((None, 1234)), call((1234, 9876))])

    def test_event_changed_not_called_with_no_changes(self):
        f = Mock()
        self.model.changed.subscribe(f)
        self.model.set_field("test", 9876)
        self.model.set_field("test", 9876)
        f.assert_called_once_with((None, 9876))

    def test_to_dictionary(self):
        dictionary = {"init": True, "test":123}
        self.model.set_field("init", True)
        self.model.set_field("test", 123)
        self.assertEqual(self.model.to_dictionary(), dictionary)

    def test_to_dictionary_copy(self):
        self.model.set_field("init", True)
        copy = self.model.to_dictionary()
        copy["init"] = False
        self.assertEqual(self.model.get_field("init"), True)

    def test_from_dictionary(self):
        dictionary = {"init": True}
        self.model.from_dictionary(dictionary)
        self.assertEqual(self.model.to_dictionary(), dictionary)

    def test_from_dictionary_clean(self):
        dictionary = {"init": True}
        self.model.set_field("one_more", "true")
        self.model.from_dictionary(dictionary)
        self.assertEqual(self.model.to_dictionary(), dictionary)
        self.assertEqual(self.model.get_field("one_more"), None)
