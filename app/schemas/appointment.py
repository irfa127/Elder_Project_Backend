from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class AppointmentStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    ON_THE_WAY = "ON_THE_WAY"
    ARRIVED = "ARRIVED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"

class AppointmentBase(BaseModel): #book-appointment.html
    patient_id: int
    nurse_id: int
    appointment_date: datetime
    appointment_time: str
    service_type: Optional[str] = None
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase): #book-appointment.html
    pass

class AppointmentUpdate(BaseModel): #nurse-dashboard.html
    status: AppointmentStatus
    notes: Optional[str] = None

class AppointmentResponse(AppointmentBase): #patient-appointments.html nurse-appointments.html
    id: int
    status: str
    created_at: Optional[datetime] = None
    has_review: Optional[bool] = False
    nurse_name: Optional[str] = None
    nurse_image: Optional[str] = None
    patient_name: Optional[str] = None
    patient_image: Optional[str] = None
    # Additional Patient Details
    patient_dob: Optional[str] = None
    patient_gender: Optional[str] = None
    patient_blood_group: Optional[str] = None
    patient_emergency_contact_name: Optional[str] = None
    patient_emergency_contact_phone: Optional[str] = None
    patient_medical_condition: Optional[str] = None
    patient_mobility_status: Optional[str] = None

    class Config:
        from_attributes = True

