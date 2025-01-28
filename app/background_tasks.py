from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.models import Event, EventStatus
from datetime import datetime


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


scheduler = BackgroundScheduler()
scheduler.add_job(update_event_statuses, "interval", minutes=2)
scheduler.start()
