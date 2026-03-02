from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum): #signup dropdown
    PATIENT = "patient"
    NURSE = "nurse"
    OAH_MANAGER = "oah_manager"

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    role: UserRole
    phone: Optional[str] = None
    address: Optional[str] = None

class UserCreate(UserBase):   #signup.html #Common fields if needed → UserBase inherit
    password: str

class UserUpdate(BaseModel):   #edit-profile.html
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    profile_picture: Optional[str] = None
    
class UserLogin(BaseModel): #login.html Different / minimal fields if needed → BaseModel direct
    email: EmailStr
    password: str

class UserResponse(UserBase): #profile.html / dashboard
    id: int
    rating: Optional[float] = 4.8
    profile_picture: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel): #login.html (response)
    access_token: str
    token_type: str
    user: UserResponse

