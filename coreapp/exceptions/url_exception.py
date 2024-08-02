
class URLException(Exception):
    """Ici je capte toutes les exceptions sur l 'url, a finir after."""

    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code

    def __str__(self):
        if self.code:
            return f"{self.args[0]} (Code: {self.code})"
        return self.args[0]
