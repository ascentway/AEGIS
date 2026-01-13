from pydantic import BaseModel, EmailStr
from typing import Optional, Literal

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    role: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    role: Literal["player", "organization"]
