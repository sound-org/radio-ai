from logging import getLogger
from typing import Iterator, Literal, Union

from elevenlabs import Voice, generate, save, set_api_key

from ..config import TextToSpeechConfig
from ..service_interface import TextToSpeechServiceInterface

logger = getLogger(__name__)


class TextToSpeechServiceElevenLabs(TextToSpeechServiceInterface):
    _voice: Voice
    _model: str
    _generated_audio: Union[bytes, Iterator[bytes]]

    def __init__(self, voice_id: str="TX3LPaxmHKxFdv7VOQHJ"):
        set_api_key(api_key=TextToSpeechConfig.elevenlabs_api_key)
        self._voice = Voice.from_id(voice_id)
        self._model = "eleven_monolingual_v1"

    def text_to_speech(self, text: str) -> None:
        self._generated_audio = generate(
            text=text, voice=self._voice, model=self._model
        )

    def save(self, filename: str) -> None:
        save(audio=self._generated_audio, filename=filename)

    def get_TTS_driver_name(self) -> Literal["elevenlabs"]:
        return "elevenlabs"

    def get_TTS_voice_name(self) -> str:
        return self._voice.name
