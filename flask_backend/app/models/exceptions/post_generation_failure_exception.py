class PostGenerationFailureException(Exception):
    """Raised when generative model post generation fails validation."""
    def __init__(self, message="Unknown"):
        self.message = "Post Generation Failed Validation. Reason: " + message
        super().__init__(self.message)