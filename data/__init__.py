import yaml
from pathlib import Path

with open(Path(__file__).parent / "config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

class Config:
    SECRET_KEY = config["main"]["SECRET_KEY"]
    ALGORITHM = config["main"]["ALGORITHM"]
    ACCESS_TOKEN_EXPIRE_MINUTES = config["main"]["ACCESS_TOKEN_EXPIRE_MINUTES"]
