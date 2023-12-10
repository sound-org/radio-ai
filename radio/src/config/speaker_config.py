from enum import Enum
from typing import Dict


class TTSEnum(Enum):
    ELEVENLABS = "ELEVENLABS"
    PYTTSX3 = "PYTTSX3"


class SpeakerConfig:
    """
    Represents the configuration for a speaker.

    Args:
        speaker_config (Dict[str, str]): A dictionary containing the speaker configuration.

    Attributes:
        name (str): The name of the speaker.
        TTS (TTSEnum): The text-to-speech engine used by the speaker.
        voice (str): The voice used by the speaker.
        personality (str): The personality of the speaker.
        output_dir (str): The output directory for the speaker.

    Raises:
        Exception: If any of the required attributes are missing in the speaker configuration.
    """

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
