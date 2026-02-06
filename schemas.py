from pydantic import BaseModel
import datetime
from typing import Optional, List, Dict
from models import RunStatus

class PlayerBase(BaseModel):
    name: str

class PlayerCreate(PlayerBase):
    pass

    class Config:
        from_attributes = True

class Player(PlayerBase):
    id: int
    created_at: datetime.datetime

class RunBase(BaseModel):
    player_id: int
    map_id: str

class RunCreate(RunBase):
    pass

class RunUpdate(BaseModel):
    time_survived: Optional[int] = None
    monsters_slain: Optional[int] = None
    level: Optional[int] = None
    xp: Optional[int] = None
    upgrades: Optional[Dict[str, int]] = None
    status: Optional[RunStatus] = None
    ended_at: Optional[datetime.datetime] = None
    cause_of_death: Optional[str] = None

class Run(RunBase):
    id: int
    player: Player  # Include the full Player object
    started_at: datetime.datetime
    status: RunStatus
    duration_seconds: int
    level: int
    xp: int
    kills_total: int
    upgrades: Optional[Dict[str, int]] = None
    ended_at: Optional[datetime.datetime]
    cause_of_death: Optional[str]

    class Config:
        from_attributes = True

class RunEventBase(BaseModel):
    event_type: str
    value: Optional[str] = None

class RunEventCreate(RunEventBase):
    pass

class RunEvent(RunEventBase):
    id: int
    run_id: int
    timestamp: datetime.datetime

    class Config:
        from_attributes = True

class RunStart(BaseModel):
    player_name: str
    map_id: str
    create_new_player: bool = False  # Allow creating new player with provided name

class RunStartResponse(BaseModel):
    player_id: int
    run_id: int

class PlayerSummary(Player):
    total_runs: int
    best_run_time: Optional[int] = 0

class PlayerStats(BaseModel):
    player_name: str
    number_of_runs: int
    total_time_played: int
    average_time_survived: float
    longest_run: int
    favourite_upgrade: Optional[str] = None
    total_monsters_slain: int

class NameCheckRequest(BaseModel):
    player_name: str

class NameCheckResponse(BaseModel):
    exists: bool
    message: str

class GenerateNameResponse(BaseModel):
    player_name: str
