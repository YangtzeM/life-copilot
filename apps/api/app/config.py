from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Life Copilot API"
    database_url: str = "postgresql+psycopg://life:life@postgres:5432/life_copilot"
    redis_url: str = "redis://redis:6379/0"
    model_provider: str = "mock"
    enqueue_tasks: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_prefix="LIFE_")


@lru_cache
def get_settings() -> Settings:
    return Settings()
