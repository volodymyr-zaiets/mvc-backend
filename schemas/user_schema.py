from pydantic import BaseModel, EmailStr, constr
from datetime import datetime


class UserCreate(BaseModel):
    """
    Pydantic schema for creating a new user.

    This schema validates the user data during the registration process.
    It ensures that the email is valid and the password meets the minimum length requirement.
    """
    # Email field, must be a valid email format
    email: EmailStr

    # Password field: must be between 8 and 128 characters long
    password: constr(min_length=8, max_length=128)


class UserLogin(BaseModel):
    """
    Pydantic schema for user login.

    This schema validates the user credentials during the login process.
    """
    # Email field for login: must be a valid email
    email: EmailStr

    # Password field for login: should be a plain string (not hashed)
    password: str


class UserOut(BaseModel):
    """
    Pydantic schema for returning user data after successful registration or login.

    This schema is used to serialize the user object when sending data back to the client.
    """
    id: int  # Unique identifier for the user
    email: EmailStr  # The email address of the user
    created_at: datetime  # Timestamp of when the user account was created

    class Config:
        # This option allows the model to accept data from ORM objects like SQLAlchemy models
        from_attributes = True
