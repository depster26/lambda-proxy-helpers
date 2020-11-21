class NotFoundError(Exception):
    """
    Raised when the item being requested cannot be found
    """
    def __init__(self, message):
        self.message = message
        self.status_code = 404

    def __str__(self):
        return self.message

    def __repr__(self):
        return 'Not Found Error'


class MissingParameterError(Exception):
    """
    Raised when the endpoint is expecting a parameter but was not provided.
    """
    def __init__(self, message):
        self.message = message
        self.status_code = 400

    def __str__(self):
        return self.message

    def __repr__(self):
        return 'Missing Parameter Error'


class InvalidParameterError(Exception):
    """
    Raised when the endpoint is expecting a parameter that's provided but is invalid.
    """
    def __init__(self, message):
        self.message = message
        self.status_code = 400

    def __str__(self):
        return self.message

    def __repr__(self):
        return 'Invalid Parameter Error'


class AlreadyExistsError(Exception):
    """
    Raised when an object is trying to be created but one already exists
    """
    def __init__(self, message):
        self.message = message
        self.status_code = 400

    def __str__(self):
        return self.message

    def __repr__(self):
        return 'Object Already Exists Error'


class RelatedRecordsExistError(Exception):
    """
    Raised when a delete operation is attempted but related records exist and will break foreign key constraint(s)
    """
    def __init__(self, message):
        self.message = message
        self.status_code = 400

    def __str__(self):
        return self.message

    def __repr__(self):
        return 'Related Records Exist Error'


class ValidationError(Exception):
    """
    Raised when validation of a request fails
    """
    def __init__(self, message):
        self.message = message
        self.status_code = 400

    def __str__(self):
        return self.message

    def __repr__(self):
        return 'Validation Error'


class InvalidFunctionRequestError(Exception):
    """
    Raised when the handler method is unable to determine the correct function call
    """
    def __init__(self, message):
        self.message = message
        self.status_code = 400

    def __str__(self):
        return self.message

    def __repr__(self):
        return 'Invalid Function Request Error'


class InvalidUserError(Exception):
    """
    Raised when the handler method is unable to determine the user from the request
    """
    def __init__(self, message):
        self.message = message
        self.status_code = 400

    def __str__(self):
        return self.message

    def __repr__(self):
        return 'Invalid User Error'


class GeneralError(Exception):
    """
    Raised when we don't know the type of error being thrown or just want to throw a general exception along
    with the request event object.
    """
    def __init__(self, message):
        self.message = message
        self.status_code = 500
        self.event = None

    def __str__(self):
        return self.message

    def __repr__(self):
        return 'General Error'
