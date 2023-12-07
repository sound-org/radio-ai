from typing import List

from src.channel.channel import Channel
from src.config.radio_config import RadioConfig


class ContentCreator:
    """
    The ContentCreator class is responsible for creating content for radio channels.

    Attributes:
        channels (List[Channel]): A list of Channel objects representing the radio channels.

    Methods:
        __init__(config: RadioConfig): Initializes the ContentCreator object with the given RadioConfig object.
    """

    channels: List[Channel] = []

    def __init__(self, config: RadioConfig):
        for channel_config in config.channels.values():
            self.channels.append(Channel(channel_config))
