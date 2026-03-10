# This file is the main entry point for the FastAPI application.
# It defines all the API endpoints and ties together the different
# components of the application, such as the database, CRUD operations,
# and authentication.

from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Optional

import crud
import models
import schemas
from database import SessionLocal, engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from auth import get_current_admin, verify_password
import auth

# Create all database tables based on the models
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI(
    title="Player and Run Tracker API",
    description="An API for tracking player data and game runs.",
    version="1.0.0"
)

# Configure Cross-Origin Resource Sharing (CORS) to allow requests
# from any origin. This is useful for development but should be
# configured more securely for production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- Player Name Endpoints ---

@app.post("/players/check-name", response_model=schemas.NameCheckResponse)
def check_name(request: schemas.NameCheckRequest, db: Session = Depends(get_db)):
    """
    Checks if a player name is already taken. This is useful for
    real-time validation in the user interface.
    """
    player_name = request.player_name.strip()
    
    if not player_name:
        return {"exists": False, "message": "Name cannot be empty"}
    
    player = crud.get_player_by_name(db, name=player_name)
    if player:
        return {"exists": True, "message": "This username is already taken."}
    else:
        return {"exists": False, "message": "This username is available."}

@app.get("/players/generate-name", response_model=schemas.GenerateNameResponse)
def generate_name(db: Session = Depends(get_db)):
    """
    Generates a unique, random player name that is not already in use.
    """
    new_name = crud.generate_available_player_name(db)
    return {"player_name": new_name}

# --- Game Session Endpoint ---

@app.post("/runs/start", response_model=schemas.RunStartResponse)
def start_run(run_input: schemas.RunStart, db: Session = Depends(get_db)):
    """
    Starts a new game run. This endpoint handles both new and existing players.
    If `create_new_player` is true, a new player is created. Otherwise,
    the existing player is authenticated.
    """
    if run_input.create_new_player:
        # Handle new player creation
        if crud.get_player_by_name(db, name=run_input.player_name):
            raise HTTPException(status_code=409, detail="Player name already registered")
        
        if not run_input.password:
            raise HTTPException(status_code=422, detail="Password is required for a new player")
            
        player = crud.create_player_with_password(db, player_name=run_input.player_name, plain_password=run_input.password)

    else:
        # Authenticate an existing player
        player = auth.authenticate_player(db, name=run_input.player_name, password=run_input.password)
        if not player:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
            )
    
    # Create a new run for the authenticated or newly created player
    run_create = schemas.RunCreate(player_id=player.id, map_id=run_input.map_id)
    db_run = crud.create_run(db=db, run=run_create)
    
    return schemas.RunStartResponse(player_id=player.id, run_id=db_run.id)

# --- Player CRUD Endpoints ---

@app.get("/players", response_model=List[schemas.Player])
def get_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of all players with pagination.
    """
    players = crud.get_players(db, skip=skip, limit=limit)
    return players

@app.get("/players/{player_id}", response_model=schemas.Player)
def read_player(player_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single player by their ID.
    """
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player

@app.post("/players", response_model=schemas.PlayerCreateResponse, status_code=201)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    """
    Creates a new player with a randomly generated password.
    Returns the new player's details, including the password.
    """
    db_player_check = crud.get_player_by_name(db, name=player.name)
    if db_player_check:
        raise HTTPException(status_code=409, detail="Player name already registered")
    
    return crud.create_player(db=db, player=player)

@app.delete("/players/{player_id}", status_code=204)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    """
    Deletes a player and all of their associated data.
    """
    db_player = crud.delete_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return Response(status_code=204)

# --- Run CRUD Endpoints ---

@app.get("/runs", response_model=List[schemas.Run])
def get_runs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of all runs with pagination.
    """
    runs = crud.get_runs(db, skip=skip, limit=limit)
    return runs

@app.get("/runs/{run_id}", response_model=schemas.Run)
def get_run(run_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single run by its ID.
    """
    db_run = crud.get_run(db, run_id=run_id)
    if not db_run:
        raise HTTPException(status_code=404, detail="Run not found")
    return db_run

@app.patch("/runs/{run_id}", response_model=schemas.Run)
def update_run(run_id: int, run_update: schemas.RunUpdate, db: Session = Depends(get_db)):
    """
    Updates the details of a specific run, such as duration, kills, and status.
    This is the primary endpoint for updating a run's progress.
    """
    db_run = crud.get_run(db, run_id=run_id)
    if not db_run:
        raise HTTPException(status_code=404, detail="Run not found")
    return crud.update_run(db=db, run_id=run_id, run_update=run_update)

@app.delete("/runs/{run_id}")
def delete_run(run_id: int, db: Session = Depends(get_db)):
    """
    Deletes a single run and its associated events.
    """
    db_run = crud.delete_run(db, run_id=run_id)
    if not db_run:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"message": "Run and associated events deleted successfully"}

# --- Run Event Endpoints ---

@app.post("/runs/{run_id}/events", response_model=schemas.RunEvent)
def create_run_event(run_id: int, event: schemas.RunEventCreate, db: Session = Depends(get_db)):
    """
    Creates a new event associated with a specific run.
    """
    db_run = crud.get_run(db, run_id=run_id)
    if not db_run:
        raise HTTPException(status_code=404, detail="Run not found")
    return crud.create_run_event(db=db, run_id=run_id, event=event)

