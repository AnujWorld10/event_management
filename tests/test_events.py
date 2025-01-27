# D:\Even_management_new\tests\test_events.py

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app
from app.models import Event
from app.database import SessionLocal

client = TestClient(app)


@pytest.fixture(scope="function")
def test_db():
    """
    Provides a clean database session for testing.
    Rolls back any changes after each test.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


def create_sample_event_data():
    """Helper function to generate sample event data."""
    return {
        "name": "Test Event",
        "description": "This is a test event",
        "start_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "end_time": (datetime.now() + timedelta(days=2)).isoformat(),
        "location": "Test Location",
        "max_attendees": 50,
    }


def create_sample_event(db):
    """Helper function to create a sample event in the database."""
    event = Event(
        name="Test Event",
        description="This is a test event",
        start_time=datetime.now() + timedelta(days=1),
        end_time=datetime.now() + timedelta(days=2),
        location="Test Location",
        max_attendees=50,
        status="SCHEDULED",
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def test_create_event(test_db):
    """Test creating a new event."""
    event_data = create_sample_event_data()

    response = client.post("/events", json=event_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == event_data["name"]
    assert response_data["description"] == event_data["description"]
    assert response_data["max_attendees"] == event_data["max_attendees"]


def test_get_event(test_db):
    """Test fetching details of an event."""
    db = test_db
    event = create_sample_event(db)

    response = client.get(f"/events/{event.event_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == event.name
    assert response_data["description"] == event.description


def test_get_nonexistent_event():
    """Test fetching a non-existent event."""
    response = client.get("/events/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found."


def test_update_event(test_db):
    """Test updating an event."""
    db = test_db
    event = create_sample_event(db)

    updated_data = {"name": "Updated Event Name", "description": "Updated description"}
    response = client.put(f"/events/{event.event_id}", json=updated_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == updated_data["name"]
    assert response_data["description"] == updated_data["description"]


def test_update_nonexistent_event():
    """Test updating a non-existent event."""
    updated_data = {"name": "Updated Event Name", "description": "Updated description"}
    response = client.put("/events/999", json=updated_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found."


def test_delete_event(test_db):
    """Test deleting an event."""
    db = test_db
    event = create_sample_event(db)

    response = client.delete(f"/events/{event.event_id}")
    assert response.status_code == 204

    # Verify the event was deleted
    response = client.get(f"/events/{event.event_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found."


def test_delete_nonexistent_event():
    """Test deleting a non-existent event."""
    response = client.delete("/events/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found."
