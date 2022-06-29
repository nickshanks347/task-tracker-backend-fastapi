import os
import sys
from importlib import reload
from pathlib import Path

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_config_file_not_found():
    with pytest.raises(ImportError):
        from main import Config

        Config.path = Path(__file__).parent.parent / "data" / "config_not_found.env"
        reload(Config)
