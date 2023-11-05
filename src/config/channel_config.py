from typing import Dict

from .speaker_config import SpeakerConfig


class ChannelConfig:
    def __init__(self, channel_config: Dict[str, str]) -> None:
        self.id: int = channel_config.get("id")
        self.name: str = channel_config.get("name")
        self.description: str = channel_config.get("description")
        self.music_theme: str = channel_config.get("music_theme")
        speaker_config = channel_config.get("speaker")
        if speaker_config:
            self.speaker: SpeakerConfig = SpeakerConfig(speaker_config)
        else:
            self.speaker = None
        if not all(
            [self.id, self.name, self.description, self.music_theme, self.speaker]
        ):
            raise Exception("Channel configuration is incomplete")
