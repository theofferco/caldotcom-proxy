from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import requests
import os

app = FastAPI()

# Booking request with flat input from Hope
class BookingRequest(BaseModel):
    start: str
    eventTypeId: int
    attendee_name: str
    attendee_email: str
    attendee_timeZone: str

@app.post("/")
def book_meeting(request: BookingRequest):
    payload = {
        "start": request.start,
        "eventTypeId": request.eventTypeId,
        "attendee": {
            "name": request.attendee_name,
            "email": request.attendee_email,
            "timeZone": request.attendee_timeZone
        }
    }

    cal_url = "https://api.cal.com/v2/bookings"
    headers = {
        "Authorization": f"Bearer {os.environ.get('CAL_API_KEY')}",
        "Content-Type": "application/json",
        "cal-api-version": "2024-09-04"
    }

    response = requests.post(cal_url, json=payload, headers=headers)
    return JSONResponse(content=response.json(), status_code=response.status_code)

@app.get("/")
def root():
    return JSONResponse(content={"message": "Calendar proxy is live."})

@app.get("/test-cal")
def test_cal_api_key():
    cal_url = "https://api.cal.com/v2/event-types"
    headers = {
        "Authorization": f"Bearer {os.environ.get('CAL_API_KEY')}",
        "cal-api-version": "2024-09-04"
    }

    response = requests.get(cal_url, headers=headers)
    return {
        "status_code": response.status_code,
        "response": response.json()
    }
