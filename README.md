# Fitness Studio Booking API

This is a simple backend API built with **FastAPI** for a fictional fitness studio.  
Clients can view available fitness classes, book a spot, and view their bookings.

---

## Objective

- Provide API endpoints for listing classes, booking a class, and viewing bookings by client email.
- Handle slot availability and prevent overbooking.
- Manage class timings in **IST timezone**, adjusting correctly for client timezones.
- Use an **in-memory data store** (no external DB setup required).
- Include error handling and basic input validation.

---

## Tech Stack

- Python 3.8+
- FastAPI
- Uvicorn (ASGI server)
- Pydantic (data validation)
- pytz (timezone handling)

---

## Setup Instructions

1. **Clone or download** the project files.

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv fitness-studio-booking-api
   # On Windows
   fitness-studio-booking-api\Scripts\activate
   # On macOS/Linux
   source fitness-studio-booking-api/bin/activate

3. Install dependencies:

    pip install fastapi uvicorn pydantic pytz
    pip install email-validator

4. Run the app with hot reload:

    uvicorn main:app --reload

5. Access the API at: http://127.0.0.1:8000, 
   Swagger Documentation at: http://127.0.0.1:8000/docs

API Endpoints:

1. Get all upcoming classes
    URL: /classes
    Method: GET
    Response: List of fitness classes with name, date/time (in IST), instructor, total and available slots.

2. Book a class spot
    URL: /book
    Method: POST
    Request body:
    {
    "class_id": 1,
    "client_name": "John Doe",
    "client_email": "john@example.com"
    }

3. Get bookings by client email
    URL: /bookings
    Method: GET
    Query parameter: client_email (required)
    Response: List of bookings for that email.
    