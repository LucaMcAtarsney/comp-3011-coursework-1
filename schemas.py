# This file defines the Pydantic models (schemas) that are used for
# data validation, serialization, and documentation in the API.
# These models ensure that the data flowing in and out of the API
# has a consistent and predictable structure.

from pydantic import BaseModel, ConfigDict
import datetime
from typing import Optional, List, Dict
from models import RunStatus

# --- Player Schemas ---

class PlayerBase(BaseModel):
    """Base schema for a player, containing the essential information."""
    name: str

class PlayerCreate(PlayerBase):
    """Schema for creating a new player. Currently, it's the same as the base."""
    pass

class PlayerNameUpdate(BaseModel):
    """Schema for updating a player's name."""
    name: str

class Player(PlayerBase):
    """Schema for representing a player, including their ID and creation date."""
    id: int
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class PlayerCreateResponse(Player):
    """
    Schema for the response when a new player is created.
    It includes the player's details and their generated password.
    """
    password: str

# --- Run Schemas ---

class RunBase(BaseModel):
    """Base schema for a run, linking it to a player and a map."""
    player_id: int
    map_id: str

class RunCreate(RunBase):
    """Schema for creating a new run."""
    pass

class RunUpdate(BaseModel):
    """
    Schema for updating a run's statistics. All fields are optional,
    allowing for partial updates.
    """
    duration_seconds: Optional[int] = None
    kills_total: Optional[int] = None
    level: Optional[int] = None
    xp: Optional[int] = None
    upgrades: Optional[Dict[str, int]] = None
    status: Optional[RunStatus] = None
    ended_at: Optional[datetime.datetime] = None
    cause_of_death: Optional[str] = None

class Run(RunBase):
    """Schema for representing a run, including all its details."""
    id: int
    player: Player
    started_at: datetime.datetime
    status: RunStatus
    duration_seconds: int
    level: int
    xp: int
    kills_total: int
    upgrades: Optional[Dict[str, int]] = None
    ended_at: Optional[datetime.datetime]
    cause_of_death: Optional[str]
    model_config = ConfigDict(from_attributes=True)

# --- Run Event Schemas ---

class RunEventBase(BaseModel):
    """Base schema for a run event."""
    event_type: str
    value: Optional[str] = None

class RunEventCreate(RunEventBase):
    """Schema for creating a new run event."""
    pass

class RunEvent(RunEventBase):
    """Schema for representing a run event, including its ID and timestamp."""
    id: int
    run_id: int
    timestamp: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

# --- Game Session Schemas ---

class RunStart(BaseModel):
    """
    Schema for starting a new game session. It can be used for both
    new and existing players.
    """
    player_name: str
    password: Optional[str] = None
    map_id: str
    create_new_player: bool = False

class RunStartResponse(BaseModel):
    """Schema for the response when a new game session is started."""
    player_id: int
    run_id: int

# --- Analytics Schemas ---

class PlayerSummary(Player):
    """
    Schema for a player summary, which includes their total number of runs
    and their best run time.
    """
    total_runs: int
    best_run_time: Optional[int] = 0

class PlayerStats(BaseModel):
    """Schema for detailed player statistics."""
    player_name: str
    number_of_runs: int
    total_time_played: int
    average_time_survived: float
    longest_run: int
    favourite_upgrade: Optional[str] = None
    total_monsters_slain: int

class RunLeaderboard(BaseModel):
    """Schema for a single entry in the leaderboard."""
    player_id: int
    run_id: int
    player_name: str
    duration_seconds: int
    total_kills: int
    model_config = ConfigDict(from_attributes=True)

# --- Name Validation Schemas ---

class NameCheckRequest(BaseModel):
    """Schema for a request to check if a player name is available."""
    player_name: str

class NameCheckResponse(BaseModel):
    """Schema for the response when checking a player name."""
    exists: bool
    message: str

class GenerateNameResponse(BaseModel):
    """Schema for the response when generating a random player name."""
    player_name: str
