from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Event, EventStatus


# Function to update event status to 'completed' if the end_time has passed
def update_event_status_if_needed(db: Session, event: Event):
    # Check if the event's end_time has passed
    if event.end_time and event.end_time < datetime.now():
        if event.status != EventStatus.COMPLETED:
            event.status = EventStatus.COMPLETED
            db.commit()
            db.refresh(event)


# # Fetch events or perform other operations
# def get_event(event_id: int, db: Session):
#     event = db.query(Event).filter(Event.event_id == event_id).first()
#     if event:
#         update_event_status_if_needed(db, event)  # Update status if needed
#     return event
