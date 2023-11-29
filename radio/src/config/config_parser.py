import json
from os import path

from .radio_config import RadioConfig


class ConfigParser:
    path: str = "radio_config.json"

    @staticmethod
    def get_config() -> RadioConfig:
        if path.exists(ConfigParser.path):
            with open(ConfigParser.path, "r") as f:
                config = json.load(f)
                return RadioConfig(config)
        else:
            raise Exception("Config file not found")
