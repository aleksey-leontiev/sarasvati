from .events import Events


class Api:
    def __init__(self):
        self.events = Events()
        self.brain = None

api = Api()
