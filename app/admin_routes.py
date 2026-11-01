from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import UploadFile, File
import csv
import io

from .database import SessionLocal
from . import crud, schemas

templates = Jinja2Templates(directory="templates")
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/buildings")
def buildings_page(request: Request, db: Session = Depends(get_db)):
    buildings = crud.get_buildings(db)
    return templates.TemplateResponse(
        "buildings.html",
        {"request": request, "buildings": buildings}
    )

@router.post("/buildings")
def add_building(
    name: str = Form(...),
    lat: float = Form(...),
    lng: float = Form(...),
    radius_m: int = Form(...),
    db: Session = Depends(get_db)
):
    crud.create_building(
        db,
        schemas.BuildingCreate(
            name=name,
            lat=lat,
            lng=lng,
            radius_m=radius_m
        )
    )
    return RedirectResponse("/buildings", status_code=303)

@router.get("/sessions")
def sessions_page(request: Request, db: Session = Depends(get_db)):
    sessions = crud.get_sessions(db)
    buildings = crud.get_buildings(db)
    return templates.TemplateResponse(
        "sessions.html",
        {
            "request": request,
            "sessions": sessions,
            "buildings": buildings
        }
    )


@router.post("/sessions")
def add_session(
    title: str = Form(...),
    start_time: str = Form(...),   
    end_time: str = Form(...),
    building_id: int = Form(...),
    db: Session = Depends(get_db)
):
    
    try:
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
    except ValueError:
       
        return RedirectResponse("/sessions", status_code=303)

    crud.create_session(
        db,
        schemas.SessionCreate(
            title=title,
            start_time=start_dt,
            end_time=end_dt,
            building_id=building_id
        )
    )
    return RedirectResponse("/sessions", status_code=303)

@router.post("/sessions/import")
async def import_sessions_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith(".csv"):
        return RedirectResponse("/sessions", status_code=303)

    contents = await file.read()
    decoded = contents.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))

    for row in reader:
        try:
            start_dt = datetime.fromisoformat(row["start_time"])
            end_dt = datetime.fromisoformat(row["end_time"])

            crud.create_session(
                db,
                schemas.SessionCreate(
                    title=row["title"].strip(),
                    start_time=start_dt,
                    end_time=end_dt,
                    building_id=int(row["building_id"]),
                ),
            )
        except Exception:
            # Skip bad rows silently (safe admin behavior)
            continue

    return RedirectResponse("/sessions", status_code=303)


@router.get("/events")
def events_page(request: Request, db: Session = Depends(get_db)):
    events = crud.get_attendance_events(db)  
    sessions = crud.get_sessions(db)
    return templates.TemplateResponse("events.html", {"request": request, "events": events, "sessions": sessions})

@router.post("/events")
def add_event(
    session_id: int = Form(...),
    type: str = Form(...),
    timestamp: str = Form(...), 
    reason: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        ts = datetime.fromisoformat(timestamp)
    except ValueError:
        return RedirectResponse("/events", status_code=303)
    crud.create_attendance_event(
        db,
        schemas.AttendanceEventCreate(
            session_id=session_id,
            type=type,
            timestamp=ts,
            reason=reason
        )
    )
    return RedirectResponse("/events", status_code=303)