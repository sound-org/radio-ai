import json
from os import path

from .radio_config import RadioConfig


class ConfigParser:
    path: str = "radio_config.json"

    @staticmethod
    def get_config() -> RadioConfig:
        """
        Get the radio configuration from the config file.

        Returns:
            RadioConfig: The radio configuration object.

        Raises:
            Exception: If the config file is not found.
        """
        if path.exists(ConfigParser.path):
            with open(ConfigParser.path, "r") as f:
                config = json.load(f)
                return RadioConfig(config)
        else:
            raise Exception("Config file not found")
