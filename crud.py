# This file contains the core CRUD (Create, Read, Update, Delete)
# operations for interacting with the database. It acts as a bridge
# between the API endpoints and the database models.

from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from collections import Counter
import datetime
from datetime import timezone

import models
import schemas
import name_pool
import secrets
import string
from auth import get_password_hash

def generate_random_password(length: int = 12) -> str:
    """
    Generates a cryptographically secure random password.
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))

# --- Player Operations ---

def create_player(db: Session, player: schemas.PlayerCreate):
    """
    Creates a new player with a randomly generated password.
    The password is then hashed before being stored.
    """
    plain_password = generate_random_password()
    hashed_password = get_password_hash(plain_password)
    
    db_player = models.Player(name=player.name, hashed_password=hashed_password)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    
    # Return a response object that includes the plain-text password
    return schemas.PlayerCreateResponse(
        id=db_player.id,
        name=db_player.name,
        created_at=db_player.created_at,
        password=plain_password
    )

def create_player_with_password(db: Session, player_name: str, plain_password: str):
    """
    Creates a new player with a user-provided password.
    The password is hashed before being stored.
    """
    hashed_password = get_password_hash(plain_password)
    
    db_player = models.Player(name=player_name, hashed_password=hashed_password)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    
    return db_player

def get_player(db: Session, player_id: int):
    """
    Retrieves a single player by their unique ID.
    """
    return db.query(models.Player).filter(models.Player.id == player_id).first()

def get_player_by_name(db: Session, name: str):
    """
    Retrieves a single player by their unique name.
    """
    return db.query(models.Player).filter(models.Player.name == name).first()

def update_player_name(db: Session, player_id: int, new_name: str):
    """
    Updates a player's name.
    """
    db_player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if db_player:
        db_player.name = new_name
        db.commit()
        db.refresh(db_player)
        return db_player
    return None

def delete_player(db: Session, player_id: int):
    """
    Deletes a player and all of their associated runs and run events.
    This ensures that no orphaned data is left in the database.
    """
    db_player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if db_player:
        # Cascade delete to runs and their events
        db.query(models.Run).filter(models.Run.player_id == player_id).delete()
        db.delete(db_player)
        db.commit()
        return db_player
    return None

# --- Name Generation and Validation ---

def check_player_name(db: Session, player_name: str):
    """
    Checks if a player name already exists in the database.
    """
    player = get_player_by_name(db, name=player_name)
    if player:
        return {"exists": True, "message": "This username is already taken."}
    else:
        return {"exists": False, "message": "This username is available."}

def get_all_player_names(db: Session) -> list[str]:
    """
    Returns a list of all player names currently in the database.
    """
    return [name for name, in db.query(models.Player.name).all()]

def generate_available_player_name(db: Session) -> str:
    """
    Generates a unique random name that is not already in use.
    """
    existing_names = get_all_player_names(db)
    return name_pool.generate_unique_name(existing_names)

# --- Analytics and Summaries ---

def get_players_summary(db: Session, search: Optional[str] = None):
    """
    Retrieves a summary for each player, including their total number of runs
    and their best run time. Can be filtered by a search term.
    """
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

def get_player_stats(db: Session, player_id: int):
    """
    Calculates and retrieves detailed statistics for a single player,
    including total runs, time played, average survival time, longest run,
    total kills, and their most frequently chosen upgrade.
    """
    player = db.query(models.Player).options(joinedload(models.Player.runs)).filter(models.Player.id == player_id).first()
    if not player:
        return None

    runs = player.runs
    total_runs = len(runs)
    if total_runs == 0:
        # Return a default stats object if the player has no runs
        return schemas.PlayerStats(
            player_name=player.name,
            number_of_runs=0,
            total_time_played=0,
            average_time_survived=0.0,
            longest_run=0,
            total_monsters_slain=0,
            favourite_upgrade=None
        )

    total_time_played = sum(run.duration_seconds for run in runs)
    average_time_survived = total_time_played / total_runs
    longest_run = max(run.duration_seconds for run in runs)
    total_monsters_slain = sum(run.kills_total for run in runs)

    # Determine the player's favorite upgrade by counting all upgrades across all runs
    all_upgrades = []
    for run in runs:
        if run.upgrades:
            for upgrade, level in run.upgrades.items():
                all_upgrades.extend([upgrade] * level)
    
    favourite_upgrade = None
    if all_upgrades:
        favourite_upgrade = Counter(all_upgrades).most_common(1)[0][0]

    return schemas.PlayerStats(
        player_name=player.name,
        number_of_runs=total_runs,
        total_time_played=total_time_played,
        average_time_survived=average_time_survived,
        longest_run=longest_run,
        total_monsters_slain=total_monsters_slain,
        favourite_upgrade=favourite_upgrade
    )

def get_leaderboard(db: Session, skip: int = 0, limit: int = 10) -> List[schemas.RunLeaderboard]:
    """
    Retrieves the top runs for the leaderboard, sorted by duration in
    descending order.
    """
    runs = db.query(models.Run).order_by(models.Run.duration_seconds.desc()).offset(skip).limit(limit).all()
    
    leaderboard_entries = []
    for run in runs:
        leaderboard_entries.append(schemas.RunLeaderboard(
            player_id=run.player.id,
            run_id=run.id,
            player_name=run.player.name,
            duration_seconds=run.duration_seconds,
            total_kills=run.kills_total
        ))
    return leaderboard_entries

# --- Run Operations ---

def create_run(db: Session, run: schemas.RunCreate):
    """
    Creates a new run for a given player.
    """
    db_run = models.Run(player_id=run.player_id, map_id=run.map_id)
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run

def get_run(db: Session, run_id: int):
    """
    Retrieves a single run by its unique ID.
    """
    return db.query(models.Run).filter(models.Run.id == run_id).first()

def get_runs(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieves a list of all runs with pagination.
    """
    return db.query(models.Run).offset(skip).limit(limit).all()

