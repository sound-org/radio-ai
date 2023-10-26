from logging import getLogger

logger = getLogger(__name__)


# class TextToSpeechService:
#     def __init__(
#         self,
#         voice: str = TextToSpeechConfig.voice,
#         rate: int = TextToSpeechConfig.rate,
#         volume: float = TextToSpeechConfig.volume,
#     ):
#         self._audio_merger = AudioMerger()
#         self._tts_engine = TextToSpeechEngine(voice=voice, rate=rate, volume=volume)

#     def text_to_speech(self, text: str, say: bool, save: bool, file_name: str) -> None:
#         self._tts_engine.text_to_speech(text, say, save, file_name)

#     def text_to_speech_elevenlabs(self, text: str, filename: str) -> None:
#         voice: Voice = Voice.from_id("TX3LPaxmHKxFdv7VOQHJ")
#         logger.info("Using voice %s", voice)
#         voice_file_name = self._get_path_for_filename(filename)
#         audio = generate(
#             text=text,
#             voice=voice,
#             model="eleven_monolingual_v1",
#         )
#         save(audio=audio, filename=voice_file_name)


class TextToSpeechServiceInterface:
    def text_to_speech(self, text: str) -> None:
        raise NotImplementedError

    def save(self, name: str) -> None:
        raise NotImplementedError

    def get_TTS_driver_name(self) -> str:
        raise NotImplementedError

    def get_TTS_voice_name(self) -> str:
        raise NotImplementedError
