from logging import getLogger

logger = getLogger(__name__)


class TextToSpeechInterface:
    def text_to_speech(self, text: str) -> str:
        raise NotImplementedError

    def get_TTS_driver_name(self) -> str:
        raise NotImplementedError

    def get_TTS_voice_name(self) -> str:
        raise NotImplementedError
