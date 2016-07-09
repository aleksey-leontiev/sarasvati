
class Event:
    def __init__(self):
        """
        Initializes new instance of the Event class
        """
        self.handlers = []

    def subscribe(self, handler):
        """
        Subscribe for the event
        :param handler:
        """
        self.handlers.append(handler)

    def unsubscribe(self, handler):
        """
        Unsubscribe from the event
        :param handler:
        """
        self.handlers.remove(handler)

    def notify(self, args):
        """
        Notify subscribers
        :param args: Event arguments
        """
        for handler in self.handlers:
            handler(args)
