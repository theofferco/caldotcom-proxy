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
    # Prepare nested payload
    payload = {
        "start": request.start,
        "eventTypeId": request.eventTypeId,
        "attendee": {
            "name": request.attendee_name,
            "email": request.attendee_email,
            "timeZone": request.attendee_timeZone
        }
    }

    # ✅ Corrected Cal.com API URL (removed /v2)
    cal_url = "https://api.cal.com/bookings"
    headers = {
        "Authorization": f"Bearer {os.environ.get('CAL_API_KEY')}",
        "Content-Type": "application/json"
    }

    response = requests.post(cal_url, json=payload, headers=headers)

    # Return Cal.com response
    return JSONResponse(content=response.json(), status_code=response.status_code)

@app.get("/")
async def root():
    return JSONResponse(content={"message": "Calendar proxy is live."})
