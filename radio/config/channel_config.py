from typing import Dict

from radio.config.music_config import MusicConfig

from .speaker_config import SpeakerConfig


class ChannelConfig:
    def __init__(self, channel_config: Dict[str, str]) -> None:
        self.id: int = channel_config.get("id")
        self.name: str = channel_config.get("name")
        self.description: str = channel_config.get("description")
        self.broadcast_output_dir: str = channel_config.get("broadcast_output_dir")
        self.streaming_output_dir: str = channel_config.get("streaming_output_dir")
        speaker_config = channel_config.get("speaker")
        if speaker_config:
            self.speaker: SpeakerConfig = SpeakerConfig(speaker_config)
        else:
            self.speaker = None
        music_config = channel_config.get("music")
        if music_config:
            self.music = MusicConfig(music_config)
        else:
            self.music = None
        if not all(
            [
                self.id,
                self.name,
                self.description,
                self.broadcast_output_dir,
                self.streaming_output_dir,
                self.speaker,
                self.music,
            ]
        ):
            raise Exception("Channel configuration is incomplete")
