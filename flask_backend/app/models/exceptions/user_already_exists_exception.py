class UserAlreadyExistsException(ValueError):
    """Raised when attempting to create a user with an existing email."""
    def __init__(self, message="User already exists."):
        self.message = message
        super().__init__(self.message)