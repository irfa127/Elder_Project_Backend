from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.inquiry import Inquiry, InquiryStatus as ModelInquiryStatus
from app.schemas.inquiry import InquiryCreate, InquiryUpdate, InquiryResponse, InquiryResponseManager
from typing import List
from app.models.user import User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/inquiries", tags=["Inquiries"])
# CREATE Inquiry

@router.post("/", response_model=InquiryResponse)
def create_inquiry(inquiry: InquiryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_inquiry = Inquiry(**inquiry.dict())
    db.add(new_inquiry)
    db.commit()
    db.refresh(new_inquiry)
    return new_inquiry
# GET ALL Inquiries

@router.get("/", response_model=List[InquiryResponse])
def get_inquiries(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    inquiries = db.query(Inquiry).all()
    return inquiries

# GET ALL Inquiries (Community View - Detailed)
@router.get("/community/{community_id}", response_model=List[InquiryResponseManager])
def get_community_inquiries(community_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    inquiries = db.query(Inquiry).filter(Inquiry.community_id == community_id).all()
    return inquiries
# GET Patient Inquiries
@router.get("/patient/{patient_id}", response_model=List[InquiryResponse])
def get_patient_inquiries(patient_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    inquiries = db.query(Inquiry).filter(Inquiry.patient_id == patient_id).all()
    return inquiries
# GET Single Inquiry
@router.get("/{inquiry_id}", response_model=InquiryResponse)
def get_inquiry(inquiry_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return inquiry
# UPDATE Inquiry oahdashbord.js update 
@router.put("/{inquiry_id}", response_model=InquiryResponse)
def update_inquiry(inquiry_id: int, inquiry_update: InquiryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    
    for key, value in inquiry_update.dict(exclude_unset=True).items():
        if key == 'status':
            # Convert Schema Enum (or string) to Model Enum
            str_val = value.value if hasattr(value, 'value') else value
            value = ModelInquiryStatus(str_val)
        setattr(inquiry, key, value)
    
    db.commit()
    db.refresh(inquiry)
    return inquiry

@router.delete("/{inquiry_id}")
def delete_inquiry(inquiry_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    inquiry = db.query(Inquiry).filter(Inquiry.id == inquiry_id).first()
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    
    db.delete(inquiry)
    db.commit()
    return {"message": "Inquiry deleted successfully"}

