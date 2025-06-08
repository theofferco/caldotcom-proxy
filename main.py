from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
import requests

app = FastAPI()

class Attendee(BaseModel):
    name: str
    email: str
    timeZone: str

class BookingRequest(BaseModel):
    eventTypeId: int
    start: str
    attendee: Attendee

@app.get("/")
def read_root():
    return {"message": "FastAPI is live."}

@app.get("/test-cal")
def test_cal_key():
    key = os.environ.get("CAL_API_KEY")
    return {
        "status": "success" if key else "error",
        "api_key_present": bool(key),
        "sample_key_fragment": key[-6:] if key else None
    }

@app.post("/test-booking")
def test_booking():
    url = "https://api.cal.com/v2/bookings"
    api_key = os.environ.get("CAL_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "eventTypeId": 1685765,
        "start": "2025-06-10T14:00:00-07:00",
        "attendee": {
            "name": "Chris Brown",
            "email": "chris@theofferco.com",
            "timeZone": "America/Phoenix"
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    return {
        "status_code": response.status_code,
        "response": response.json()
    }
