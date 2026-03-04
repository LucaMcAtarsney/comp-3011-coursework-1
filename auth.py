from passlib.context import CryptContext
import secrets
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
import string

# --- Existing password hashing code ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def generate_password(length: int = 12) -> str:
    """Generate a random password."""
    return "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# --- Admin Authentication Logic ---
security = HTTPBasic()

def get_current_admin(credentials: HTTPBasicCredentials = Depends(security)):
    # In a real app, use a secure password from config
    correct_username = "admin" 
    correct_password = "admin" 
    
    is_correct_username = secrets.compare_digest(credentials.username, correct_username)
    is_correct_password = secrets.compare_digest(credentials.password, correct_password)
    
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password for admin access",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username