from logging import getLogger

from src.config.speaker_config import SpeakerConfig, TTSEnum
from src.data_storage.create_dir_if_not_exist import create_dir_if_not_exists
from src.speaker.gmail.gmail import Gmail
from src.speaker.llm.llm import LLM

from .text_to_speech.interface import TextToSpeechInterface
from .text_to_speech.service_implementation.text_to_speech_elevenlabs import (
    TextToSpeechElevenLabs,
)
from .text_to_speech.service_implementation.text_to_speech_pyttsx3 import (
    TextToSpeechPyttsx3,
)

logger = getLogger(__name__)


class Speaker:
    """
    Represents a speaker that generates random lines and reacts to email messages.
    """

    _tts: TextToSpeechInterface
    _name: str
    _personality: str
    _gmail: Gmail
    _llm: LLM

    def __init__(self, config: SpeakerConfig):
        """
        Initializes a Speaker instance with the given configuration.

        Args:
            config (SpeakerConfig): The configuration for the speaker.
        """
        logger.info(f"Initializing Speaker with config: {config}")
        self._name: str = config.name
        self._personality: str = config.personality
        create_dir_if_not_exists(config.output_dir)

        if config.TTS == TTSEnum.ELEVENLABS:
            self._tts = TextToSpeechElevenLabs(
                output_dir=config.output_dir, voice_id=config.voice
            )
        elif config.TTS == TTSEnum.PYTTSX3:
            self._tts = TextToSpeechPyttsx3(
                output_dir=config.output_dir, voice=config.voice
            )
        else:
            raise Exception(f"Unknown TTS engine: {config.TTS}")

        self._gmail = Gmail()
        self._llm = LLM(personality=self._personality)

    def generate_random_lines(self) -> tuple[str, str]:
        """
        Generates random lines for the speaker.

        Returns:
            tuple[str, str]: A tuple containing the generated lines and the path to the generated speech file.
        """
        logger.info(f"{self._name}: Generating lines...")
        lines: str = self._say_cool_things()
        path: str = self._text_to_speech(text=lines)
        return (lines, path)

    def react_to_email_message(self) -> tuple[str, str]:
        """
        Reacts to the latest email from fans.

        Returns:
            tuple[str, str]: A tuple containing the speaker's reaction to the email and the path to the generated speech file.
        """
        logger.info(f"{self._name}: Reacting to email message...")
        email: str = self._get_last_email()
        speaker_reaction: str = self._react_to_email(email)
        path = self._text_to_speech(text=speaker_reaction)
        return (speaker_reaction, path)

    def _get_last_email(self) -> str:
        """
        Gets the latest email.

        Returns:
            str: The content of the latest email.
        """
        logger.info("Getting last email...")
        return self._gmail.get_latest_message()

    def _react_to_email(self, email: str) -> str:
        """
        Reacts to an email.

        Args:
            email (str): The content of the email.

        Returns:
            str: The speaker's reaction to the email.
        """
        return self._llm.react_to_email_message(email)

    def _say_cool_things(self) -> str:
        """
        Generates cool things for the speaker to say.

        Returns:
            str: The generated lines for the speaker.
        """
        logger.info("Saying cool things...")
        return self._llm.generate_speaker_lines("say next thing")

    def _text_to_speech(self, text: str) -> str:
        """
        Converts text to speech.

        Args:
            text (str): The text to convert.

        Returns:
            str: The path to the generated speech file.
        """
        logger.info("Converting text to speech...")
        path: str = self._tts.text_to_speech(text=text)
        return path
