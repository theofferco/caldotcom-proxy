from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import os

app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    print(f"\nREQUEST BODY:\n{body.decode()}\n")
    response = await call_next(request)
    return response

@app.post("/")
async def book_meeting(request: Request):
    try:
        body = await request.json()
    except:
        return JSONResponse(status_code=400, content={"error": "Invalid JSON payload"})

    # Validate required fields
    required_fields = ["start", "eventTypeId", "attendee_name", "attendee_email", "attendee_timeZone"]
    for field in required_fields:
        if field not in body:
            return JSONResponse(status_code=400, content={"error": f"Missing field: {field}"})

    # Build payload for Cal.com
    payload = {
        "start": body["start"],
        "eventTypeId": body["eventTypeId"],
        "attendee": {
            "name": body["attendee_name"],
            "email": body["attendee_email"],
            "timeZone": body["attendee_timeZone"]
        }
    }

    # Send to Cal.com API
    cal_url = "https://api.cal.com/v2/bookings"
    headers = {
        "Authorization": f"Bearer {os.environ.get('CAL_API_KEY')}",
        "Content-Type": "application/json",
        "cal-api-version": "2024-09-04"
    }

    response = requests.post(cal_url, json=payload, headers=headers)
    return JSONResponse(content=response.json(), status_code=response.status_code)

@app.get("/")
async def root():
    return JSONResponse(content={"message": "Calendar proxy is live."})
