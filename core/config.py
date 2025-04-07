import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration class for application settings.

    Reads environment variables or uses default values for critical settings
    such as database connection info and JWT-related parameters.

    Attributes:
        DB_HOST (str): Host address for the database server.
        DB_PORT (str): Port number for the database server.
        DB_NAME (str): Name of the database to connect to.
        DB_USER (str): Username used to authenticate with the database.
        DB_PASSWORD (str): Password used to authenticate with the database.
        SECRET_KEY (str): Secret key used for JWT encoding/decoding.
        ALGORITHM (str): The hashing algorithm used for JWT.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Token expiration time in minutes.
    """

    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_NAME: str = os.getenv("DB_NAME", "mvc_backend")
    DB_USER: str = os.getenv("DB_USER", "admin")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "admin")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "examplesecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


# Global settings instance accessible throughout the application
settings = Settings()
