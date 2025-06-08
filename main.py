import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

CAL_API_KEY = os.getenv("CAL_API_KEY")

headers = {
    "Authorization": f"Bearer {CAL_API_KEY}",
    "Content-Type": "application/json"
}

class Attendee(BaseModel):
    name: str
    email: str
    timeZone: str

class BookingRequest(BaseModel):
    eventTypeId: int
    start: str
    attendee: Attendee

@app.get("/")
def root():
    return {"message": "Cal.com Proxy is live."}

@app.get("/test-cal")
def test_cal_connection():
    url = "https://api.cal.com/v2/event-types"
    response = requests.get(url, headers=headers)
    return {"status_code": response.status_code, "response": response.json()}

@app.post("/")
def create_booking(request: BookingRequest):
    url = "https://api.cal.com/v2/bookings"
    data = {
        "eventTypeId": request.eventTypeId,
        "start": request.start,
        "attendee": {
            "name": request.attendee.name,
            "email": request.attendee.email,
            "timeZone": request.attendee.timeZone
        }
    }
    response = requests.post(url, headers=headers, json=data)
    return {"status_code": response.status_code, "response": response.json()}
