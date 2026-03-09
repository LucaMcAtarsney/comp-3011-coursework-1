# This file contains tests for the run-related endpoints of the API.
# It covers starting, updating, and ending a run, as well as handling
# cases where a run is not found.

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db

# --- Test Database Setup ---

# Use an in-memory SQLite database for testing to ensure isolation.
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_function():
    """
    Create all database tables before each test function is executed.
    """
    Base.metadata.create_all(bind=engine)

def teardown_function():
    """
    Drop all database tables after each test function has executed.
    This ensures a clean state for every test.
    """
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    """
    A dependency override that provides a test database session to the
    API endpoints during testing.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Apply the dependency override to the FastAPI app.
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# --- Run Tests ---

def test_start_run():
    """
    Tests the successful start of a new run for an existing player.
    """
    # 1. Create a player to get their credentials.
    player_response = client.post("/players", json={"name": "run_tester"})
    assert player_response.status_code == 201
    player_data = player_response.json()
    player_name = player_data["name"]
    password = player_data["password"]

    # 2. Start a new run for the player using their credentials.
    run_response = client.post(
        "/runs/start",
        json={"player_name": player_name, "password": password, "map_id": "map1"}
    )
    assert run_response.status_code == 200
    run_data = run_response.json()
    assert "run_id" in run_data

def test_update_run():
    """
    Tests updating a run with new statistics, such as level and kills.
    Note: This test uses a deprecated endpoint (`/runs/{run_id}/update`).
    The current endpoint is `PATCH /runs/{run_id}`.
    """
    # 1. Create a player and start a run.
    player_response = client.post("/players", json={"name": "run_updater"})
    player_data = player_response.json()
    player_name = player_data["name"]
    password = player_data["password"]
    run_response = client.post("/runs/start", json={"player_name": player_name, "password": password, "map_id": "map1"})
    run_id = run_response.json()["run_id"]

    # 2. Update the run with new statistics.
    update_response = client.patch(
        f"/runs/{run_id}",
        json={"level": 5, "kills_total": 100}
    )
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["level"] == 5
    assert updated_data["kills_total"] == 100

def test_end_run():
    """
    Tests ending a run by updating its status to 'completed'.
    It verifies that the run's status and cause of death are updated,
    and that an end timestamp is set.
    Note: This test also uses the deprecated endpoint.
    """
    # 1. Create a player and start a run.
    player_response = client.post("/players", json={"name": "run_ender"})
    player_data = player_response.json()
    player_name = player_data["name"]
    password = player_data["password"]
    run_response = client.post("/runs/start", json={"player_name": player_name, "password": password, "map_id": "map1"})
    run_id = run_response.json()["run_id"]

    # 2. End the run by updating its status.
    end_response = client.patch(
        f"/runs/{run_id}",
        json={"status": "completed", "cause_of_death": "Fell off a cliff"}
    )
    assert end_response.status_code == 200
    ended_data = end_response.json()
    assert ended_data["status"] == "completed"
    assert ended_data["cause_of_death"] == "Fell off a cliff"
    assert ended_data["ended_at"] is not None

def test_get_run_not_found():
    """
    Tests that the API correctly handles a request for a run that
    does not exist. It should return a 404 Not Found status.
    """
    response = client.get("/runs/9999")  # A run ID that is unlikely to exist.
    assert response.status_code == 404