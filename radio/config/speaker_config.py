from enum import Enum
from typing import Dict


class TTSEnum(Enum):
    ELEVENLABS = "ELEVENLABS"
    PYTTSX3 = "PYTTSX3"


class SpeakerConfig:
    def __init__(self, speaker_config: Dict[str, str]) -> None:
        self.name: str = speaker_config.get("name")
        self.TTS: TTSEnum = (
            TTSEnum(speaker_config.get("TTS")) if speaker_config.get("TTS") else None
        )
        self.voice: str = speaker_config.get("voice")
        self.personality: str = speaker_config.get("personality")
        self.output_dir: str = speaker_config.get("output_dir")
        if not all(
            [self.name, self.TTS, self.voice, self.personality, self.output_dir]
        ):
            raise Exception("Speaker configuration is incomplete")
