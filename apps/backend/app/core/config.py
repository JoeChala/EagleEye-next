from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EagleEye v2"
    app_version: str = "0.1.0"
    api_title: str = "EagleEye API"
    api_description: str = "AI-powered Face Recognition Attendance System"
    environment: str = "development"
    debug: bool = False
    api_prefix: str = "/api/v1"
    database_url: str = ""
    supabase_url: str = ""
    supabase_key: str = ""
    jwt_secret: str = ""
    redis_url: str = ""
    model_path: str = ""
    allowed_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
        ]
    )
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, value: object) -> list[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return []

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("DATABASE_URL cannot be empty.")

        return value

    @field_validator("app_name", mode="before")
    @classmethod
    def normalize_app_name(cls, value: object) -> str:
        if isinstance(value, str):
            normalized = value.strip()
            if normalized:
                if normalized.lower() == "eagleeye":
                    return "EagleEye v2"
                return normalized
        return "EagleEye v2"

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value: object) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "y", "on"}:
                return True
            if normalized in {"0", "false", "no", "n", "off", "release"}:
                return False
        return bool(value)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
