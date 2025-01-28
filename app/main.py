from fastapi import FastAPI, HTTPException
from app.database import engine, Base
from app.routers import events, attendees
from app import update_event_status
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.database import SessionLocal
from app.models import Event, EventStatus
from app.routers import check_in


# Initialize FastAPI app
app = FastAPI(title="Event Management API")


# Function to update event statuses periodically
def update_event_statuses():
    db = SessionLocal()
    events = (
        db.query(Event)
        .filter(Event.end_time < datetime.now(), Event.status != EventStatus.COMPLETED)
        .all()
    )
    for event in events:
        event.status = EventStatus.COMPLETED
        db.commit()
    db.close()


# Schedule the background job to run every 10 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(update_event_statuses, "interval", minutes=10)
scheduler.start()

# Create the database tables if they don't exist yet
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error creating database tables: {e}")

# Include routers for events and attendees
try:
    app.include_router(events.router, prefix="/events", tags=["Events"])
    app.include_router(attendees.router, prefix="/attendees", tags=["Attendees"])
    app.include_router(check_in.router, prefix="/attendees", tags=["Attendees"])

except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error loading routers: {e}")
