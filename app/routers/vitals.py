from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.vital import Vitals
from app.models.user import User
from app.schemas.vital import VitalCreate, VitalResponse
from typing import List
from app.routers.auth import get_current_user

router = APIRouter(prefix="/vitals", tags=["Vitals"])
# CREATE Vital
@router.post("/", response_model=VitalResponse)
def create_vital(vital: VitalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_vital = Vitals(**vital.dict())
    db.add(new_vital)
    db.commit()
    db.refresh(new_vital)
    return new_vital
# GET ALL Vitals
@router.get("/", response_model=List[VitalResponse])
def get_vitals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    vitals = db.query(Vitals).all()
    return vitals
# GET Patient Vitals
@router.get("/patient/{patient_id}", response_model=List[VitalResponse])
def get_patient_vitals(patient_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    vitals = db.query(Vitals).filter(Vitals.patient_id == patient_id).order_by(Vitals.created_at.desc()).all()
    return vitals
# GET Single Vital
@router.get("/{vital_id}", response_model=VitalResponse)
def get_vital(vital_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    vital = db.query(Vitals).filter(Vitals.id == vital_id).first()
    if not vital:
        raise HTTPException(status_code=404, detail="Vital record not found")
    return vital

@router.delete("/{vital_id}")
def delete_vital(vital_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    vital = db.query(Vitals).filter(Vitals.id == vital_id).first()
    if not vital:
        raise HTTPException(status_code=404, detail="Vital record not found")
    
    db.delete(vital)
    db.commit()
    return {"message": "Vital record deleted successfully"}

