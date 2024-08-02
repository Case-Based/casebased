class InvalidAttributeValueError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InvalidAttributeTypeError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
