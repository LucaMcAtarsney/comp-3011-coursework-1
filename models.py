import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from database import Base
import enum

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now)

    runs = relationship("Run", back_populates="player")

class RunStatus(str, enum.Enum):
    in_progress = "in_progress"
    died = "died"
    completed = "completed"

class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    map_id = Column(String)
    started_at = Column(DateTime, default=datetime.datetime.now)
    status = Column(Enum(RunStatus), default=RunStatus.in_progress)
    duration_seconds = Column(Integer, default=0)
    level = Column(Integer, default=0)
    xp = Column(Integer, default=0)
    kills_total = Column(Integer, default=0)
    upgrades = Column(JSON, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    cause_of_death = Column(String, nullable=True)

    player = relationship("Player", back_populates="runs")
    events = relationship("RunEvent", back_populates="run")

class RunEvent(Base):
    __tablename__ = "run_events"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"))
    event_type = Column(String)
    value = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.now)

    run = relationship("Run", back_populates="events")
