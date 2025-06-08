from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os
import requests

app = FastAPI()

class BookingRequest(BaseModel):
    start: str
    eventTypeId: int
    attendee_name: str
    attendee_email: str
    attendee_timeZone: str

@app.post("/")
def book_meeting(req: BookingRequest):
    api_key = os.environ.get("CAL_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="CAL_API_KEY is missing.")

    print("✅ API KEY EXISTS:", bool(api_key))  # this will log True if it found the key

    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
        "cal-api-version": "2024-09-04"
    }

    payload = {
        "start": req.start,
        "eventTypeId": req.eventTypeId,
        "attendee": {
            "name": req.attendee_name,
            "email": req.attendee_email,
            "timeZone": req.attendee_timeZone
        }
    }

    url = "https://api.cal.com/v2/bookings"
    response = requests.post(url, json=payload, headers=headers)

    print("📡 CAL.COM STATUS:", response.status_code)
    print("📨 CAL.COM BODY:", response.text)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return JSONResponse(content=response.json())

@app.get("/")
def root():
    return {"message": "Calendar proxy is live."}
