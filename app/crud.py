from sqlalchemy.orm import Session
from . import models, schemas

def create_building(db: Session, building: schemas.BuildingCreate):
    db_building = models.Building(**building.dict())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building

def get_buildings(db: Session):  
    return db.query(models.Building).all()

def create_session(db: Session, session: schemas.SessionCreate):
    db_session = models.Session(**session.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_sessions(db: Session): 
    return db.query(models.Session).all()

def create_attendance_event(db: Session, event: schemas.AttendanceEventCreate):  # Added event param; fixed body
    db_event = models.AttendanceEvent(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_attendance_events(db: Session): 
    return db.query(models.AttendanceEvent).all()

def get_events_for_session(db: Session, session_id: int):
    return (
        db.query(models.AttendanceEvent)
        .filter(models.AttendanceEvent.session_id == session_id)
        .order_by(models.AttendanceEvent.timestamp.asc())
        .all()
    )