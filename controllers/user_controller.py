from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import SessionLocal
from schemas.user_schema import UserCreate, UserLogin
from services.user_service import register_user, login_user

# Initialize API router for authentication-related endpoints
router = APIRouter()


def get_db():
    """
    Dependency function that provides a SQLAlchemy database session.
    This ensures that the session is properly closed after the request is completed.

    :return: Generator yielding a scoped database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint for registering a new user account.

    :param user_data: User registration data including email, password, etc.
    :param db: SQLAlchemy session used to interact with the database
    :return: A dictionary containing a generated access token
    """
    token = register_user(user_data, db)
    return {"access_token": token}


@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Endpoint for logging in an existing user.

    :param user_data: Login credentials (email and password)
    :param db: SQLAlchemy session used to retrieve and verify user data
    :return: A dictionary containing a generated access token if credentials are valid
    """
    token = login_user(user_data, db)
    return {"access_token": token}
