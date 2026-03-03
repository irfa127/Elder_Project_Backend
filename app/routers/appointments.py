from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.dependencies import get_db
from app.models.appointment import Appointment, AppointmentStatus
from app.models.review import Review
from app.models.user import User
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse,
)
from typing import List
from app.routers.auth import get_current_user

router = APIRouter(prefix="/appointments", tags=["Appointments"])

# book-appointment.html patient_dashboard.html (Book button click)
@router.post("/", response_model=AppointmentResponse)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:

        existing = (
            db.query(Appointment)
            .filter(
                Appointment.nurse_id == appointment.nurse_id,
                Appointment.appointment_date == appointment.appointment_date,
                Appointment.appointment_time == appointment.appointment_time,
                Appointment.status.in_(["PENDING", "ACCEPTED"]),
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400, detail="Nurse not available at the selected time"
            )

        new_appointment = Appointment(**appointment.dict())
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)
        return new_appointment
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()

        if "foreign key constraint" in str(e).lower():
            raise HTTPException(
                status_code=400,
                detail="Invalid patient_id or nurse_id. User does not exist.",
            )
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# nurse ku get apoinment
@router.get("/")
def get_appointments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        appointments = db.query(Appointment).all()
        results = []
        for a in appointments:
            results.append(
                {
                    "id": a.id,
                    "patient_id": a.patient_id,
                    "nurse_id": a.nurse_id,
                    "appointment_date": a.appointment_date,
                    "appointment_time": a.appointment_time,
                    "service_type": a.service_type,
                    "status": (
                        str(a.status.value)
                        if hasattr(a.status, "value")
                        else str(a.status)
                    ),
                    "notes": a.notes,
                    "created_at": a.created_at,
                }
            )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching appointments: {str(e)}"
        )

# My Appointments
@router.get("/patient/{patient_id}")
def get_patient_appointments(patient_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        appointments = (
            db.query(Appointment).filter(Appointment.patient_id == patient_id).all()
        )
        results = []
        for a in appointments:

            has_review = (
                db.query(Review).filter(Review.appointment_id == a.id).first()
                is not None
            )

            nurse = db.query(User).filter(User.id == a.nurse_id).first()
            nurse_name = nurse.full_name if nurse else f"Nurse #{a.nurse_id}"
            nurse_image = nurse.profile_picture

            results.append(
                {
                    "id": a.id,
                    "patient_id": a.patient_id,
                    "nurse_id": a.nurse_id,
                    "nurse_name": nurse_name,
                    "nurse_image": nurse_image,
                    "appointment_date": a.appointment_date,
                    "appointment_time": a.appointment_time,
                    "service_type": a.service_type,
                    "status": (
                        str(a.status.value)
                        if hasattr(a.status, "value")
                        else str(a.status)
                    ),
                    "notes": a.notes,
                    "created_at": a.created_at,
                    "has_review": has_review,
                }
            )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching patient appointments: {str(e)}"
        )

# Nurse Dashboard
@router.get("/nurse/{nurse_id}")
def get_nurse_appointments(nurse_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        appointments = (
            db.query(Appointment).filter(Appointment.nurse_id == nurse_id).all()
        )

        results = []
        for a in appointments:

            patient = db.query(User).filter(User.id == a.patient_id).first()
            patient_name = patient.full_name if patient else f"Patient #{a.patient_id}"
            patient_image = patient.profile_picture

            results.append(
                {
                    "id": a.id,
                    "patient_id": a.patient_id,
                    "patient_name": patient_name,
                    "patient_image": patient_image,
                    "nurse_id": a.nurse_id,
                    "appointment_date": a.appointment_date,
                    "appointment_time": a.appointment_time,
                    "service_type": a.service_type,
                    "status": (
                        str(a.status.value)
                        if hasattr(a.status, "value")
                        else str(a.status)
                    ),
                    "notes": a.notes,
                    "created_at": a.created_at,
                }
            )
        return results
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"Error fetching appointments for nurse {nurse_id}: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching nurse appointments: {str(e)}"
        )

# Appointment Detail
@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

# Update Status nurse and 
@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment_update: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    old_status = (
        appointment.status.value
        if hasattr(appointment.status, "value")
        else str(appointment.status)
    )
    new_status = appointment_update.status.value if hasattr(appointment_update.status, "value") else str(appointment_update.status)

    # Status Order Mapping
    status_order = {
        "PENDING": 1,
        "ON_THE_WAY": 2,
        "ARRIVED": 3,
        "COMPLETED": 4,
    }

    if new_status in status_order and old_status in status_order:
        old_val = status_order[old_status]
        new_val = status_order[new_status]

        # Rule: No skipping, No backwards
        if new_val != old_val + 1:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid transition from {old_status} to {new_status}. Steps must be followed in order."
            )

        # Rule: Cannot complete before appointment time
        if new_status == "COMPLETED":
            from datetime import datetime, time
            
            appt_date = appointment.appointment_date # This is already a DateTime object
            try:
                # Assuming appointment_time is "HH:mm"
                hour, minute = map(int, appointment.appointment_time.split(':'))
                appt_full_time = datetime.combine(appt_date.date(), time(hour, minute))
                
                if datetime.now() < appt_full_time:
                    raise HTTPException(
                        status_code=400,
                        detail="Visit cannot be completed before the scheduled appointment time."
                    )
            except ValueError:
                # fallback if time format is weird
                pass

    for key, value in appointment_update.dict(exclude_unset=True).items():
        setattr(appointment, key, value)

    db.commit()
    db.refresh(appointment)
    return appointment

# Cancel
@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(appointment)
    db.commit()
    return {"message": "Appointment deleted successfully"}

