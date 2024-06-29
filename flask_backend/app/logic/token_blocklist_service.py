from abc import ABC, abstractmethod
from app.models.token_blocked import TokenBlocked

class TokenBlocklistService(ABC):
    @abstractmethod
    def __init__(self) -> None:
        "Initialize Token Blocklist Database"
        pass   

    @abstractmethod
    def add_token_to_blocklist(self, token: TokenBlocked) -> None:
        "Add a token to the blocklist"
        pass
    
    @abstractmethod
    def is_token_in_blocklist(self, token: TokenBlocked) -> bool:
        "Check if a token is in the blocklist"
        pass