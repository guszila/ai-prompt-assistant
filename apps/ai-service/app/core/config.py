from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment or .env file."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Service Configuration
    AI_SERVICE_HOST: str = "127.0.0.1"
    AI_SERVICE_PORT: int = 8000
    AI_SERVICE_ENV: str = "development"
    AI_SERVICE_LOG_LEVEL: str = "info"

    # Embedded SQLite Database (Desktop-First)
    SQLITE_DB_PATH: str = "data/app.db"

    # LLM Settings (Provider-agnostic in M1)
    DEFAULT_LLM_PROVIDER: str = "mock"

    @property
    def resolved_sqlite_path(self) -> Path:
        """Resolve absolute path for SQLite database file."""
        path = Path(self.SQLITE_DB_PATH)
        if not path.is_absolute():
            # Resolve relative to project root or current working directory
            return Path.cwd() / path
        return path


settings = Settings()
