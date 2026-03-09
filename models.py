# This file defines the SQLAlchemy models, which represent the database
# tables as Python objects. These models are the foundation of the
# application's data structure.

import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from database import Base
import enum

class Player(Base):
    """
    Represents a player in the database. Each player has a unique name
    and a hashed password for authentication.
    """
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)

    # Establishes a one-to-many relationship with the Run model.
    runs = relationship("Run", back_populates="player", cascade="all, delete-orphan")

class RunStatus(str, enum.Enum):
    """
    An enumeration for the possible statuses of a run.
    """
    in_progress = "in_progress"
    died = "died"
    completed = "completed"

class Run(Base):
    """
    Represents a single game run. Each run is associated with a player
    and contains statistics about the run, such as duration and kills.
    """
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
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

    # Establishes a many-to-one relationship with the Player model.
    player = relationship("Player", back_populates="runs")
    # Establishes a one-to-many relationship with the RunEvent model.
    events = relationship("RunEvent", back_populates="run", cascade="all, delete-orphan")

class RunEvent(Base):
    """
    Represents an event that occurred during a run, such as picking up
    an item or defeating a boss.
    """
    __tablename__ = "run_events"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("runs.id"), nullable=False)
    event_type = Column(String)
    value = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.now)

    # Establishes a many-to-one relationship with the Run model.
    run = relationship("Run", back_populates="events")
