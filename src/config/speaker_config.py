from enum import Enum
from typing import Dict


class TTSEnum(Enum):
    ELEVENLABS = "ELEVENLABS"
    PYTTSX3 = "PYTTSX3"


class SpeakerConfig:
    def __init__(self, speaker_config: Dict[str, str]) -> None:
        self.name: str = speaker_config.get("name")
        self.voice: str = speaker_config.get("voice")
        self.TTS: TTSEnum = (
            TTSEnum(speaker_config.get("TTS")) if speaker_config.get("TTS") else None
        )
        self.personality: str = speaker_config.get("personality")

        if not all([self.name, self.voice, self.TTS, self.personality]):
            raise Exception("Speaker configuration is incomplete")
