from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from core.config import settings

# Construct the full database URL from environment configuration
# Format: mysql+mysqldb://<user>:<password>@<host>:<port>/<database>
DATABASE_URL = (
    f"mysql+mysqldb://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# SQLAlchemy engine that manages the connection pool and communication with the database
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # Enables checking if connections are alive before using them
)

# Session factory for creating database sessions.
# - autocommit=False: ensures explicit commit/rollback handling.
# - autoflush=False: delays automatic flushing of data to the DB.
SessionLocal = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
))

# Base class for declaring models using SQLAlchemy ORM
Base = declarative_base()


def init_db():
    """
    Initializes the database by importing model definitions
    and creating the associated tables if they don't exist.

    This function is typically called during application startup.
    """
    import models.user_model  # Ensures User model is registered
    import models.post_model  # Ensures Post model is registered
    Base.metadata.create_all(bind=engine)  # Creates all tables from Base subclasses
