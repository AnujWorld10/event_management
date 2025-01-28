from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Event, EventStatus


def update_event_status_if_needed(db: Session, event: Event):
    if event.end_time and event.end_time < datetime.now():
        if event.status != EventStatus.COMPLETED:
            event.status = EventStatus.COMPLETED
            db.commit()
            db.refresh(event)
