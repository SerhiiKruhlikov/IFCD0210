class CantGetCoordinates(Exception):
    """Program can't get current GPS coordinates"""
    def __init__(self, message="Could not get coordinates"):
        self.message = message
        super().__init__(self.message)


class ApiServiceError(Exception):
    """Program can't get current GPS coordinates"""
