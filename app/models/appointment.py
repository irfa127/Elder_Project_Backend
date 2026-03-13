
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
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

    patient = relationship("User", foreign_keys=[patient_id])
    nurse = relationship("User", foreign_keys=[nurse_id])

    @property
    def patient_name(self):
        return self.patient.full_name if self.patient else None

    @property
    def patient_image(self):
        return self.patient.profile_picture if self.patient else None

    @property
    def patient_dob(self):
        return self.patient.dob if self.patient else None

    @property
    def patient_gender(self):
        return self.patient.gender if self.patient else None

    @property
    def patient_blood_group(self):
        return self.patient.blood_group if self.patient else None

    @property
    def patient_emergency_contact_name(self):
        return self.patient.emergency_contact_name if self.patient else None

    @property
    def patient_emergency_contact_phone(self):
        return self.patient.emergency_contact_phone if self.patient else None

    @property
    def patient_medical_condition(self):
        return self.patient.medical_condition if self.patient else None

    @property
    def patient_mobility_status(self):
        return self.patient.mobility_status if self.patient else None

    @property
    def nurse_name(self):
        return self.nurse.full_name if self.nurse else None

    @property
    def nurse_image(self):
        return self.nurse.profile_picture if self.nurse else None

