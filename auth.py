# This file handles all authentication-related logic, including
# password hashing, verification, and admin authorization.

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
import secrets
from sqlalchemy.orm import Session
from typing import Optional

import models 
import crud

# Use bcrypt for password hashing, which is a strong and widely-used algorithm.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generates a hash for a plain-text password.
    """
    return pwd_context.hash(password)

def authenticate_player(db: Session, name: str, password: str) -> Optional[models.Player]:
    """
    Authenticates a player by their name and password.
    Returns the player object if authentication is successful, otherwise None.
    """
    player = crud.get_player_by_name(db, name=name)
    if not player:
        return None
    if not verify_password(password, player.hashed_password):
        return None
    return player

# --- Admin Authentication ---

# Custom exception for admin authentication failures.
admin_credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid admin credentials",
    headers={"WWW-Authenticate": "Basic"},
)

def get_current_admin(credentials: HTTPBasicCredentials = Depends(HTTPBasic(realm="admin"))):
    """
    A dependency that protects admin-only endpoints. It uses Basic Authentication
    to verify admin credentials.
    """
    # In a real-world application, these credentials should be stored securely,
    # for example, in environment variables or a secrets management service.
    correct_username = "admin"
    correct_password = "admin"
    
    # Use `secrets.compare_digest` to prevent timing attacks.
    is_user_correct = secrets.compare_digest(credentials.username, correct_username)
    is_pass_correct = secrets.compare_digest(credentials.password, correct_password)
    
    if not (is_user_correct and is_pass_correct):
        raise admin_credentials_exception
    
    return credentials.username