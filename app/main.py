import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import Base, engine
from app.models.user import User
from app.models.appointment import Appointment
from app.models.vital import Vitals
from app.models.community import Community
from app.models.inquiry import Inquiry
from app.models.review import Review

print("Registered tables:", Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)

from app.routers import (
    auth,
    users,
    appointments,
    vitals,
    communities,
    inquiries,
    reviews,
)

app = FastAPI(title="ElderConnect API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(appointments.router)
app.include_router(vitals.router)
app.include_router(communities.router)
app.include_router(inquiries.router)
app.include_router(reviews.router)


@app.get("/")
async def root():
    return {"message": "Welcome to ElderConnect API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
