from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserResponse, UserUpdate
from app.routers.auth import get_current_user, get_password_hash

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
    
    # Validation: Do not allow clearing fields that already have data
    for field, new_value in update_data.items():
        if field == "password":
            if new_value and new_value.strip():
                user.hashed_password = get_password_hash(new_value)
            continue

        existing_value = getattr(user, field)
        
        # If database already has a value, do not allow clearing it
        if existing_value is not None and existing_value != "" and (new_value is None or str(new_value).strip() == ""):
             raise HTTPException(
                status_code=400, 
                detail=f"Field '{field}' cannot be cleared. Please provide current value."
            )
        
        setattr(user, field, new_value)
    
    db.commit()
    db.refresh(user)
    return user

