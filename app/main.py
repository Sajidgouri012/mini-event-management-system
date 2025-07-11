"""
FastAPI application entrypoint for the Mini Event Management System.
"""

from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware

from app.routers import events
from app.routers import attendees
from utils.common import limiter

app = FastAPI(
    title="Mini Event Management System",
    description="API for creating events, registering attendees, viewing attendee lists.",
    version="1.0.0"
)

# Rate limiter
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# API Version prefix
URL_PREFIX = "/api/v1/events"

# Register routers
app.include_router(events.router, prefix=URL_PREFIX, tags=["Events"])
app.include_router(attendees.router, prefix=URL_PREFIX, tags=["Attendees"])

# Health check endpoint
@app.get(f"{URL_PREFIX}/health", tags=["Health"])
async def root():
    return {"message": "Event Management API is running."}
