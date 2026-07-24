from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+asyncpg://taskmanager:taskmanager@localhost:5432/taskmanager"
    )
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:8080"]


settings = Settings()
