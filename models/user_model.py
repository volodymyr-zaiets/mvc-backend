from sqlalchemy import Column, Integer, String, DateTime, func, UniqueConstraint
from core.database import Base


class User(Base):
    """
    SQLAlchemy model representing a user entity in the database.

    Each user has an email (which must be unique), a hashed password,
    and a timestamp indicating when the user was created.
    The email field is constrained to ensure no duplicates exist in the database.
    """
    __tablename__ = "users"
    # Unique constraint on the email field to ensure no two users have the same email
    __table_args__ = (UniqueConstraint("email", name="uq_user_email"),)

    id = Column(Integer, primary_key=True, index=True)
    # Email address of the user; unique to each user
    email = Column(String(255), nullable=False)
    # Hashed password for secure storage of user credentials
    hashed_password = Column(String(255), nullable=False)
    # Timestamp automatically set to the current time when the user is created
    created_at = Column(DateTime(timezone=True), server_default=func.now())
