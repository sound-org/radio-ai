from typing import Any, Dict

from .channel_config import ChannelConfig


class RadioConfig:
    """
    Represents the configuration for a radio.

    Args:
        radio_config (Dict[str, any]): The dictionary containing the radio configuration.

    Attributes:
        channels (Dict[int, ChannelConfig]): A dictionary of channel configurations, where the key is the channel ID and the value is the corresponding ChannelConfig object.

    Raises:
        Exception: If the radio configuration is incomplete (i.e., no channels are defined).
    """

    def __init__(self, radio_config: Dict[str, Any]) -> None:
        self.channels: Dict[int, ChannelConfig] = {}
        for channel_config_dict in radio_config.get("channels", []):
            channel_id = channel_config_dict.get("id")
            self.channels[int(channel_id)] = ChannelConfig(channel_config_dict)

        if not self.channels:
            raise Exception("Radio configuration is incomplete")
