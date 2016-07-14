from .event import Event


class SarasvatiApiEvents:
    def __init__(self, api):
        self.api = api

        self.thoughtCreated = Event()
        self.thoughtSelected = Event()
        self.thoughtChanging = Event()
        self.thoughtChanged = Event()
