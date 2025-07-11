"""
Pydantic schemas for Attendee creation and reading.
"""

from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class AttendeeCreate(BaseModel):
    """Schema for creating a new attendee."""
    name: str = Field(..., description="Full name of the attendee")
    email: EmailStr = Field(..., description="Unique email address for registration")

class AttendeeRead(BaseModel):
    """Schema for reading attendee data."""
    id: UUID
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
