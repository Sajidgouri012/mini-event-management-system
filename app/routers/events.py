"""
Event-related API routes.
"""

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
import pytz

from app.database.db_connection import get_session
from app.schemas.events import EventCreate, EventRead
from app.crud.events import create_event, list_events
from fastapi import HTTPException

router = APIRouter()

@router.post("/", response_model=EventRead)
async def register_event(
    request: Request,
    event: EventCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Register a new event with IST to UTC conversion.
    """
    return await create_event(session, event)

@router.get("/", response_model=List[EventRead])
# Note: This endpoint intentionally not rate-limited for public access
async def get_events(
    request: Request,
    location: Optional[str] = Query(None, description="Filter by location"),
    start_date: Optional[datetime] = Query(None, description="Filter start date (UTC)"),
    end_date: Optional[datetime] = Query(None, description="Filter end date (UTC)"),
    tz: Optional[str] = Query("UTC", description="Timezone for output datetimes"),
    session: AsyncSession = Depends(get_session)
):
    """
    List upcoming events with optional filtering and timezone conversion.
    """
    
    events = await list_events(session, location, start_date, end_date)

    # Convert UTC times to requested timezone
    try:
        target_tz = pytz.timezone(tz)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid timezone: {tz}")

    for event in events:
        event.start_time = event.start_time.astimezone(target_tz)
        event.end_time = event.end_time.astimezone(target_tz)

    return events
