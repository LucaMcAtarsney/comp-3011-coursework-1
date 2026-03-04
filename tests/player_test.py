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

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def setup_function():
    # Create tables before each test
    Base.metadata.create_all(bind=engine)

def teardown_function():
    # Drop tables after each test
    Base.metadata.drop_all(bind=engine)

def test_create_player():
    response = client.post("/players", json={"name": "testplayer"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "testplayer"
    assert "id" in data

def test_create_player_duplicate_name():
    client.post("/players", json={"name": "testplayer"}) # first player
    response = client.post("/players", json={"name": "testplayer"}) # second player
    assert response.status_code == 400
    assert response.json()["detail"] == "Player name already registered"

def test_generate_name():
    response = client.get("/players/generate-name")
    assert response.status_code == 200
    data = response.json()
    assert "player_name" in data
    assert len(data["player_name"]) > 0