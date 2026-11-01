from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Building(Base):
    __tablename__ = "buildings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    radius_m = Column(Integer, nullable=False)

    sessions = relationship("Session", back_populates="building")


class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    events = relationship("AttendanceEvent", back_populates="session")
    building_id = Column(Integer, ForeignKey("buildings.id"))
    building = relationship("Building", back_populates="sessions")

class AttendanceEvent(Base):
    __tablename__ = "attendance_events"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    type = Column(String, nullable=False)  # CLOCK_IN, etc.
    timestamp = Column(DateTime, nullable=False)
    reason = Column(String, nullable=False)
    session = relationship("Session", back_populates="events")