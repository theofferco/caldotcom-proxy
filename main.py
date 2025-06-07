from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

class BookingRequest(BaseModel):
    start: str
    eventTypeId: int
    attendee_name: str
    attendee_email: str
    attendee_timeZone: str

@app.post("/")
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

@app.get("/")
async def root():
    return JSONResponse(content={"message": "Calendar proxy is live."})
