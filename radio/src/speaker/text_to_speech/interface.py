from logging import getLogger

logger = getLogger(__name__)


class TextToSpeechInterface:
    """Interface for text-to-speech functionality."""

    def text_to_speech(self, text: str) -> str:
        """Converts the given text to speech.

        Args:
            text (str): The text to be converted.

        Returns:
            str: File path to the generated speech file.
        """
        raise NotImplementedError

    def get_TTS_driver_name(self) -> str:
        """Returns the name of the text-to-speech driver.

        Returns:
            str: The name of the driver.
        """
        raise NotImplementedError

    def get_TTS_voice_name(self) -> str:
        """Returns the name of the text-to-speech voice.

        Returns:
            str: The name of the voice.
        """
        raise NotImplementedError
