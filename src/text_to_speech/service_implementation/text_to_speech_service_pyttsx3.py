from logging import getLogger
from typing import Literal

from ..config import TextToSpeechConfig
from ..service_interface import TextToSpeechServiceInterface
from .pyttsx3_engine import PyTTSx3Engine

logger = getLogger(__name__)


class TextToSpeechServicePyttsx3(TextToSpeechServiceInterface):
    def __init__(self):
        self._voice = TextToSpeechConfig.voice
        self._tts_engine: PyTTSx3Engine = PyTTSx3Engine(
            voice=TextToSpeechConfig.voice,
            rate=TextToSpeechConfig.rate,
            volume=TextToSpeechConfig.volume,
        )

    def text_to_speech(self, text: str) -> None:
        self._tts_engine.text_to_speech(text=text)

    def save(self, name: str) -> None:
        self._tts_engine.save(name)

    def get_TTS_driver_name(self) -> Literal["pyttsx3"]:
        return "pyttsx3"

    def get_TTS_voice_name(self) -> str:
        return self._voice
