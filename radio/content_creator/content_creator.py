from typing import List

from radio.channel.channel import Channel
from radio.config.radio_config import RadioConfig


class ContentCreator:
    channels: List[Channel] = []

    def __init__(self, config: RadioConfig):
        for channel_config in config.channels.values():
            self.channels.append(Channel(channel_config))
