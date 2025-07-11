"""
SQLAlchemy ORM models for the Event Management System.
"""

import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Event(Base):
    """Database model for an event."""
    __tablename__ = "events"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    location = Column(String(255), nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    max_capacity = Column(Integer, nullable=False)

    attendees = relationship(
        "Attendee", back_populates="event", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Event(id={self.id}, name={self.name})>"

class Attendee(Base):
    """Database model for an attendee."""
    __tablename__ = "attendees"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    event_id = Column(PG_UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)

    event = relationship("Event", back_populates="attendees")

    __table_args__ = (
        UniqueConstraint('event_id', 'email', name='_event_email_uc'),
    )

    def __repr__(self):
        return f"<Attendee(id={self.id}, email={self.email})>"
