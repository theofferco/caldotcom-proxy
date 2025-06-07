from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# Root health check route
@app.get("/")
async def root():
    return JSONResponse(content={"message": "Calendar proxy is live."})

# Booking request model
class BookingRequest(BaseModel):
    start: str
    eventTypeId: int
    attendee_name: str
    attendee_email: str
    attendee_timeZone: str

# Meeting booking endpoint
@app.post("/book")
def book_meeting(request: BookingRequest):
    return {
        "start": request.start,
        "eventTypeId": request.eventTypeId,
        "attendee": {
            "name": request.attendee_name,
            "email": request.attendee_email,
            "timeZone": request.attendee_timeZone
        }
    }
