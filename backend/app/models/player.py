from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional, List, Dict
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

# Helper for MongoDB ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

class PlayerBase(BaseModel):
    name: str
    age: int
    city: str
    state: str
    country: str
    mobile_no: str
    email: EmailStr
    profile_photo: str
    social_links: Optional[Dict[str, str]] = None

class PlayerCreate(PlayerBase):
    password: str

class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    mobile_no: Optional[str] = None
    email: Optional[EmailStr] = None
    profile_photo: Optional[str] = None
    social_links: Optional[Dict[str, str]] = None

class PlayerInDB(PlayerBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    hashed_password: str

class PlayerResponse(PlayerBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
