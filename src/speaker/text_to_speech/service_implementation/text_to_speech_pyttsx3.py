from logging import getLogger
from typing import Literal

from ..config import TextToSpeechConfig
from ..interface import TextToSpeechInterface
from .pyttsx3_engine import PyTTSx3Engine

logger = getLogger(__name__)


class TextToSpeechPyttsx3(TextToSpeechInterface):
    def __init__(self, output_dir: str, voice: str = "english"):
        self._voice: str = voice
        self._tts_engine: PyTTSx3Engine = PyTTSx3Engine(
            voice=voice,
            rate=TextToSpeechConfig.rate,
            volume=TextToSpeechConfig.volume,
        )
        self._output_dir = output_dir

    def text_to_speech(self, text: str) -> str:
        logger.info("Text to speech for: %s", text)
        path: str = self._tts_engine.text_to_speech(
            text=text, output_dir=self._output_dir
        )
        return path

    def get_TTS_driver_name(self) -> Literal["pyttsx3"]:
        return "pyttsx3"

    def get_TTS_voice_name(self) -> str:
        return self._voice
