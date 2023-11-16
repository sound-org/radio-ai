import pytest

from radio.config.config_parser import ConfigParser
from radio.config.radio_config import RadioConfig

from .utils import create_valid_radio_config_file


def test_radio_config_complete(create_valid_radio_config_file):
    ConfigParser.path = create_valid_radio_config_file
    radio_config = ConfigParser.get_config()
    assert isinstance(radio_config, RadioConfig)
    assert len(radio_config.channels) == 1


def test_radio_config_file_not_found():
    ConfigParser.path = "non_existent_file.json"
    with pytest.raises(Exception) as excinfo:
        ConfigParser.get_config()
    assert "Config file not found" in str(excinfo.value)
