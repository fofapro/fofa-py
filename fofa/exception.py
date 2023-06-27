
class FofaError(Exception):
    """This exception gets raised whenever an error returned by the Fofa API."""
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
