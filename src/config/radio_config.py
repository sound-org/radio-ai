from typing import Dict

from .channel_config import ChannelConfig


class RadioConfig:
    def __init__(self, radio_config: Dict[str, any]) -> None:
        self.channels: Dict[int, ChannelConfig] = {}
        for channel_config_dict in radio_config.get("channels", []):
            channel_id = channel_config_dict.get("id")
            self.channels[int(channel_id)] = ChannelConfig(channel_config_dict)

        if not self.channels:
            raise Exception("Radio configuration is incomplete")
