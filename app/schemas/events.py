"""
Pydantic schemas for Event creation and reading.
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class EventCreate(BaseModel):
    """Schema for creating a new event."""
    name: str = Field(..., description="Name of the event")
    location: str = Field(..., description="Event location")
    start_time: datetime = Field(
        ..., description="Start time in ISO 8601 format (assumed IST)"
    )
    end_time: datetime = Field(
        ..., description="End time in ISO 8601 format (assumed IST)"
    )
    max_capacity: int = Field(gt=0, description="Maximum capacity (> 0)")

class EventRead(BaseModel):
    """Schema for reading event data."""
    id: UUID
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    max_capacity: int

    model_config = ConfigDict(from_attributes=True)
