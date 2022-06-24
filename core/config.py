import yaml
from pathlib import Path

with open(Path(__file__).parent.parent / "data" / "config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


class Config:
    JWT_SECRET_KEY = config["main"]["JWT_SECRET_KEY"]
    JSON_SECRET_KEY = config["main"]["JSON_SECRET_KEY"]
    ALGORITHM = config["main"]["ALGORITHM"]
    ACCESS_TOKEN_EXPIRE_MINUTES = config["main"]["ACCESS_TOKEN_EXPIRE_MINUTES"]
    ENABLE_REGISTRATIONS = config["main"]["ENABLE_REGISTRATIONS"]
    ENCRYPT_JSON = config["main"]["ENCRYPT_JSON"]
