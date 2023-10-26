from logging import getLogger

logger = getLogger(__name__)


class TextToSpeechServiceInterface:
    def text_to_speech(self, text: str) -> None:
        raise NotImplementedError

    def save(self, name: str) -> None:
        raise NotImplementedError

    def get_TTS_driver_name(self) -> str:
        raise NotImplementedError

    def get_TTS_voice_name(self) -> str:
        raise NotImplementedError