@app.get("/runs/{run_id}/events", response_model=List[schemas.RunEvent])
def get_run_events(run_id: int, db: Session = Depends(get_db)):
    """
    Retrieves all events for a specific run.
    """
    events = crud.get_run_events(db, run_id=run_id)
    return events

# --- Analytics Endpoints ---

@app.get("/analytics/leaderboard", response_model=List[schemas.RunLeaderboard])
def get_leaderboard(db: Session = Depends(get_db)):
    """
    Retrieves the top 10 runs for the leaderboard, sorted by duration.
    """
    return crud.get_leaderboard(db)

@app.get("/analytics/players-summary", response_model=List[schemas.PlayerSummary])
def get_players_summary(db: Session = Depends(get_db), search: Optional[str] = None):
    """
    Provides a summary of all players, including their total number of runs
    and best run time. Can be filtered by a search term.
    """
    return crud.get_players_summary(db, search=search)

@app.get("/analytics/view_player_stats/{player_id}", response_model=schemas.PlayerStats)
def view_player_stats(player_id: int, db: Session = Depends(get_db)):
    """
    Retrieves detailed statistics for a single player, such as total runs,
    average survival time, and total kills.
    """
    stats = crud.get_player_stats(db, player_id=player_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Player not found or has no runs")
    return stats

@app.get("/players/{player_id}/runs", response_model=List[schemas.Run])
def get_player_runs(player_id: int, db: Session = Depends(get_db)):
    """
    Retrieves all runs for a specific player.
    """
    runs = crud.get_runs_by_player(db, player_id=player_id)
    return runs

# --- Admin Endpoints ---

@app.get("/admin/login", status_code=200)
def admin_login(admin_user: str = Depends(get_current_admin)):
    """
    Verifies admin credentials. This endpoint is protected and requires
    Basic Authentication.
    """
    return {"message": "Admin authentication successful"}

@app.patch("/admin/players/{player_id}", response_model=schemas.Player)
def admin_update_player_name(
    player_id: int, 
    update_data: schemas.PlayerNameUpdate,
    db: Session = Depends(get_db), 
    admin_user: str = Depends(get_current_admin)
):
    """
    Admin-only endpoint to update a player's name.
    """
    db_player = crud.update_player_name(db, player_id=player_id, new_name=update_data.name)
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player

@app.delete("/admin/runs/{run_id}", status_code=204)
def admin_delete_run(
    run_id: int, 
    db: Session = Depends(get_db), 
    admin_user: str = Depends(get_current_admin)
):
    """
    Admin-only endpoint to delete a specific run.
    """
    db_run = crud.delete_run(db, run_id=run_id)
    if not db_run:
        raise HTTPException(status_code=404, detail="Run not found")
    return Response(status_code=204)

@app.delete("/admin/players/{player_id}", status_code=204)
def admin_delete_player(
    player_id: int, 
    db: Session = Depends(get_db), 
    admin_user: str = Depends(get_current_admin)
):
    """
    Admin-only endpoint to delete a player and all their associated runs.
    """
    db_player = crud.delete_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return Response(status_code=204)

# --- Deprecated / Unused Endpoints ---
# These endpoints are left for reference but are either replaced by more
# comprehensive endpoints or are no longer in use.

@app.post("/runs/{run_id}/update", response_model=schemas.Run)
def update_run_from_game(run_id: int, run_update: schemas.RunUpdate, db: Session = Depends(get_db)):
    db_run = crud.get_run(db, run_id=run_id)
    if not db_run:
        raise HTTPException(status_code=404, detail="Run not found")
    return crud.update_run(db=db, run_id=run_id, run_update=run_update)
    
#     updated_run = crud.update_run_stats(db=db, run_id=run_id, run_update=run_update)
#     if not updated_run:
#         raise HTTPException(status_code=404, detail="Run not found during update")
        
#     return updated_run

# @app.get("/analytics/player/{player_id}/run-summary")
# def get_player_run_summary(player_id: int, db: Session = Depends(get_db)):
#     ...

# @app.get("/analytics/player/{player_id}/death-causes")
# def get_player_death_causes(player_id: int, db: Session = Depends(get_db)):
#     ...

# @app.get("/analytics/player/{player_id}/survival-time-distribution")
# def get_survival_time_distribution(player_id: int, db: Session = Depends(get_db)):
#     ...

# @app.get("/analytics/player/{player_id}/upgrade-effectiveness")
# def get_upgrade_effectiveness(player_id: int, db: Session = Depends(get_db)):
#     ...

# --- Test Endpoints ---
# These are simple endpoints used for basic connectivity testing.

@app.get("/test1")
def test_endpoint_one():
    return {"message": "TEST ENDPOINT ONE (PLAYER NAME) OK"}

@app.get("/test2")
def test_endpoint_two():
    return {"message": "TEST ENDPOINT TWO (UPDATE 30 SEC) OK"}

@app.get("/test3")
def test_endpoint_three():
    return {"message": "TEST ENDPOINT THREE (ENDGAME) OK"}
