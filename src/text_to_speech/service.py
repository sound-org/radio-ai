from text_to_speech.audio_merger import AudioMerger

from .config import TextToSpeechConfig
from .text_to_speech import TextToSpeechEngine


class TextToSpeechService:
    def __init__(
        self,
        voice: str = TextToSpeechConfig.voice,
        rate: int = TextToSpeechConfig.rate,
        volume: float = TextToSpeechConfig.volume,
    ):
        self._tts_engine = TextToSpeechEngine(voice=voice, rate=rate, volume=volume)
        self._audio_merger = AudioMerger()

    def text_to_speech(self, text: str, say: bool, save: bool, file_name: str) -> None:
        self._tts_engine.text_to_speech(text, say, save, file_name)

    def prepare_audition(self, text: str, voice_file_name: str) -> None:
        self.text_to_speech(text, say=False, save=True, file_name=voice_file_name)

    def _merge_audio_files(self, voice_file_name: str, audition_file_name: str) -> None:
        self._audio_merger.merge_audio_files(
            filenames=[
                TextToSpeechConfig.sample_filename_1,
                voice_file_name,
                TextToSpeechConfig.sample_filename_2,
            ],
            target_filename=audition_file_name,
        )
