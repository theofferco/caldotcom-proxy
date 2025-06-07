from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import os

app = FastAPI()

@app.post("/")
async def book_appointment(request: Request):
    try:
        data = await request.json()
        print("REQUEST BODY (parsed):", data)
    except Exception as e:
        print("ERROR PARSING JSON:", str(e))
        return JSONResponse(status_code=400, content={"error": "Invalid JSON"})

    try:
        payload = {
            "start": data["start"],
            "eventTypeId": data["eventTypeId"],
            "attendee": {
                "name": data["attendee_name"],
                "email": data["attendee_email"],
                "timeZone": data["attendee_timeZone"]
            }
        }

        headers = {
            "Authorization": f"Bearer {os.environ.get('CAL_API_KEY')}",
            "Content-Type": "application/json",
            "cal-api-version": "2024-09-04"
        }

        response = requests.post("https://api.cal.com/v2/bookings", json=payload, headers=headers)
        print("CAL.COM RESPONSE:", response.status_code, response.text)
        return JSONResponse(content=response.json(), status_code=response.status_code)

    except Exception as e:
        print("ERROR BOOKING APPOINTMENT:", str(e))
        return JSONResponse(status_code=500, content={"error": "Booking failed"})

@app.get("/")
async def health_check():
    return {"message": "Calendar proxy is live"}
