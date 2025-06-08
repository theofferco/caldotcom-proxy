from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import requests
import os

app = FastAPI()

class BookingRequest(BaseModel):
    start: str
    eventTypeId: int
    attendee_name: str
    attendee_email: str
    attendee_timeZone: str

@app.post("/")
async def book_meeting(req: BookingRequest):
    payload = {
        "start": req.start,
        "eventTypeId": req.eventTypeId,
        "attendee": {
            "name": req.attendee_name,
            "email": req.attendee_email,
            "timeZone": req.attendee_timeZone
        }
    }

    cal_url = "https://api.cal.com/api/v1/bookings"  # ✅ Use the v1 endpoint

    api_key = os.getenv("CAL_API_KEY")
    print("using API key:", "present" if api_key else "none")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    print("REQUEST BODY (parsed):", payload)

    resp = requests.post(cal_url, json=payload, headers=headers)

    print("CAL.COM RESPONSE:", resp.status_code, resp.text)

    return JSONResponse(content=resp.json(), status_code=resp.status_code)

@app.get("/")
async def root():
    return JSONResponse(content={"message": "Calendar proxy is live."})
