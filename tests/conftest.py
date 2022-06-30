import os
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import Config


@pytest.fixture(scope="session")
def set_env_vars_encrypted():
    Config.ENCRYPT_JSON = 1
    Config.DATA_DIR = "tests/data_encrypted"
    yield
    Config.ENCRYPT_JSON = 0
    Config.DATA_DIR = ""


@pytest.fixture(scope="session")
def set_env_vars_plain():
    Config.ENCRYPT_JSON = 0
    Config.DATA_DIR = "tests/data_plain"
    yield
    Config.ENCRYPT_JSON = 0
    Config.DATA_DIR = ""
