from sqlalchemy.orm import Session
from . import models, schemas
import datetime

def create_player(db: Session, player: schemas.PlayerCreate):
    pass
def get_player(db: Session, player_id: int):
    pass

def get_player_by_name(db: Session, name: str):
    pass

def get_players(db: Session, skip: int = 0, limit: int = 100):
    pass

def create_run(db: Session, run: schemas.RunCreate):
    pass

def get_run(db: Session, run_id: int):
    pass

def get_runs(db: Session, skip: int = 0, limit: int = 100):
    pass

def get_leaderboard(db: Session, skip: int = 0, limit: int = 10):
    pass

def get_runs_by_player(db: Session, player_id: int, skip: int = 0, limit: int = 100):
    pass

def update_run(db: Session, run_id: int, run_update: schemas.RunUpdate):
    pass

def update_run_stats(db: Session, run_id: int, run_update: schemas.RunUpdate):
    pass

def delete_run(db: Session, run_id: int):
    pass

def delete_player(db: Session, player_id: int):
    pass
