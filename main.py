
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

@app.post("/proxy")
async def proxy(request: Request):
    body = await request.json()

    # Transform flat body into nested Cal.com-compatible structure
    transformed = {
        "start": body.get("start"),
        "eventTypeId": body.get("eventTypeId"),
        "attendee": {
            "name": body.get("attendee_name"),
            "email": body.get("attendee_email"),
            "timeZone": "America/Phoenix"  # Always Phoenix timezone
        }
    }

    return JSONResponse(content=transformed)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
