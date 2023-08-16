import os

from starlette.config import Config

from dotenv import load_dotenv

from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

config = Config()


class Settings:
    PROJECT_NAME: str = "Event App"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", default=False)

    DB_DRIVER: str = os.getenv("DB_DRIVER", default="db_driver")
    DB_USER: str = os.getenv("DB_USER", default="db_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", default="db_password")
    DB_HOST: str = os.getenv("DB_HOST", default="localhost")
    DB_PORT: str = os.getenv("DB_PORT", default="db_port")
    DB_NAME: str = os.getenv("DB_NAME", default="db_name")
    DATABASE_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", default=20))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", default=60 * 24 * 2))


settings = Settings()
