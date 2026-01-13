from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional, List, Dict
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class OrganizationBase(BaseModel):
    org_name: str
    address: str
    logo: Optional[str] = None
    contact_no: str
    email: EmailStr
    games_hiring_for: List[str] = []
    established_year: int
    social_links: Dict[str, str] = Field(default_factory=dict, description="e.g. {'instagram': 'url'}")

class OrganizationCreate(OrganizationBase):
    password: str

class OrganizationUpdate(BaseModel):
    org_name: Optional[str] = None
    address: Optional[str] = None
    logo: Optional[str] = None
    contact_no: Optional[str] = None
    email: Optional[EmailStr] = None
    games_hiring_for: Optional[List[str]] = None
    established_year: Optional[int] = None
    social_links: Optional[Dict[str, str]] = None

class OrganizationInDB(OrganizationBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    hashed_password: str

class OrganizationResponse(OrganizationBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
