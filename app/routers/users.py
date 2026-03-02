from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserResponse, UserUpdate
from app.routers.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/nurses", response_model=List[UserResponse])
def get_nurses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fetch all users with the role 'nurse'"""
    nurses = db.query(User).filter(User.role == UserRole.NURSE).all()
    return nurses

@router.get("/patients", response_model=List[UserResponse])
def get_patients(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fetch all users with the role 'patient'"""
    patients = db.query(User).filter(User.role == UserRole.PATIENT).all()
    return patients

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fetch a specific user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

