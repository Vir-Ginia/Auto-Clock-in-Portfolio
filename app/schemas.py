from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EventType(str, Enum):
    CLOCK_IN = "CLOCK_IN"
    CLOCK_OUT = "CLOCK_OUT"
    GRACE_START = "GRACE_START"
    GRACE_CANCEL = "GRACE_CANCEL"

    
class BuildingBase(BaseModel):
    name: str
    lat: float
    lng: float
    radius_m: int

class BuildingCreate(BuildingBase):
    pass

class BuildingOut(BuildingBase):
    id: int

    class Config:
        orm_mode = True


class SessionBase(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime
    building_id: int

class SessionCreate(SessionBase):
    pass

class SessionOut(SessionBase):
    id: int

    class Config:
        orm_mode = True


class AttendanceEventBase(BaseModel):
    session_id: int
    type: EventType
    timestamp: datetime
    reason: str


class AttendanceEventCreate(AttendanceEventBase):
    pass


class AttendanceEventOut(AttendanceEventBase):
    id: int

    class Config:
        orm_mode = True

class AttendanceEventOut(BaseModel):
    id: int
    session_id: int
    type: str
    timestamp: datetime
    reason: str

    class Config:
        orm_mode = True