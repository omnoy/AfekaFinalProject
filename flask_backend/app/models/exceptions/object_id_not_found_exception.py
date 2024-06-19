class ObjectIDNotFoundException(ValueError):
    """Raised when attempting to access objects with invalid IDs."""
    def __init__(self, message="Object ID not found in the database."):
        self.message = message
        super().__init__(self.message)