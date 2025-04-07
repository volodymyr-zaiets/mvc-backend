from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from core.config import settings
from core.database import SessionLocal
from models.user_model import User

# Security configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTPBearer is used for token-based authentication
security = HTTPBearer()


def get_password_hash(password: str) -> str:
    """
    Hashes a plain-text password using bcrypt.

    Args:
        password (str): The plain password to hash.

    Returns:
        str: A hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if a plain password matches its hashed version.

    Args:
        plain_password (str): The original password in plain text.
        hashed_password (str): The hashed password stored in the DB.

    Returns:
        bool: True if match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Generates a JWT access token with optional expiration.

    Args:
        data (dict): The payload to encode into the JWT.
        expires_delta (timedelta, optional): Custom expiration time.
            If not provided, defaults to settings value.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """
    Decodes a JWT token and validates its signature.

    Args:
        token (str): The JWT token to decode.

    Raises:
        HTTPException: If the token is invalid or malformed.

    Returns:
        dict: Decoded token payload.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(lambda: SessionLocal())
) -> User:
    """
    Dependency function that retrieves the current authenticated user.

    Args:
        credentials (HTTPAuthorizationCredentials): Extracted token from Authorization header.
        db (Session): SQLAlchemy session dependency.

    Raises:
        HTTPException: If token is invalid or user is not found.

    Returns:
        User: The authenticated user object from the database.
    """
    payload = decode_token(credentials.credentials)
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
