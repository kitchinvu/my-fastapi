"""Application configuration management."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Attributes:
        DATABASE_URL: MySQL database connection string.
        PROJECT_NAME: Name of the API project.
        DEBUG: Debug mode flag.
        API_VERSION: API version string.
        JWT_SECRET_KEY: Secret key for JWT token signing.
        JWT_ALGORITHM: JWT encoding algorithm.
        JWT_ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration time in minutes.
    """

    DATABASE_URL: str = "mysql+pymysql://fastapi_user:fastapi_password@localhost:3306/user_management"
    PROJECT_NAME: str = "User Management API"
    DEBUG: bool = True
    API_VERSION: str = "1.0.0"
    JWT_SECRET_KEY: str = "change-this-to-random-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Global settings instance
settings = Settings()
