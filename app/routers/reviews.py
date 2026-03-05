from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.review import Review
from app.models.appointment import Appointment, AppointmentStatus
from app.models.user import User, UserRole
from app.schemas.review import ReviewCreate, ReviewOut
from sqlalchemy import func
from app.routers.auth import get_current_user

router = APIRouter(prefix="/reviews", tags=["reviews"])

# CREATE REVIEW
@router.post("/", response_model=ReviewOut)
def create_review(review: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    appointment = (
        db.query(Appointment).filter(Appointment.id == review.appointment_id).first()
    )
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

# Duplicate review prevent
    existing_review = (
        db.query(Review).filter(Review.appointment_id == review.appointment_id).first()
    )
    if existing_review:
        raise HTTPException(
            status_code=400, detail="Review already exists for this appointment"
        )

    new_review = Review(
        patient_id=appointment.patient_id,
        nurse_id=appointment.nurse_id,
        appointment_id=appointment.id,
        rating=review.rating,
        comment=review.comment,
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    stats = (
        db.query(
            func.avg(Review.rating).label("average"), 
            # label is used for aliases
            func.count(Review.id).label("count"),
        )
        .filter(Review.nurse_id == appointment.nurse_id)
        .first()
    )

    if stats and stats.average is not None:
        nurse = db.query(User).filter(User.id == appointment.nurse_id).first()
        if nurse:

            nurse.rating = round(stats.average, 1)
            db.commit()

    return new_review


@router.get("/check/{appointment_id}")
def check_review_exists(appointment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    review = db.query(Review).filter(Review.appointment_id == appointment_id).first()
    return {"exists": review is not None}
