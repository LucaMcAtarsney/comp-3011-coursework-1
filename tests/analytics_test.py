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

def test_get_player_stats():
    # 1. Create a player and a few runs for them
    player_response = client.post("/players", json={"name": "stats_player"})
    player_id = player_response.json()["id"]
    player_name = player_response.json()["name"]
    
    # Run 1
    run1 = client.post("/runs/start", json={"player_name": player_name, "map_id": "map1"}).json()
    client.post(f"/runs/{run1['run_id']}/update", json={"time_survived": 120, "monsters_slain": 50, "status": "completed"})

    # Run 2
    run2 = client.post("/runs/start", json={"player_name": player_name, "map_id": "map2"}).json()
    client.post(f"/runs/{run2['run_id']}/update", json={"time_survived": 240, "monsters_slain": 100, "status": "completed"})

    # 2. Fetch the player's stats
    stats_response = client.get(f"/analytics/view_player_stats/{player_id}")
    assert stats_response.status_code == 200
    stats_data = stats_response.json()

    # 3. Assert the calculations are correct
    assert stats_data["number_of_runs"] == 2
    assert stats_data["total_time_played"] == 360  # 120 + 240
    assert stats_data["average_time_survived"] == 180.0
    assert stats_data["longest_run"] == 240
    assert stats_data["total_monsters_slain"] == 150

def test_leaderboard():
    # 1. Create multiple players and runs with different scores
    p1_name = client.post("/players", json={"name": "leader_one"}).json()['name']
    run1 = client.post("/runs/start", json={"player_name": p1_name, "map_id": "map1"}).json()
    client.post(f"/runs/{run1['run_id']}/update", json={"time_survived": 500, "status": "completed"})

    p2_name = client.post("/players", json={"name": "leader_two"}).json()['name']
    run2 = client.post("/runs/start", json={"player_name": p2_name, "map_id": "map1"}).json()
    client.post(f"/runs/{run2['run_id']}/update", json={"time_survived": 1000, "status": "completed"})

    # 2. Fetch the leaderboard
    leaderboard_response = client.get("/analytics/leaderboard")
    assert leaderboard_response.status_code == 200
    leaderboard = leaderboard_response.json()

    # 3. Assert the order is correct
    assert len(leaderboard) == 2
    assert leaderboard[0]["player"]["name"] == "leader_two" # Player 2 should be first
    assert leaderboard[0]["duration_seconds"] == 1000
    assert leaderboard[1]["player"]["name"] == "leader_one"
    assert leaderboard[1]["duration_seconds"] == 500