def get_runs_by_player(db: Session, player_id: int, skip: int = 0, limit: int = 100):
    """
    Retrieves all runs for a specific player with pagination.
    """
    return db.query(models.Run).filter(models.Run.player_id == player_id).offset(skip).limit(limit).all()

def update_run(db: Session, run_id: int, run_update: schemas.RunUpdate):
    """
    Updates a run's details. This function is used to update the run's
    progress, such as duration, kills, and status.
    """
    db_run = get_run(db, run_id)
    if db_run:
        update_data = run_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_run, key, value)
        if 'status' in update_data and update_data['status'] in ['died', 'completed']:
            db_run.ended_at = datetime.datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_run)
    return db_run

def delete_run(db: Session, run_id: int):
    """
    Deletes a single run and all of its associated events.
    """
    db_run = get_run(db, run_id)
    if db_run:
        # Cascade delete to associated run events
        db.query(models.RunEvent).filter(models.RunEvent.run_id == run_id).delete()
        db.delete(db_run)
        db.commit()
    return db_run

# --- Deprecated Functions ---
# The function below is deprecated and will be removed in a future version.
# `update_run` should be used instead.

def update_run_stats(db: Session, run_id: int, run_update: schemas.RunUpdate):
    """
    DEPRECATED: This function is no longer in use.
    Updates the statistics of a run.
    """
    db_run = get_run(db, run_id)
    if db_run:
        if run_update.duration_seconds is not None:
            db_run.duration_seconds = run_update.duration_seconds
        if run_update.kills_total is not None:
            db_run.kills_total = run_update.kills_total
        if run_update.level is not None:
            db_run.level = run_update.level
        if run_update.xp is not None:
            db_run.xp = run_update.xp
        if run_update.status is not None:
            db_run.status = run_update.status
            if run_update.status in [models.RunStatus.completed, models.RunStatus.died]:
                db_run.ended_at = datetime.datetime.now(datetime.timezone.utc)
        if run_update.cause_of_death is not None:
            db_run.cause_of_death = run_update.cause_of_death
        if run_update.upgrades is not None:
            db_run.upgrades = run_update.upgrades
        
        db.commit()
        db.refresh(db_run)
    return db_run