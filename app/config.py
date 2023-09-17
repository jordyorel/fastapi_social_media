from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

dotenv_path = ".env"
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise Exception(f"{dotenv_path} not found")


class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASWORD: str
    DATABASE_USERNAME: str
    DATABASE_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: str

    class config:
        env_file = ".env"


settings = Settings()
