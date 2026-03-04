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

def get_current_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin") 
    correct_password = secrets.compare_digest(credentials.password, "admin") 
    
    is_correct_username = correct_username
    is_correct_password = correct_password
    
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password for admin access",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username