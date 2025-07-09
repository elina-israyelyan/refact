class RefactGeneric(Exception):
    """Base exception for all custom errors in reAct."""

    def __init__(self, message=None):
        if message is None:
            message = "An unknown error occurred."
        super().__init__(message)


class RefactException(RefactGeneric):
    def __init__(self, message=None):
        if message is None:
            message = "An unknown error occurred."
        super().__init__(message)


class ActException(RefactGeneric):
    def __init__(self, message=None):
        if message is None:
            message = "An unknown error occurred."
        super().__init__(message)


class ReasonException(RefactGeneric):
    def __init__(self, message=None):
        if message is None:
            message = "An unknown error occurred."
        super().__init__(message)


class ZeroDivisionCustomException(RefactGeneric):
    def __init__(self, message=None):
        if message is None:
            message = (
                "The Caller wants to do magic, make sure the caller is not a wizard."
            )
        super().__init__(message)
