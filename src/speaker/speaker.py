from logging import getLogger

from src.config.speaker_config import SpeakerConfig, TTSEnum
from src.speaker.gmail.service import GmailService
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
    _tts: TextToSpeechInterface
    _name: str
    _personality: str
    _gmail_connector: GmailService
    _llm: LLM

    def __init__(self, config: SpeakerConfig):
        logger.info(f"Initializing Speaker with config: {config}")
        self._name: str = config.name
        self._personality: str = config.personality
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

        self._gmail_connector = GmailService()
        self._llm = LLM(personality=self._personality)

    def generate_random_lines(self) -> tuple[str, str]:
        """
        Generates random lines for the speaker.

        Returns:
            tuple[str, str]: (lines, path)
        """
        logger.info("Generating speaker lines...")
        lines: str = self._say_cool_things()
        path: str = self._text_to_speech(text=lines)
        return (lines, path)

    def react_to_email_message(self) -> tuple[str, str]:
        """
        React to latest email from fans.

        Returns:
            tuple[str, str]: (lines, path)
        """
        logger.info("Reacting to email message...")
        email: str = self._get_last_email()
        speaker_reaction: str = self._react_to_email(email)
        path = self._text_to_speech(text=speaker_reaction)
        return (speaker_reaction, path)

    def _get_last_email(self) -> str:
        logger.info("Getting last email...")
        return self._gmail_connector.get_latest_message()

    def _react_to_email(self, email: str) -> str:
        logger.info("Reacting to email...")
        return self._llm.react_to_email_message(email)

    def _say_cool_things(self) -> str:
        logger.info("Saying cool things...")
        return self._llm.generate_speaker_lines("say next thing")

    def _text_to_speech(self, text: str) -> str:
        logger.info("Converting text to speech...")
        path: str = self._tts.text_to_speech(text=text)
        return path
