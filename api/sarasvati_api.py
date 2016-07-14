from .sarasvati_api_actions import SarasvatiApiActions
from .sarasvati_api_events import SarasvatiApiEvents


class SarasvatiApi:
    def __init__(self):
        self.events = SarasvatiApiEvents(self)
        self.actions = SarasvatiApiActions(self)
        self.brain = None
        self.pluginManager = None

api = SarasvatiApi()
