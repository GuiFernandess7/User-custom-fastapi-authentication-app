import os 
import sys
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_directory)
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASSWORD : str = os.environ.get("DB_PASSWORD")
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_HOST: str = os.environ.get("DB_HOST")
    DATABASE_URL: str = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ALGORITHM : str = os.environ.get("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")

def get_settings() -> Settings:
    return Settings()