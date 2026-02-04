from sqlalchemy.orm import Session, joinedload
from typing import Optional
from . import models, schemas
import datetime

def create_player(db: Session, player: schemas.PlayerCreate):
    db_player = models.Player(name=player.name)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.id == player_id).first()

def get_player_by_name(db: Session, name: str):
    return db.query(models.Player).filter(models.Player.name == name).first()

def get_players(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Player).offset(skip).limit(limit).all()

def get_players_summary(db: Session, search: Optional[str] = None):
    query = db.query(models.Player).options(joinedload(models.Player.runs))
    
    if search:
        query = query.filter(models.Player.name.contains(search))
        
    players = query.all()
    
    summaries = []
    for player in players:
        total_runs = len(player.runs)
        best_run_time = 0
        if player.runs:
            best_run_time = max(run.duration_seconds for run in player.runs)
            
        summary = schemas.PlayerSummary(
            id=player.id,
            name=player.name,
            created_at=player.created_at,
            total_runs=total_runs,
            best_run_time=best_run_time
        )
        summaries.append(summary)
        
    return summaries

def create_run(db: Session, run: schemas.RunCreate):
    db_run = models.Run(player_id=run.player_id, map_id=run.map_id)
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run

def get_run(db: Session, run_id: int):
    return db.query(models.Run).filter(models.Run.id == run_id).first()

def get_runs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Run).offset(skip).limit(limit).all()

def get_leaderboard(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Run).order_by(models.Run.duration_seconds.desc()).offset(skip).limit(limit).all()

def get_runs_by_player(db: Session, player_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Run).filter(models.Run.player_id == player_id).offset(skip).limit(limit).all()

def update_run(db: Session, run_id: int, run_update: schemas.RunUpdate):
    db_run = get_run(db, run_id)
    if db_run:
        update_data = run_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_run, key, value)
        if 'status' in update_data and update_data['status'] in ['died', 'completed']:
            db_run.ended_at = datetime.datetime.utcnow()
        db.commit()
        db.refresh(db_run)
    return db_run

def update_run_stats(db: Session, run_id: int, run_update: schemas.RunUpdate):
    db_run = get_run(db, run_id)
    if db_run:
        if run_update.time_survived is not None:
            db_run.duration_seconds = run_update.time_survived
        if run_update.monsters_slain is not None:
            db_run.kills_total = run_update.monsters_slain
        if run_update.level is not None:
            db_run.level = run_update.level
        if run_update.xp is not None:
            db_run.xp = run_update.xp
        if run_update.status is not None:
            db_run.status = run_update.status
            if run_update.status in [models.RunStatus.completed, models.RunStatus.died]:
                db_run.ended_at = datetime.datetime.now()
        if run_update.cause_of_death is not None:
            db_run.cause_of_death = run_update.cause_of_death
        if run_update.upgrades is not None:
            db_run.upgrades = run_update.upgrades
        
        db.commit()
        db.refresh(db_run)
    return db_run

def delete_run(db: Session, run_id: int):
    db_run = get_run(db, run_id)
    if db_run:
        # also delete events associated with the run
        db.query(models.RunEvent).filter(models.RunEvent.run_id == run_id).delete()
        db.delete(db_run)
        db.commit()
    return db_run

def delete_player(db: Session, player_id: int):
    db_player = get_player(db, player_id)
    if db_player:
        # also delete runs and events associated with the player
        runs = db.query(models.Run).filter(models.Run.player_id == player_id).all()
        for run in runs:
            db.query(models.RunEvent).filter(models.RunEvent.run_id == run.id).delete()
            db.delete(run)
        db.delete(db_player)
        db.commit()
    return db_player


def create_run_event(db: Session, run_id: int, event: schemas.RunEventCreate):
    db_event = models.RunEvent(**event.dict(), run_id=run_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_run_events(db: Session, run_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.RunEvent).filter(models.RunEvent.run_id == run_id).offset(skip).limit(limit).all()