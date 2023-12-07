from logging import getLogger
from typing import Literal

from ..config import TextToSpeechConfig
from ..interface import TextToSpeechInterface
from .pyttsx3_engine import PyTTSx3Engine

logger = getLogger(__name__)


class TextToSpeechPyttsx3(TextToSpeechInterface):
    """
    A class that implements the TextToSpeechInterface using pyttsx3 library.

    Args:
        output_dir (str): The directory where the generated speech files will be saved.
        voice (str, optional): The voice to be used for text-to-speech conversion. Defaults to "english".
    """

    def __init__(self, output_dir: str, voice: str = "english"):
        self._voice: str = voice
        self._tts_engine: PyTTSx3Engine = PyTTSx3Engine(
            voice=voice,
            rate=TextToSpeechConfig.rate,
            volume=TextToSpeechConfig.volume,
        )
        self._output_dir = output_dir

    def text_to_speech(self, text: str) -> str:
        """
        Convert the given text to speech.

        Args:
            text (str): The text to be converted to speech.

        Returns:
            str: The path of the generated speech file.
        """
        logger.info("Text to speech for: %s", text)
        path: str = self._tts_engine.text_to_speech(
            text=text, output_dir=self._output_dir
        )
        return path

    def get_TTS_driver_name(self) -> Literal["pyttsx3"]:
        """
        Get the name of the text-to-speech driver.

        Returns:
            Literal["pyttsx3"]: The name of the text-to-speech driver.
        """
        return "pyttsx3"

    def get_TTS_voice_name(self) -> str:
        """
        Get the name of the current voice used for text-to-speech conversion.

        Returns:
            str: The name of the current voice.
        """
        return self._voice
