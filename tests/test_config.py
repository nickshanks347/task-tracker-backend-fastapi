from importlib import reload
from pathlib import Path

import pytest
from core.config import Config


def test_config_file_not_found():
    with pytest.raises(ImportError):
        Config.path = Path(__file__).parent.parent / "data" / "config_not_found.env"
        reload(Config)
