from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    zt_api_key: str = ""

    class Config(BaseSettings.Config):
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
