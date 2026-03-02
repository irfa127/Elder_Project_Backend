from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base
import enum

class InquiryStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class Inquiry(Base):
    __tablename__ = "inquiries"
    
    id = Column(Integer, primary_key=True, index=True)
    community_id = Column(Integer, ForeignKey("communities.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("app_users.id"), nullable=False)
    resident_name = Column(String, nullable=False)
    resident_age = Column(Integer)
    applicant_name = Column(String, nullable=False)
    applicant_phone = Column(String, nullable=False)
    applicant_email = Column(String, nullable=False)
    relation = Column(String)
    move_in_date = Column(String)
    medical_needs = Column(String)
    special_requests = Column(String)
    status = Column(SQLEnum(InquiryStatus), default=InquiryStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    community = relationship("Community", foreign_keys=[community_id])
    patient = relationship("User", foreign_keys=[patient_id])

