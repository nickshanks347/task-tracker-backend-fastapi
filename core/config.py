import os
from pathlib import Path

from dotenv import load_dotenv

try:

    class Config:
        path = Path(__file__).parent.parent / "data" / "config.env"
        load_dotenv(path)

        JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
        JSON_SECRET_KEY = os.getenv("JSON_SECRET_KEY")
        ALGORITHM = os.getenv("ALGORITHM")
        ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        ENABLE_REGISTRATIONS = os.getenv("ENABLE_REGISTRATIONS") == "1"
        ENCRYPT_JSON = os.getenv("ENCRYPT_JSON") == "1"
        RELOAD = os.getenv("RELOAD") == "1"
        HOST = os.getenv("HOST")
        PORT = int(os.getenv("PORT"))

except (FileNotFoundError, TypeError, ImportError) as err:
    print(f"{err}\n")
    print("Config file not found...")
    print("Please ensure config.env exists in the data directory...")
