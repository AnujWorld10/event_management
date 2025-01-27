from fastapi import APIRouter, HTTPException, Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Attendee, Event
from app.schemas import AttendeeCreate, AttendeeUpdate, AttendeeResponse
from typing import List, Optional

router = APIRouter()


# API to create an attendee
@router.post("/", response_model=AttendeeResponse)
async def create_attendee(attendee: AttendeeCreate, db: Session = Depends(get_db)):
    try:
        existing_attendee = (
            db.query(Attendee).filter(Attendee.email == attendee.email).first()
        )
        if existing_attendee:
            raise HTTPException(
                status_code=400,
                detail=f"Attendee with email '{attendee.email}' already exists.",
            )

        db_attendee = Attendee(
            first_name=attendee.first_name,
            last_name=attendee.last_name,
            email=attendee.email,
            phone_number=attendee.phone_number,
            event_id=attendee.event_id,
            check_in_status=attendee.check_in_status,
        )

        db.add(db_attendee)
        db.commit()
        db.refresh(db_attendee)
        return db_attendee

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Duplicate entry: {e.orig.args[1]}"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating attendee: {e}")


# API to update an attendee
@router.put("/{attendee_id}", response_model=AttendeeResponse)
async def update_attendee(
    attendee_id: int, attendee: AttendeeUpdate, db: Session = Depends(get_db)
):
    try:
        db_attendee = (
            db.query(Attendee).filter(Attendee.attendee_id == attendee_id).first()
        )
        if not db_attendee:
            raise HTTPException(status_code=404, detail="Attendee not found")

        for key, value in attendee.dict(exclude_unset=True).items():
            setattr(db_attendee, key, value)

        db.commit()
        db.refresh(db_attendee)
        return db_attendee
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating attendee: {e}")


# API to list all attendees or filter by event and check-in status
@router.get("/", response_model=List[AttendeeResponse])
async def list_attendees(
    event_id: Optional[int] = None,
    check_in_status: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    try:
        query = db.query(Attendee)

        if event_id:
            query = query.filter(Attendee.event_id == event_id)
        if check_in_status is not None:
            query = query.filter(Attendee.check_in_status == check_in_status)

        attendees = query.all()
        return attendees
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching attendees: {e}")


# API to fetch a specific attendee by ID
@router.get("/{attendee_id}", response_model=AttendeeResponse)
async def get_attendee(attendee_id: int, db: Session = Depends(get_db)):
    try:
        db_attendee = (
            db.query(Attendee).filter(Attendee.attendee_id == attendee_id).first()
        )
        if not db_attendee:
            raise HTTPException(status_code=404, detail="Attendee not found")
        return db_attendee
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching attendee: {e}")


# API to delete an attendee
@router.delete("/{attendee_id}")
async def delete_attendee(attendee_id: int, db: Session = Depends(get_db)):
    try:
        db_attendee = (
            db.query(Attendee).filter(Attendee.attendee_id == attendee_id).first()
        )
        if not db_attendee:
            raise HTTPException(status_code=404, detail="Attendee not found")

        db.delete(db_attendee)
        db.commit()
        return {"message": "Attendee deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting attendee: {e}")
