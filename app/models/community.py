from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Community(Base):
    __tablename__ = "communities"
    
    
    id = Column(Integer, primary_key=True, index=True)
    manager_id = Column(Integer, ForeignKey("app_users.id"), nullable=False)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    description = Column(String)
    pricing = Column(String)
    image_url = Column(String)
    phone = Column(String)
    specialty_label = Column(String)
    rating = Column(Float, default=0.0)
    is_featured = Column(Boolean, default=False)
    is_premium = Column(Boolean, default=False)
    facilities = Column(String)
    
    manager = relationship("User", foreign_keys=[manager_id])

    @property
    def email(self):
        return self.manager.email if self.manager else None

