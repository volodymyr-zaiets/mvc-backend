from sqlalchemy.orm import Session
from models.user_model import User
from schemas.user_schema import UserCreate, UserLogin
from core.auth import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status


def register_user(user_data: UserCreate, db: Session) -> str:
    """
    Registers a new user.

    This function performs the following steps:
    1. Checks if a user with the same email already exists.
    2. If a user already exists, raises an HTTPException with a 400 status.
    3. Hashes the user's password using `get_password_hash`.
    4. Creates a new user record in the database.
    5. Returns a JWT access token for the newly created user.

    Args:
        user_data (UserCreate): The data provided for the new user (email and password).
        db (Session): The SQLAlchemy session object used to interact with the database.

    Returns:
        str: The JWT access token that can be used for authenticating the user.

    Raises:
        HTTPException: If the email is already registered (status code 400).
    """
    # Check if the email is already in use
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password before saving the user
    hashed_password = get_password_hash(user_data.password)

    # Create a new user instance and add to the database
    user = User(email=user_data.email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)  # Refresh the user object with data from the database

    # Return an access token for the newly registered user
    return create_access_token({"user_id": user.id, "email": user.email})


def login_user(user_data: UserLogin, db: Session) -> str:
    """
    Authenticates a user and provides an access token.

    This function checks if the user's credentials (email and password) are valid:
    1. It checks whether the email exists in the database.
    2. If the email exists, it verifies the password using `verify_password`.
    3. If both are valid, it generates and returns a JWT access token for the user.

    Args:
        user_data (UserLogin): The data provided for the user login (email and password).
        db (Session): The SQLAlchemy session object used to interact with the database.

    Returns:
        str: The JWT access token that can be used for authenticating the user.

    Raises:
        HTTPException: If the credentials are invalid (status code 401).
    """
    # Retrieve the user by email from the database
    user = db.query(User).filter(User.email == user_data.email).first()

    # If no user is found or password doesn't match, raise unauthorized error
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Return an access token for the authenticated user
    return create_access_token({"user_id": user.id, "email": user.email})
