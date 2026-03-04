from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
import secrets
import string
from sqlalchemy.orm import Session
from typing import Optional

# Add these imports
import models 
import crud

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def generate_password(length: int = 12) -> str:
    """Generate a random password."""
    return "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_player(db: Session, name: str, password: str) -> Optional[models.Player]:
    """Authenticate a player by name and password."""
    player = crud.get_player_by_name(db, name=name)
    if not player:
        return None
    if not verify_password(password, player.hashed_password):
        return None
    return player

# --- Admin Authentication ---
admin_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid admin credentials",
    headers={"WWW-Authenticate": "Basic"},
)

def get_current_admin(credentials: HTTPBasicCredentials = Depends(HTTPBasic(realm="admin"))):
    """Dependency to protect admin-only endpoints."""
    # For simplicity, we'll hardcode the admin credentials.
    # In a real app, use environment variables and secrets management.
    correct_username = "admin"
    correct_password = "admin"
    
    is_user_correct = secrets.compare_digest(credentials.username, correct_username)
    is_pass_correct = secrets.compare_digest(credentials.password, correct_password)
    
    if not (is_user_correct and is_pass_correct):
        raise admin_credentials_exception
    
    return credentials.username