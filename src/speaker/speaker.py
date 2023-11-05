from src.config.speaker_config import SpeakerConfig, TTSEnum
from src.speaker.gmail.service import GmailService

from .text_to_speech.interface import TextToSpeechInterface
from .text_to_speech.service_implementation.text_to_speech_elevenabs import (
    TextToSpeechElevenLabs,
)
from .text_to_speech.service_implementation.text_to_speech_pyttsx3 import (
    TextToSpeechPyttsx3,
)


class Speaker:
    tts: TextToSpeechInterface
    name: str
    personality: str
    gmail_connector: GmailService

    def __init__(self, config: SpeakerConfig):
        self.name: str = config.name
        self.personality: str = config.personality
        if config.TTS == TTSEnum.ELEVENLABS:
            self.tts = TextToSpeechElevenLabs(voice_id=config.voice)
        elif config.TTS == TTSEnum.PYTTSX3:
            self.tts = TextToSpeechPyttsx3(voice=config.voice)
        else:
            raise Exception(f"Unknown TTS engine: {config.TTS}")
