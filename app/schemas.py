from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models import EventStatus


class AttendeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    event_id: int


class AttendeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    check_in_status: Optional[bool] = None


class AttendeeResponse(BaseModel):
    attendee_id: int
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str]
    event_id: int
    check_in_status: bool

    class Config:
        from_attributes = True


class EventCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: str
    max_attendees: int
    status: Optional[EventStatus]


class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    max_attendees: Optional[int] = None


class EventResponse(BaseModel):
    event_id: int
    name: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    location: str
    max_attendees: int
    status: str

    class Config:
        from_attributes = True
