# D:\Even_management_new\tests\test_attendees.py

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app
from app.models import Event, Attendee
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


def create_sample_event(db, max_attendees=10):
    """Helper function to create a sample event."""
    event = Event(
        name="Sample Event",
        description="A test event",
        start_time=datetime.now() + timedelta(days=1),
        end_time=datetime.now() + timedelta(days=2),
        location="Test Location",
        max_attendees=max_attendees,
        status="SCHEDULED",
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def create_sample_attendee(db, event_id, name="Test Attendee"):
    """Helper function to create a sample attendee."""
    attendee = Attendee(
        name=name,
        email="test@example.com",
        event_id=event_id,
        checked_in=False,
    )
    db.add(attendee)
    db.commit()
    db.refresh(attendee)
    return attendee


def test_registration_limits(test_db):
    """Test that registration respects the maximum attendee limit."""
    db = test_db
    event = create_sample_event(db, max_attendees=2)

    # Register two attendees
    for i in range(2):
        response = client.post(
            f"/events/{event.event_id}/attendees",
            json={"name": f"Attendee {i+1}", "email": f"attendee{i+1}@example.com"},
        )
        assert response.status_code == 201
        assert response.json()["name"] == f"Attendee {i+1}"

    # Attempt to register a third attendee
    response = client.post(
        f"/events/{event.event_id}/attendees",
        json={"name": "Attendee 3", "email": "attendee3@example.com"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Registration limit reached for this event."


def test_check_in(test_db):
    """Test that attendees can check in to an event."""
    db = test_db
    event = create_sample_event(db)
    attendee = create_sample_attendee(db, event.event_id)

    # Check in the attendee
    response = client.post(f"/events/{event.event_id}/attendees/{attendee.id}/check-in")
    assert response.status_code == 200
    assert response.json()["checked_in"] is True

    # Attempt to check in the same attendee again
    response = client.post(f"/events/{event.event_id}/attendees/{attendee.id}/check-in")
    assert response.status_code == 400
    assert response.json()["detail"] == "Attendee already checked in."


def test_invalid_event_registration(test_db):
    """Test registering an attendee for a non-existent event."""
    response = client.post(
        "/events/999/attendees",
        json={"name": "Invalid Attendee", "email": "invalid@example.com"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found."


def test_invalid_check_in(test_db):
    """Test checking in to a non-existent event or attendee."""
    # Attempt to check in a non-existent attendee
    response = client.post("/events/999/attendees/1/check-in")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event or attendee not found."
