from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base
from .user import User  

class Vitals(Base):
    __tablename__ = "vitals"


    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("app_users.id"), nullable=False)  
    nurse_id = Column(Integer, ForeignKey("app_users.id"), nullable=True)     
    blood_pressure = Column(String)
    heart_rate = Column(Integer)
    temperature = Column(String)
    sugar_level = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # relationships
    patient = relationship("User", foreign_keys=[patient_id], backref="patient_vitals")
    nurse = relationship("User", foreign_keys=[nurse_id], backref="nurse_vitals")


