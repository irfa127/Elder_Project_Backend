from pydantic import BaseModel
from typing import Optional

class CommunityBase(BaseModel):
    name: str
    location: str
    description: Optional[str] = None
    pricing: Optional[str] = None
    image_url: Optional[str] = None
    phone: Optional[str] = None
    specialty_label: Optional[str] = None
    facilities: Optional[str] = None
    is_featured: bool = False
    is_premium: bool = False

class CommunityCreate(CommunityBase):  #add-community.html
    manager_id: int

class CommunityUpdate(BaseModel): #edit-community.html
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    pricing: Optional[str] = None
    image_url: Optional[str] = None
    phone: Optional[str] = None
    specialty_label: Optional[str] = None
    facilities: Optional[str] = None

class CommunityResponse(CommunityBase): #community-list.html community-details.html
    id: int
    manager_id: int
    rating: float
    phone: Optional[str] = None
    
    class Config:
        from_attributes = True

