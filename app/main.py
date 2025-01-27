from fastapi import FastAPI, HTTPException
from app.database import engine, Base
from app.routers import events, attendees

app = FastAPI(title="Event Management API")

try:
    # Create the database tables if they don't exist yet
    Base.metadata.create_all(bind=engine)
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error creating database tables: {e}")

try:
    app.include_router(events.router, prefix="/events", tags=["Events"])
    app.include_router(attendees.router, prefix="/attendees", tags=["Attendees"])
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error loading routers: {e}")
