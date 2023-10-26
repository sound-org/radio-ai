import logging
from pathlib import Path
from typing import List

from src.radio_broadcast.boradcast_saver_service import BroadcastSaverService
from src.text_to_speech.config import TextToSpeechConfig
from src.text_to_speech.service_implementation.text_to_speech_service_elevenabs import (
    TextToSpeechServiceElevenLabs,
)
from src.text_to_speech.service_interface import TextToSpeechServiceInterface

from .audio_filename_builder import AudioFilenameBuilder
from .audio_merger import AudioMerger

logger = logging.getLogger(__name__)


class RadioBroadcastService:
    # NOTE: a single radio broadcast is a: intro + speaker voice + music + outro

    def __init__(self) -> None:
        self._audio_merger: AudioMerger = AudioMerger()
        self._text_to_speech_service: TextToSpeechServiceInterface = (
            # TextToSpeechServicePyttsx3()
            TextToSpeechServiceElevenLabs(TextToSpeechConfig.elevenlabs_voice_id)
        )

    def create_broadcast(self, speaker_text: str, music_files: List[str]) -> Path:
        broadcast_saver: BroadcastSaverService = BroadcastSaverService()
        output_broadcast_filename: str = self.get_broadcast_name()

        voice_filename: str = self.get_voice_filename()
        voice_file: str = broadcast_saver.get_file_from_filename(
            filename=voice_filename
        )
        logger.info("Running TTS for %s", speaker_text)
        self._text_to_speech_service.text_to_speech(speaker_text)
        logger.info("Saving TTS output to %s", voice_file)
        self._text_to_speech_service.save(voice_file)

        path: Path = broadcast_saver.save(
            input_voice_file=voice_file,
            input_music_files=music_files,
            output_broadcast_filename=output_broadcast_filename,
        )

        return path

    def get_voice_filename(self) -> str:
        return (
            AudioFilenameBuilder()
            .add(self._text_to_speech_service.get_TTS_driver_name())
            .add(self._text_to_speech_service.get_TTS_voice_name())
            .build()
        )

    def get_broadcast_name(self) -> str:
        return (
            AudioFilenameBuilder()
            .add("broadcast")
            .add(self._text_to_speech_service.get_TTS_driver_name())
            .add(self._text_to_speech_service.get_TTS_voice_name())
            .build()
        )
