import logging
from pathlib import Path
from typing import List

from src.content_creator.boradcast_saver_service import BroadcastSaverService
from src.speaker.text_to_speech import TextToSpeechInterface
from src.speaker.text_to_speech.service_implementation.text_to_speech_elevenlabs import (  # noqa: F401
    TextToSpeechElevenLabs,
)
from src.speaker.text_to_speech.service_implementation.text_to_speech_pyttsx3 import (  # noqa: F401
    TextToSpeechPyttsx3,
)

from .audio_filename_builder import AudioFilenameBuilder
from .audio_merger import AudioMerger

logger = logging.getLogger(__name__)


class ContentCreatorService:
    # NOTE: a single radio broadcast is a: intro + speaker voice + music + outro

    def __init__(self) -> None:
        self._audio_merger: AudioMerger = AudioMerger()
        self._text_to_speech_service: TextToSpeechInterface = (
            TextToSpeechPyttsx3()
            # TextToSpeechServiceElevenLabs(TextToSpeechConfig.elevenlabs_voice_id)
        )

    def create_new_broadcast(self, speaker_text: str, music_files: List[str]) -> Path:
        broadcast_saver: BroadcastSaverService = BroadcastSaverService()
        output_broadcast_filename: str = self._get_broadcast_name()

        voice_filename: str = self._get_voice_filename()
        voice_file: str = broadcast_saver.get_file_from_filename(
            filename=voice_filename
        )
        logger.info("Running TTS for %s", speaker_text)
        # TODO: we should call speaker to get his lines, and then we call TTS to convert it to audio
        self._text_to_speech_service.text_to_speech(speaker_text)
        logger.info("Saving TTS output to %s", voice_file)
        self._text_to_speech_service.save(voice_file)

        path: Path = broadcast_saver.save(
            input_voice_file=voice_file,
            input_music_files=music_files,
            output_broadcast_filename=output_broadcast_filename,
        )

        return path

    def _get_voice_filename(self) -> str:
        return (
            AudioFilenameBuilder()
            .add(self._text_to_speech_service.get_TTS_driver_name())
            .add(self._text_to_speech_service.get_TTS_voice_name())
            .build()
        )

    def _get_broadcast_name(self) -> str:
        return (
            AudioFilenameBuilder()
            .add("broadcast")
            .add(self._text_to_speech_service.get_TTS_driver_name())
            .add(self._text_to_speech_service.get_TTS_voice_name())
            .build()
        )
