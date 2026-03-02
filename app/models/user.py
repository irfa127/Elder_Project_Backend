from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, Float
from sqlalchemy.sql import func
from app.database.database import Base
import enum

class UserRole(str, enum.Enum):
    PATIENT = "patient"
    NURSE = "nurse"
    OAH_MANAGER = "oah_manager"

class User(Base):
    __tablename__ = "app_users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole, native_enum=False, values_callable=lambda x: [e.value for e in x]), nullable=False)
    phone = Column(String)
    address = Column(String)
    rating = Column(Float, default=4.8)
    profile_picture = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    @property
    def name(self):
        return self.full_name

