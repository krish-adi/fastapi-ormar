from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


class Settings(BaseSettings):
    environment: str
    base_dir: Path = BASE_DIR

    class Config:
        env_file = ".env"


settings = Settings()
