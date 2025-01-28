from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Attendee
import csv
from io import StringIO

router = APIRouter()


@router.post("/check-in/{attendee_id}", tags=["Attendees"])
async def check_in_attendee(attendee_id: int, db: Session = Depends(get_db)):
    """
    Marks an attendee as checked in by their ID.
    """
    try:
        attendee = (
            db.query(Attendee).filter(Attendee.attendee_id == attendee_id).first()
        )
        if not attendee:
            raise HTTPException(status_code=404, detail="Attendee not found.")
        if attendee.check_in_status:
            return {"message": f"Attendee with ID {attendee_id} is already checked in."}

        # Mark as checked in
        attendee.check_in_status = True
        db.commit()
        db.refresh(attendee)

        return {"message": f"Attendee with ID {attendee_id} has been checked in."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking in attendee: {e}")


@router.post("/bulk-check-in", tags=["Attendees"])
async def bulk_check_in(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Handles bulk attendee check-ins via a CSV upload.
    The CSV must have a header row with 'email' as a column.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only CSV files are allowed."
        )

    try:
        # Read and decode the uploaded file
        content = await file.read()
        csv_data = StringIO(content.decode("utf-8"))
        csv_reader = csv.DictReader(csv_data)

        # Ensure 'email' column exists
        if "email" not in csv_reader.fieldnames:
            raise HTTPException(
                status_code=400, detail="CSV must contain an 'email' column."
            )

        # Process each row in the CSV
        check_in_count = 0
        for row in csv_reader:
            email = row.get("email")
            if not email:
                continue

            # Fetch the attendee by email
            attendee = db.query(Attendee).filter(Attendee.email == email).first()
            if attendee and not attendee.check_in_status:
                # Mark attendee as checked in
                attendee.check_in_status = True
                check_in_count += 1

        # Commit the changes to the database
        db.commit()

        return {"message": f"{check_in_count} attendees successfully checked in."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")
