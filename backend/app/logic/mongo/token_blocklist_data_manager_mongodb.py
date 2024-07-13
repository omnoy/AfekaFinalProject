from typing import List
from app.logic.mongo.database import get_token_blocklist
from app.logic.token_blocklist_service import TokenBlocklistService
from app.models.token_blocked import TokenBlocked


class TokenBlocklistDataManagerMongoDB(TokenBlocklistService):
    def __init__(self):
        pass

    def add_token_to_blocklist(self, token: TokenBlocked) -> None:
        get_token_blocklist().insert_one(token.__dict__)

    def is_token_in_blocklist(self, token: TokenBlocked) -> bool:
        return get_token_blocklist().find_one(token.__dict__) is not None