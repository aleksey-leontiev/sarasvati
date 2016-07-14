from api.event import Event


class Model:
    def __init__(self):
        self.dictionary = {}
        self.changed = Event()

    def get_field(self, name):
        """
        Returns value of the specified field
        :param name: Name of the field
        :return: Value of the field
        """
        return self.dictionary.get(name, None)

    def set_field(self, name, value):
        """
        Sets value of the specified field. Raises changed event.
        :param name: Name of the field
        :param value: Value of the field
        """
        old_value = None
        if name in self.dictionary:
            old_value = self.dictionary[name]
        if old_value != value:
            self.dictionary[name] = value
            self.changed.notify((old_value, value))

    def to_dictionary(self):
        """
        Returns dictionary representation of the model
        :return: dict
        """
        return self.dictionary

    def from_dictionary(self, dictionary):
        self.dictionary = {}
        self.dictionary.update(dictionary)

