# This file contains tests for the player-related endpoints of the API.
# It covers player creation, name generation, and handling of duplicate names.

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

# --- Player Tests ---

def test_create_player():
    """
    Tests the successful creation of a new player.
    It verifies that the response contains the correct data and a generated password.
    """
    response = client.post("/players", json={"name": "testplayer"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "testplayer"
    assert "id" in data
    assert "password" in data

def test_create_player_duplicate_name():
    """
    Tests that the API correctly handles an attempt to create a player
    with a name that is already in use. It should return a 409 Conflict status.
    """
    client.post("/players", json={"name": "testplayer"})  # Create the first player.
    response = client.post("/players", json={"name": "testplayer"})  # Attempt to create a duplicate.
    assert response.status_code == 409
    assert response.json()["detail"] == "Player name already registered"

def test_generate_name():
    """
    Tests the random name generation endpoint.
    It verifies that the endpoint returns a valid name.
    """
    response = client.get("/players/generate-name")
    assert response.status_code == 200
    data = response.json()
    assert "player_name" in data
    assert len(data["player_name"]) > 0