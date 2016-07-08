
class Event:
    def __init__(self):
        """
        Initializes new instance of the event
        """
        self.handlers = []

    def subscribe(self, handler):
        """
        Subscribe for the event
        :param handler:
        """
        self.handlers.append(handler)

    def notify(self, args):
        """
        Notify subscribers
        :param args: Event arguments
        """
        for handler in self.handlers:
            handler(args)
