from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    APP_NAME: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    QDRANT_HOST: str
    QDRANT_PORT: int

    class Config:
        env_file = ".env"

settings = Settings()