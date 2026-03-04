from pydantic import BaseModel, ConfigDict
import datetime
from typing import Optional, List, Dict
from models import RunStatus
import string
import secrets

class PlayerBase(BaseModel):
    name: str

class PlayerCreate(PlayerBase):
    password: str # Make password required on creation

class Player(PlayerBase):
    id: int
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class PlayerCreateResponse(Player):
    # The user provides the password, so we don't need to send it back.
    pass

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

class RunEventBase(BaseModel):
    event_type: str
    value: Optional[str] = None

class RunEventCreate(RunEventBase):
    pass

class RunEvent(RunEventBase):
    id: int
    run_id: int
    timestamp: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class RunStart(BaseModel):
    player_name: str
    password: Optional[str] = None # Add password field
    map_id: str
    create_new_player: bool = False

class RunStartResponse(BaseModel):
    player_id: int
    run_id: int
    # Password is no longer sent in the response

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

def generate_random_password(length: int = 12) -> str:
    """Generate a secure random password."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))

def create_player(db: Session, player: schemas.PlayerCreate):
    hashed_password = get_password_hash(player.password)
    db_player = models.Player(name=player.name, hashed_password=hashed_password)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    # Return just the player object, not the plain password
    return db_player

def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.id == player_id).first()
