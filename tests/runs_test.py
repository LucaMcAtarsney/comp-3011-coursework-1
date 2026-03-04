import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_function():
    # Create tables before each test
    Base.metadata.create_all(bind=engine)

def teardown_function():
    # Drop tables after each test
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_start_run():
    # 1. Create a player first
    player_response = client.post("/players", json={"name": "run_tester"})
    assert player_response.status_code == 200
    player_name = player_response.json()["name"]

    # 2. Start a run for that player
    run_response = client.post(
        "/runs/start",
        json={"player_name": player_name, "map_id": "map1"}
    )
    assert run_response.status_code == 200
    run_data = run_response.json()
    assert "run_id" in run_data

def test_update_run():
    # 1. Start a run (as above)
    player_response = client.post("/players", json={"name": "run_updater"})
    player_name = player_response.json()["name"]
    run_response = client.post("/runs/start", json={"player_name": player_name, "map_id": "map1"})
    run_id = run_response.json()["run_id"]

    # 2. Update the run with new stats
    update_response = client.post(
        f"/runs/{run_id}/update",
        json={"level": 5, "monsters_slain": 100}
    )
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["level"] == 5
    assert updated_data["kills_total"] == 100

def test_end_run():
    # 1. Start a run
    player_response = client.post("/players", json={"name": "run_ender"})
    player_name = player_response.json()["name"]
    run_response = client.post("/runs/start", json={"player_name": player_name, "map_id": "map1"})
    run_id = run_response.json()["run_id"]

    # 2. End the run
    end_response = client.post(
        f"/runs/{run_id}/update",
        json={"status": "completed", "cause_of_death": "Fell off a cliff"}
    )
    assert end_response.status_code == 200
    ended_data = end_response.json()
    assert ended_data["status"] == "completed"
    assert ended_data["cause_of_death"] == "Fell off a cliff"
    assert ended_data["ended_at"] is not None

def test_get_run_not_found():
    response = client.get("/runs/9999") # A run ID that doesn't exist
    assert response.status_code == 404