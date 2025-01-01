class InvalidMethod(Exception):
    """
    Raised when the input method of a function is invalid
    """

    def __init__(self, message=""):
        self.message = "Method is invalid. Please recheck."
        super().__init__(self.message)
    pass

class UnknownError(Exception):
    """
    Raised when there's an unexpected error
    """

    def __init__(self, message=""):
        self.message = "An unknown error occurred. Please recheck."
        super().__init__(self.message)