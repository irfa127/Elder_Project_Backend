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
    
    class Config:
        from_attributes = True

