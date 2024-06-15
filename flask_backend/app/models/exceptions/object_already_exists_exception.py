class ObjectAlreadyExistsException(ValueError):
    """Raised when attempting to create an object with an existing identifier."""
    def __init__(self, message="Object already exists in database."):
        self.message = message
        super().__init__(self.message)