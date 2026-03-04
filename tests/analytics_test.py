import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db

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
    # 1. Create a player and capture their password
    player_response = client.post("/players", json={"name": "stats_player"})
    player_data = player_response.json()
    player_id = player_data["id"]
    player_name = player_data["name"]
    password = player_data["password"]
    
    # Run 1 - Authenticate with password
    run1_payload = {"player_name": player_name, "password": password, "map_id": "map1", "create_new_player": False}
    run1 = client.post("/runs/start", json=run1_payload).json()
    client.post(f"/runs/{run1['run_id']}/update", json={"time_survived": 120, "monsters_slain": 50, "status": "completed"})

    # Run 2 - Authenticate with password
    run2_payload = {"player_name": player_name, "password": password, "map_id": "map2", "create_new_player": False}
    run2 = client.post("/runs/start", json=run2_payload).json()
    client.post(f"/runs/{run2['run_id']}/update", json={"time_survived": 240, "monsters_slain": 100, "status": "completed"})

    # 2. Fetch the player's stats
    stats_response = client.get(f"/analytics/view_player_stats/{player_id}")
    assert stats_response.status_code == 200
    stats_data = stats_response.json()

    # 3. Verify the stats
    assert stats_data["number_of_runs"] == 2
    assert stats_data["total_time_played"] == 360  # 120 + 240
    assert stats_data["average_time_survived"] == 180.0
    assert stats_data["longest_run"] == 240
    assert stats_data["total_monsters_slain"] == 150

def test_leaderboard():
    # 1. Create multiple players and runs with different scores
    p1_data = client.post("/players", json={"name": "leader_one"}).json()
    p1_name = p1_data['name']
    p1_password = p1_data['password']
    run1 = client.post("/runs/start", json={"player_name": p1_name, "password": p1_password, "map_id": "map1", "create_new_player": False}).json()
    client.post(f"/runs/{run1['run_id']}/update", json={"time_survived": 500, "status": "completed"})

    p2_data = client.post("/players", json={"name": "leader_two"}).json()
    p2_name = p2_data['name']
    p2_password = p2_data['password']
    run2 = client.post("/runs/start", json={"player_name": p2_name, "password": p2_password, "map_id": "map1", "create_new_player": False}).json()
    client.post(f"/runs/{run2['run_id']}/update", json={"time_survived": 1000, "status": "completed"})

    # 2. Fetch the leaderboard
    leaderboard_response = client.get("/analytics/leaderboard")
    assert leaderboard_response.status_code == 200
    leaderboard_data = leaderboard_response.json()
    
    # 3. Verify the order
    assert len(leaderboard_data) >= 2
    assert leaderboard_data[0]["player_id"] == p2_data["id"] # p2 had a longer duration
    assert leaderboard_data[1]["player_id"] == p1_data["id"]