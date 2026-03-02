from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VitalBase(BaseModel): #add-vitals.html
    patient_id: int
    blood_pressure: Optional[str] = None
    heart_rate: Optional[int] = None
    sugar_level: Optional[int] = None
    temperature: Optional[str] = None

class VitalCreate(VitalBase):
    nurse_id: int

class VitalResponse(VitalBase): #patient-vitals.html nurse-vitals.html
    id: int
    nurse_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

