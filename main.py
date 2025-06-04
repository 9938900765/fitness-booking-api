from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime
from pytz import timezone
import pytz

app = FastAPI()

 
# Models
 

class FitnessClass(BaseModel):
    id: int
    name: str
    datetime_ist: datetime  # class date and time in IST timezone
    instructor: str
    total_slots: int
    available_slots: int

class BookingRequest(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr

class Booking(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: EmailStr

 
# Globals and Seed Data
 

IST = timezone('Asia/Kolkata')  # IST timezone object

# Predefined fitness classes (seed data)
classes_db: List[FitnessClass] = [
    FitnessClass(
        id=1,
        name="Yoga",
        datetime_ist=IST.localize(datetime(2025, 6, 10, 9, 0)),
        instructor="Anita Sharma",
        total_slots=10,
        available_slots=10,
    ),
    FitnessClass(
        id=2,
        name="Zumba",
        datetime_ist=IST.localize(datetime(2025, 6, 11, 18, 0)),
        instructor="Ravi Kumar",
        total_slots=15,
        available_slots=15,
    ),
    FitnessClass(
        id=3,
        name="HIIT",
        datetime_ist=IST.localize(datetime(2025, 6, 12, 7, 30)),
        instructor="Neha Singh",
        total_slots=12,
        available_slots=12,
    ),
]

# Store bookings in memory
bookings_db: List[Booking] = []

 
# Root Endpoint
 

@app.get("/")
def read_root():
    return {"message": "Welcome to the Fitness Studio Booking API"}

 
# Get all classes
 

@app.get("/classes", response_model=List[FitnessClass])
def get_classes():
    """
    Return list of all upcoming fitness classes.
    """
    return classes_db

 
# Book a class
 

@app.post("/book")
def book_class(booking: BookingRequest):
    """
    Accept a booking request for a fitness class.
    Validates class existence and available slots.
    """
    # Find class by ID
    fitness_class = None
    for c in classes_db:
        if c.id == booking.class_id:
            fitness_class = c
            break
    
    if fitness_class is None:
        raise HTTPException(status_code=404, detail="Fitness class not found")

    if fitness_class.available_slots <= 0:
        raise HTTPException(status_code=400, detail="No available slots for this class")
    
    # Reduce the available slots by 1
    fitness_class.available_slots -= 1
    
    # Create a new booking with a simple incremental ID
    booking_id = len(bookings_db) + 1
    new_booking = Booking(
        id=booking_id,
        class_id=booking.class_id,
        client_name=booking.client_name,
        client_email=booking.client_email,
    )
    bookings_db.append(new_booking)
    
    return {"message": "Booking successful", "booking_id": booking_id}

 
# Get bookings by client email
 

@app.get("/bookings", response_model=List[Booking])
def get_bookings(client_email: EmailStr = Query(..., description="Client email to fetch bookings")):
    """
    Return all bookings made by the given client email.
    """
    user_bookings = []
    for booking in bookings_db:
        # Case-insensitive email comparison
        if booking.client_email.lower() == client_email.lower():
            user_bookings.append(booking)
    return user_bookings
