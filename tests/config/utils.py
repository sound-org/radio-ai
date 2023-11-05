import json

import pytest

from .configs import valid_radio_config


@pytest.fixture(scope="function")
def create_valid_radio_config_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "radio_config.json"
    p.write_text(json.dumps(valid_radio_config))
    return str(p)
