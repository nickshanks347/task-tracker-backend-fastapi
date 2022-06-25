from dotenv import load_dotenv
import os
from pathlib import Path

path = Path(__file__).parent.parent / "data" / "config.env"
load_dotenv(path)

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JSON_SECRET_KEY = os.getenv("JSON_SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    ENABLE_REGISTRATIONS = os.getenv("ENABLE_REGISTRATIONS") == "1"
    ENCRYPT_JSON = os.getenv("ENCRYPT_JSON") == "1"
    RELOAD = os.getenv("RELOAD") == "1"
    HOST = os.getenv("HOST")
    PORT = int(os.getenv("PORT"))