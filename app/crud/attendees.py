"""
CRUD operations for attendee management.
"""

from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app import models
from app.schemas import attendees


# Register attendee

async def register_attendee(
    session: AsyncSession,
    event_id: UUID,
    attendee_in: attendees.AttendeeCreate
) -> models.Attendee:
    """
    Register a new attendee for an event.
    Validates event existence, timing, capacity, and duplicate email.
    Raises HTTPException on failure.
    """
    event = await session.get(models.Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    # Check if event has started
    if event.start_time.tzinfo is None:
        event_start = event.start_time.replace(tzinfo=timezone.utc)
    else:
        event_start = event.start_time.astimezone(timezone.utc)
    now_utc = datetime.now(timezone.utc)
    if now_utc >= event_start:
        raise HTTPException(status_code=400, detail="Registration closed: event has already started.")

    # Check for overbooking
    result = await session.execute(
        select(models.Attendee).where(models.Attendee.event_id == event.id)
    )
    attendees = result.scalars().all()
    if len(attendees) >= event.max_capacity:
        raise HTTPException(status_code=400, detail="Event is fully booked.")

    # Check for duplicate email
    result = await session.execute(
        select(models.Attendee).where(
            models.Attendee.event_id == event.id,
            models.Attendee.email == attendee_in.email
        )
    )
    if result.first():
        raise HTTPException(status_code=400, detail="Email already registered for this event.")

    new_attendee = models.Attendee(
        name=attendee_in.name,
        email=attendee_in.email,
        event_id=event.id
    )
    session.add(new_attendee)
    await session.commit()
    await session.refresh(new_attendee)
    return new_attendee

# List attendees with pagination

async def list_attendees(
    session: AsyncSession,
    event_id: UUID,
    page: int = 1,
    page_size: int = 10
) -> list[models.Attendee]:
    """
    List attendees for an event with pagination.
    Raises HTTPException if event not found.
    """
    event = await session.get(models.Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    offset = (page - 1) * page_size
    query = (
        select(models.Attendee)
        .where(models.Attendee.event_id == event.id)
        .offset(offset)
        .limit(page_size)
    )

    result = await session.execute(query)
    return result.scalars().all()
