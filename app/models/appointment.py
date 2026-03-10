
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from app.database.database import Base
import enum

class AppointmentStatus(enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    ON_THE_WAY = "ON_THE_WAY"
    ARRIVED = "ARRIVED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("app_users.id"), nullable=False)
    nurse_id = Column(Integer, ForeignKey("app_users.id"), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    appointment_time = Column(String, nullable=False)
    service_type = Column(String)
    status = Column(
        SQLEnum(AppointmentStatus, native_enum=False, validate_strings=True), # later 
        default=AppointmentStatus.PENDING
    )
    notes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

