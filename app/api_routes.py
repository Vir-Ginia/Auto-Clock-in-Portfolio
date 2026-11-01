from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import crud, schemas, models
from .database import SessionLocal
from . import crud, schemas
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/buildings", response_model=list[schemas.BuildingOut])
def read_buildings(db: Session = Depends(get_db)):
    return crud.get_buildings(db)

@router.get("/sessions", response_model=list[schemas.SessionOut])
def read_sessions(db: Session = Depends(get_db)):
    return crud.get_sessions(db)


class AttendanceEventCreate(BaseModel):
    session_id: int
    type: str  # e.g., "CLOCK_IN"
    timestamp: datetime
    reason: str

@router.get("/sync/buildings")
def sync_buildings(db: Session = Depends(get_db)):
    return crud.get_buildings(db)  # Already have this

@router.get("/sync/sessions")
def sync_sessions(from_date: str = None, to_date: str = None, db: Session = Depends(get_db)):
    # Parse dates if provided
    query = db.query(models.Session)
    if from_date:
        query = query.filter(models.Session.start_time >= datetime.fromisoformat(from_date))
    if to_date:
        query = query.filter(models.Session.end_time <= datetime.fromisoformat(to_date))
    return query.all()

@router.post("/attendance-events")
def create_attendance_events(events: list[AttendanceEventCreate], db: Session = Depends(get_db)):
    for event in events:
        crud.create_attendance_event(db, event)  # Implement this in crud.py similar to create_session
    return {"status": "synced", "count": len(events)}

@router.get(
    "/sessions/{session_id}/events",
    response_model=list[schemas.AttendanceEventOut]
)
def get_events_for_session(
    
    session_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_events_for_session(db, session_id)