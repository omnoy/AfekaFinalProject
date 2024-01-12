from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.models.user_role import UserRole

class User(BaseModel):
    _id: str | None = None
    username: str
    personal_name: str
    email: EmailStr
    position: str | None = None
    role: UserRole = UserRole.BASIC_USER