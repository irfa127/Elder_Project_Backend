from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase): #appointment-completed.html
    appointment_id: int

class ReviewOut(ReviewBase): #nurse-profile.html reviews-list.html
    id: int
    patient_id: int
    nurse_id: int
    appointment_id: int
    created_at: datetime

    class Config:
        from_attributes = True

