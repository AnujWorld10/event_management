from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database import SessionLocal
from app.models import Event, EventStatus
from app.schemas import EventCreate, EventUpdate, EventResponse
from datetime import datetime
from app.update_event_status import update_event_status_if_needed

router = APIRouter()


# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error while interacting with the database: {e}"
        )
    finally:
        db.close()


# Create a new event
@router.post("/", response_model=EventResponse)
async def create_event(event: EventCreate, db: Session = Depends(get_db)):
    try:
        # Validate start and end times
        if event.start_time >= event.end_time:
            raise HTTPException(
                status_code=400, detail="Start time must be before end time"
            )

        if event.max_attendees <= 0:
            raise HTTPException(
                status_code=400,
                detail=f"Maximum attendees can't be {event.max_attendees}",
            )

        # Check if event.status is a string, then convert to EventStatus enum
        if isinstance(event.status, str):
            status_enum = (
                EventStatus[event.status.upper()]
                if event.status
                else EventStatus.SCHEDULED
            )
        else:
            status_enum = event.status or EventStatus.SCHEDULED

        db_event = Event(
            name=event.name,
            description=event.description,
            start_time=event.start_time,
            end_time=event.end_time,
            location=event.location,
            max_attendees=event.max_attendees,
            status=status_enum,
        )

        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating event: {e}")


# Update an existing event
@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int, updated_event: EventUpdate, db: Session = Depends(get_db)
):
    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    for key, value in updated_event.dict(exclude_unset=True).items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event


# Get a list of events (with optional filters)
@router.get("/", response_model=List[EventResponse])
async def list_events(
    status: Optional[str] = None,
    location: Optional[str] = None,
    date: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    try:
        query = db.query(Event)

        if status:
            if status.upper() not in EventStatus.__members__:
                raise HTTPException(status_code=400, detail="Invalid status value")
            query = query.filter(Event.status == EventStatus[status.upper()])
        if location:
            query = query.filter(Event.location.ilike(f"%{location}%"))
        if date:
            query = query.filter(Event.start_time.date() == date.date())

        events = query.all()
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching events: {e}")


# Get details of a single event by its ID
@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    try:
        event = db.query(Event).filter(Event.event_id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        # Update the status if needed (check if event is completed)
        update_event_status_if_needed(db, event)

        # Commit changes to the database (if the status was updated)
        db.commit()
        db.refresh(event)

        return event
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching event: {e}")


# # Delete an event by its ID
# @router.delete("/{event_id}")
# async def delete_event(event_id: int, db: Session = Depends(get_db)):
#     try:
#         event = db.query(Event).filter(Event.event_id == event_id).first()
#         if not event:
#             raise HTTPException(status_code=404, detail="Event not found")

#         db.delete(event)
#         db.commit()
#         return {"message": "Event deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error deleting event: {e}")
