import os
import sys
import pytest
from pathlib import Path
from importlib import reload
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_config_file_not_found():
    with pytest.raises(ImportError) as err:
        from main import Config
        Config.path = Path(__file__).parent.parent / "data" / "config_not_found.env"
        reload(Config)
        assert err
