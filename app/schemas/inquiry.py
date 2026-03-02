from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class InquiryStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class InquiryBase(BaseModel):
    community_id: int
    resident_name: str
    resident_age: Optional[int] = None
    applicant_name: str
    applicant_phone: str
    applicant_email: EmailStr
    relation: Optional[str] = None
    move_in_date: Optional[str] = None
    medical_needs: Optional[str] = None
    special_requests: Optional[str] = None

class InquiryCreate(InquiryBase):
    patient_id: int

class InquiryUpdate(BaseModel):
    status: InquiryStatus

# Secure Nested Models
class ApplicantPublic(BaseModel):
    name: str 

    class Config:
        from_attributes = True

class ApplicantDetailed(ApplicantPublic):
    email: EmailStr
    phone: Optional[str] = None

    class Config:
        from_attributes = True

class OldAgeHomePublic(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

class InquiryResponseBase(BaseModel):
    # Use 'booking_id' across the board or just ID? User asked for booking_id.
    id: int = Field(..., serialization_alias="booking_id")
    status: InquiryStatus
    created_at: datetime
    
    old_age_home: Optional[OldAgeHomePublic] = Field(None, validation_alias="community")
    
    resident_name: str
    resident_age: Optional[int] = None
    relation: Optional[str] = None
    move_in_date: Optional[str] = None
    medical_needs: Optional[str] = None
    special_requests: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class InquiryResponse(InquiryResponseBase):
    # Patient View: Restricted Applicant Data
    applicant: Optional[ApplicantPublic] = Field(None, validation_alias="patient")

class InquiryResponseManager(InquiryResponseBase):
    # Manager View: Full Applicant Data
    applicant: Optional[ApplicantDetailed] = Field(None, validation_alias="patient")
