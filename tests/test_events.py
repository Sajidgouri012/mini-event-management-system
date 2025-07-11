# tests/test_events.py

import pytest
from datetime import datetime, timedelta
import pytz
from utils.common import get_ist_datetime


@pytest.mark.asyncio
async def test_create_event(client):
    response = await client.post("/events/", json={
        "name": "Event",
        "location": "Pune",
        "start_time": get_ist_datetime(2).isoformat(),
        "end_time": get_ist_datetime(4).isoformat(),
        "max_capacity": 2
    })
    assert response.status_code == 200


##Create Event before current date
@pytest.mark.asyncio
async def test_event_start_time_in_past(client):
    ist = pytz.timezone("Asia/Kolkata")
    past_start = datetime.now(ist) - timedelta(days=1)
    future_end = datetime.now(ist) + timedelta(days=1)

    payload = {
        "name": "Past Event",
        "location": "test town, Pune",
        "start_time": past_start.isoformat(),
        "end_time": future_end.isoformat(),
        "max_capacity": 20
    }

    response = await client.post("/events/", json=payload)
    assert response.status_code == 400
    assert "Start time must be in the future" in response.text


##Test Event With Location Filter
@pytest.mark.asyncio
async def test_list_events_with_location_filter(client):
    response = await client.get("/events/?location=Pune")
    assert response.status_code == 200
    events = response.json()
    assert any("Pune" in event["location"] for event in events)


##Test Event With date range Filter
@pytest.mark.asyncio
async def test_event_filter_by_date_range(client):
    # Create 2 events: one in range, one out
    now = datetime.utcnow()
    # Apply filter
    start_date = (now + timedelta(days=1)).date()
    end_date = (now + timedelta(days=10)).date()
    response = await client.get(f"/events/?start_date={start_date}&end_date={end_date}")
    
    assert response.status_code == 200
    events = response.json()
    assert any(e["name"] == "Test Event" for e in events)
    assert not any(e["name"] == "Rate Limited Event" for e in events)


@pytest.mark.asyncio
async def test_event_name_uniqueness(client):
    # Create an event
    payload = {
        "name": "UniqueEvent",
        "location": "Hyderabad",
        "start_time": get_ist_datetime(2).isoformat(),
        "end_time": get_ist_datetime(4).isoformat(),
        "max_capacity": 50
    }
    r1 = await client.post("/events/", json=payload)
    assert r1.status_code == 200

    # Try creating again with same name
    r2 = await client.post("/events/", json=payload)
    assert r2.status_code == 400
    assert "unique" in r2.text.lower()
