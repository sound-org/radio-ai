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


class Speaker:
    _tts: TextToSpeechInterface
    _name: str
    _personality: str
    _gmail_connector: GmailService
    _llm: LLM

    def __init__(self, config: SpeakerConfig):
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

    def generate_speaker_lines(self):
        return self._llm.generate_speaker_lines("say next thing")

    def _get_last_email(self):
        pass

    def _react_to_email(self):
        pass

    def _say_cool_things(self):
        pass
