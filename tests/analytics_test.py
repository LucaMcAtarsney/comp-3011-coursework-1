# This file contains tests for the analytics endpoints of the API.
# It verifies that the statistical calculations and leaderboard logic
# are working correctly.

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

# --- Analytics Tests ---

def test_get_player_stats():
    """
    Tests the player statistics endpoint by creating a player,
    simulating two runs, and then verifying that the calculated
    statistics are correct.
    """
    # 1. Create a player and capture their credentials.
    player_response = client.post("/players", json={"name": "stats_player"})
    player_data = player_response.json()
    player_id = player_data["id"]
    player_name = player_data["name"]
    password = player_data["password"]
    
    # 2. Simulate two runs for the player.
    # Run 1
    run1_payload = {"player_name": player_name, "password": password, "map_id": "map1"}
    run1 = client.post("/runs/start", json=run1_payload).json()
    client.patch(f"/runs/{run1['run_id']}", json={"duration_seconds": 120, "kills_total": 50, "status": "completed"})

    # Run 2
    run2_payload = {"player_name": player_name, "password": password, "map_id": "map2"}
    run2 = client.post("/runs/start", json=run2_payload).json()
    client.patch(f"/runs/{run2['run_id']}", json={"duration_seconds": 240, "kills_total": 100, "status": "completed"})

    # 3. Fetch the player's statistics.
    stats_response = client.get(f"/analytics/view_player_stats/{player_id}")
    assert stats_response.status_code == 200
    stats_data = stats_response.json()

    # 4. Verify that the calculated statistics are correct.
    assert stats_data["number_of_runs"] == 2
    assert stats_data["total_time_played"] == 360  # 120 + 240
    assert stats_data["average_time_survived"] == 180
    assert stats_data["longest_run"] == 240
    assert stats_data["total_monsters_slain"] == 150

def test_leaderboard():
    """
    Tests the leaderboard endpoint by creating two players with different
    run durations and verifying that the leaderboard is sorted correctly.
    """
    # 1. Create two players and simulate a run for each.
    # Player 1
    p1_data = client.post("/players", json={"name": "leader_one"}).json()
    p1_name = p1_data['name']
    p1_password = p1_data['password']
    run1 = client.post("/runs/start", json={"player_name": p1_name, "password": p1_password, "map_id": "map1"}).json()
    client.patch(f"/runs/{run1['run_id']}", json={"duration_seconds": 500, "status": "completed"})

    # Player 2 (with a longer run)
    p2_data = client.post("/players", json={"name": "leader_two"}).json()
    p2_name = p2_data['name']
    p2_password = p2_data['password']
    run2 = client.post("/runs/start", json={"player_name": p2_name, "password": p2_password, "map_id": "map1"}).json()
    client.patch(f"/runs/{run2['run_id']}", json={"duration_seconds": 1000, "status": "completed"})

    # 2. Fetch the leaderboard.
    leaderboard_response = client.get("/analytics/leaderboard")
    assert leaderboard_response.status_code == 200
    leaderboard_data = leaderboard_response.json()

    # 3. Verify that the leaderboard is sorted correctly (descending by duration).
    assert len(leaderboard_data) >= 2
    assert leaderboard_data[0]["player_id"] == p2_data["id"] # Player 2 should be first.
    assert leaderboard_data[1]["player_id"] == p1_data["id"] # Player 1 should be second.