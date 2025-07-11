"""
Attendee-related API routes.
"""

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.schemas.attendees import AttendeeCreate, AttendeeRead
from app.crud.attendees import register_attendee, list_attendees
from app.database.db_connection import get_session
from utils.common import limiter

router = APIRouter()

@router.post("/{event_id}/register", response_model=AttendeeRead)
@limiter.limit("10/minute")
async def register_event_attendee(
    request: Request,
    event_id: UUID,
    attendee: AttendeeCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Register a new attendee for an event.
    """
    return await register_attendee(session, event_id, attendee)

@router.get("/{event_id}/attendees", response_model=List[AttendeeRead])
async def list_event_attendees(
    request: Request,
    event_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_session)
):
    """
    List attendees for a specific event with pagination.
    """
    return await list_attendees(session, event_id, page, page_size)