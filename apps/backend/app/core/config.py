from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EagleEye v2"
    app_version: str = "0.1.0"

    database_url: str = ""
    supabase_url: str = ""
    supabase_key: str = ""
    jwt_secret: str = ""
    redis_url: str = ""
    model_path: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

