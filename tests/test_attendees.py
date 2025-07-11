"""
Test module for attendee registration endpoints.
"""

import pytest
import datetime
import pytz

@pytest.mark.asyncio
async def test_register_attendee_success(client):
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "name": "Test Event",
        "location": "Pune",
        "start_time": (now + datetime.timedelta(days=1)).isoformat(),
        "end_time": (now + datetime.timedelta(days=2)).isoformat(),
        "max_capacity": 2
    }
    create_response = await client.post("/events/", json=payload)
    assert create_response.status_code == 200
    event_id = create_response.json()["id"]

    # Register attendee
    response = await client.post(f"/events/{event_id}/register", json={
        "name": "Alice",
        "email": "alice@example.com"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alice@example.com"


@pytest.mark.asyncio
async def test_prevent_duplicate_registration(client):
    event_response = await client.get("/events/")
    event_id = event_response.json()[0]["id"]

    # Try registering with same email again
    response = await client.post(f"/events/{event_id}/register", json={
        "name": "Alice",
        "email": "alice@example.com"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_overbooking(client):
    event_response = await client.get("/events/")
    event_id = event_response.json()[0]["id"]

    # Assuming capacity=2 from earlier test, we already have 1
    await client.post(f"/events/{event_id}/register", json={
        "name": "Bob",
        "email": "bob@example.com"
    })

    # Try to exceed capacity
    response = await client.post(f"/events/{event_id}/register", json={
        "name": "Charlie",
        "email": "charlie@example.com"
    })
    assert response.status_code == 400
    assert "fully booked" in response.json()["detail"]


@pytest.mark.asyncio
async def test_rate_limiting_on_registration(client):
    # Create a valid future event
    now = datetime.datetime.utcnow()
    payload = {
        "name": "Rate Limited Event",
        "location": "Chennai",
        "start_time": (now + datetime.timedelta(days=20)).isoformat(),
        "end_time": (now + datetime.timedelta(days=21)).isoformat(),
        "max_capacity": 100
    }
    create_response = await client.post("/events/", json=payload)
    assert create_response.status_code == 200
    event_id = create_response.json()["id"]

    # Register 5 times successfully
    for i in range(10):
        r = await client.post(f"/events/{event_id}/register", json={
            "name": f"user{i}",
            "email": f"user{i}@example.com"
        })
        assert r.status_code == 200

    # 6th time should hit rate limit
    r = await client.post(f"/events/{event_id}/register", json={
        "name": "user11",
        "email": "user11@example.com"
    })

    assert r.status_code == 429


@pytest.mark.asyncio
async def test_booking_not_allowed_after_event_start(client):
    """
    Ensure that registration fails if the event has already started.
    """

    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.datetime.now(ist)

    # Create event that already started
    start_time = (now + datetime.timedelta(milliseconds=2)).isoformat()
    end_time = (now + datetime.timedelta(hours=2)).isoformat()

    # Create event
    payload = {
        "name": "Already Started Event",
        "location": "Test City",
        "start_time": start_time,
        "end_time": end_time,
        "max_capacity": 20
    }
    create_response = await client.post("/events/", json=payload)
    assert create_response.status_code == 200
    event_id = create_response.json()["id"]
    # Now try to register
    register_payload = {
        "name": "Late User",
        "email": "lateuser@example.com"
    }
    response = await client.post(f"/events/{event_id}/register", json=register_payload)
    assert response.status_code == 400
    assert "Registration closed: event has already started" in response.text