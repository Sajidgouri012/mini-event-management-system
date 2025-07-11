"""
CRUD operations for event management.
"""

from datetime import datetime, timezone

from sqlalchemy.future import select
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException

from app import models
from app.schemas import events
from  utils.common import ist_to_utc


async def create_event(
    session: AsyncSession, 
    event_in: events.EventCreate
) -> models.Event:
    """
    Create a new event.
    Converts times from IST to UTC and validates constraints.
    Raises HTTPException on failure.
    """
    start_time_utc = ist_to_utc(event_in.start_time)
    end_time_utc = ist_to_utc(event_in.end_time)

    # Check if event name is already taken
    existing = await session.execute(
        select(models.Event).where(models.Event.name == event_in.name)
    )
    if existing.first():
        raise HTTPException(status_code=400, detail="Event name must be unique.")

    if start_time_utc >= end_time_utc:
        raise HTTPException(status_code=400, detail="Start time must be before end time.")

    current_utc = datetime.now(timezone.utc)
    if start_time_utc <= current_utc:
        raise HTTPException(status_code=400, detail="Start time must be in the future.")

    new_event = models.Event(
        name=event_in.name,
        location=event_in.location,
        start_time=start_time_utc,
        end_time=end_time_utc,
        max_capacity=event_in.max_capacity
    )
    session.add(new_event)
    await session.commit()
    await session.refresh(new_event)
    return new_event

async def list_events(
    session: AsyncSession,
    location: str = None,
    start_date: datetime = None,
    end_date: datetime = None
) -> list[models.Event]:
    """
    List upcoming events, optionally filtered by location and date range.
    """
    query = select(models.Event)

    filters = []
    if location:
        filters.append(models.Event.location.ilike(f"%{location}%"))
    if start_date and end_date:
        filters.append(models.Event.start_time.between(start_date, end_date))
    
    if filters:
        query = query.where(and_(*filters))

    result = await session.execute(query)
    return result.scalars().all()