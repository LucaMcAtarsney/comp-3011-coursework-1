from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

import crud
import models
import schemas
from database import SessionLocal, engine, get_db
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Combined endpoint for starting a run
@app.post("/runs/start", response_model=schemas.RunStartResponse)
def start_run(run_start: schemas.RunStart, db: Session = Depends(get_db)):
    # Get or create player
    player = crud.get_player_by_name(db, name=run_start.player_name)
    if not player:
        player_create = schemas.PlayerCreate(name=run_start.player_name)
        player = crud.create_player(db=db, player=player_create)
    
    # Create the run
    run_create = schemas.RunCreate(player_id=player.id, map_id=run_start.map_id)
    new_run = crud.create_run(db=db, run=run_create)
    
    return {"player_id": player.id, "run_id": new_run.id}


@app.get("/players", response_model=List[schemas.Player])
def get_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    players = crud.get_players(db, skip=skip, limit=limit)
    return players

@app.get("/runs", response_model=List[schemas.Run])
def get_runs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    runs = crud.get_runs(db, skip=skip, limit=limit)
    return runs

@app.post("/players", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = crud.get_player_by_name(db, name=player.name)
    if db_player:
        raise HTTPException(status_code=400, detail="Player name already registered")
    return crud.create_player(db=db, player=player)

@app.post("/runs", response_model=schemas.Run)
def create_run(run: schemas.RunCreate, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, player_id=run.player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    new_run = crud.create_run(db=db, run=run)
    return {"run_id": new_run.id, "started_at": new_run.started_at}


@app.post("/runs/{run_id}/update", response_model=schemas.Run)
def update_run_from_game(run_id: int, run_update: schemas.RunUpdate, db: Session = Depends(get_db)):
    db_run = crud.get_run(db, run_id=run_id)
    if not db_run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    # Here you would update the run with the new data
    # For example, you might add the new values to existing ones
    # This logic should be in your crud.py file
    updated_run = crud.update_run_stats(db=db, run_id=run_id, run_update=run_update)
    if not updated_run:
        raise HTTPException(status_code=404, detail="Run not found during update")
        
    return updated_run

@app.patch("/runs/{run_id}", response_model=schemas.Run)
def update_run(run_id: int, run_update: schemas.RunUpdate, db: Session = Depends(get_db)):
    db_run = crud.get_run(db, run_id=run_id)
    if not db_run:
        raise HTTPException(status_code=404, detail="Run not found")
    return crud.update_run(db=db, run_id=run_id, run_update=run_update)

@app.post("/runs/{run_id}/events", response_model=schemas.RunEvent)
def create_run_event(run_id: int, event: schemas.RunEventCreate, db: Session = Depends(get_db)):
    db_run = crud.get_run(db, run_id=run_id)
    if not db_run:
        raise HTTPException(status_code=404, detail="Run not found")
    return crud.create_run_event(db=db, run_id=run_id, event=event)

@app.get("/analytics/player/{player_id}/run-summary")
def get_player_run_summary(player_id: int, db: Session = Depends(get_db)):
    # This is a placeholder for a more complex analytics query
    runs = crud.get_runs_by_player(db, player_id=player_id)
    if not runs:
        return {"message": "No runs found for this player."}
    
    total_runs = len(runs)
    total_duration = sum(run.duration_seconds for run in runs)
    avg_duration = total_duration / total_runs if total_runs > 0 else 0
    best_duration = max(run.duration_seconds for run in runs) if runs else 0

    return {
        "total_runs": total_runs,
        "average_survival_time": avg_duration,
        "best_survival_time": best_duration,
        "recent_runs": [schemas.Run.from_orm(run) for run in runs[-5:]]
    }

@app.get("/analytics/player/{player_id}/death-causes")
def get_player_death_causes(player_id: int, db: Session = Depends(get_db)):
    runs = crud.get_runs_by_player(db, player_id=player_id)
    causes = {}
    for run in runs:
        if run.status == 'died' and run.cause_of_death:
            causes[run.cause_of_death] = causes.get(run.cause_of_death, 0) + 1
    return causes

@app.get("/analytics/player/{player_id}/survival-time-distribution")
def get_survival_time_distribution(player_id: int, db: Session = Depends(get_db)):
    runs = crud.get_runs_by_player(db, player_id=player_id)
    buckets = {
        "0-60s": 0,
        "60-120s": 0,
        "120-180s": 0,
        "180-240s": 0,
        "240-300s": 0,
        "300s+": 0,
    }
    for run in runs:
        duration = run.duration_seconds
        if duration <= 60:
            buckets["0-60s"] += 1
        elif duration <= 120:
            buckets["60-120s"] += 1
        elif duration <= 180:
            buckets["120-180s"] += 1
        elif duration <= 240:
            buckets["180-240s"] += 1
        elif duration <= 300:
            buckets["240-300s"] += 1
        else:
            buckets["300s+"] += 1
    return buckets

@app.get("/analytics/player/{player_id}/upgrade-effectiveness")
def get_upgrade_effectiveness(player_id: int, db: Session = Depends(get_db)):
    # This requires more complex logic, placeholder for now
    return {"message": "Upgrade effectiveness analytics not implemented yet."}


@app.get("/analytics/leaderboard", response_model=List[schemas.Run])
def get_leaderboard(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    leaderboard_runs = crud.get_leaderboard(db, skip=skip, limit=limit)
    return leaderboard_runs

@app.get("/analytics/players-summary", response_model=List[schemas.PlayerSummary])
def get_players_summary(db: Session = Depends(get_db), search: Optional[str] = None):
    return crud.get_players_summary(db, search=search)

@app.get("/analytics/view_player_stats/{player_id}", response_model=schemas.PlayerStats)
def view_player_stats(player_id: int, db: Session = Depends(get_db)):
    stats = crud.get_player_stats(db, player_id=player_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Player not found")
    return stats

@app.get("/players/{player_id}/runs", response_model=List[schemas.Run])
def get_player_runs(player_id: int, db: Session = Depends(get_db)):
    runs = crud.get_runs_by_player(db, player_id=player_id)
    return runs

@app.get("/runs/{run_id}", response_model=schemas.Run)
def get_run(run_id: int, db: Session = Depends(get_db)):
    db_run = crud.get_run(db, run_id=run_id)
    if not db_run:
        raise HTTPException(status_code=404, detail="Run not found")
    return db_run

@app.get("/runs/{run_id}/events", response_model=List[schemas.RunEvent])
def get_run_events(run_id: int, db: Session = Depends(get_db)):
    events = crud.get_run_events(db, run_id=run_id)
    return events

@app.delete("/runs/{run_id}")
def delete_run(run_id: int, db: Session = Depends(get_db)):
    db_run = crud.delete_run(db, run_id=run_id)
    if not db_run:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"message": "Run and associated events deleted successfully"}

@app.delete("/players/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    db_player = crud.delete_player(db, player_id=player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    return {"message": "Player and all associated data deleted successfully"}

@app.get("/test1")
def test_endpoint_one():
    return {"message": "TEST ENDPOINT ONE (PLAYER NAME) OK"}

@app.get("/test2")
def test_endpoint_two():
    return {"message": "TEST ENDPOINT TWO (UPDATE 30 SEC) OK"}

@app.get("/test3")
def test_endpoint_three():
    return {"message": "TEST ENDPOINT THREE (ENDGAME) OK"}
