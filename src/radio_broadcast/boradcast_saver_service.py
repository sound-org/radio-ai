import os
import time
from logging import getLogger
from pathlib import Path
from typing import List

from src.text_to_speech.config import TextToSpeechConfig

from .audio_merger import AudioMerger

logger = getLogger(__name__)


class BroadcastSaverService:
    # NOTE: 'file' means a path to a file (containing a filename)
    # NOTE: 'filename' means just a name of a file
    def __init__(self):
        self._audio_merger = AudioMerger()
        self._intro_filename: str = TextToSpeechConfig.sample_filename_1
        self._outro_filename: str = TextToSpeechConfig.sample_filename_2
        self._output_dir: Path = Path(
            os.path.join(TextToSpeechConfig.broadcast_dir, str(time.time()))
        )

        self._create_output_dir(output_dir=self._output_dir)

    def save(
        self,
        input_voice_file: str,
        input_music_files: List[str],
        output_broadcast_filename,
    ) -> Path:
        """
        input_voice_file: must be a path to a file (NOT FILENAME)
        input_music_files: must be a list of paths to files (NOT FILENAMES)
        output_broadcast_filename: must be a name of a file (NOT PATH)
        """

        output_broadcast_file = self.get_file_from_filename(output_broadcast_filename)

        self._merge_audio_files(
            input_voice_file=input_voice_file,
            input_music_files=input_music_files,
            output_broadcast_file=output_broadcast_file,
        )
        return self._output_dir

    def _merge_audio_files(
        self,
        input_voice_file: str,
        input_music_files: List[str],
        output_broadcast_file: str,
    ) -> None:
        filenames: List[str] = []
        filenames.append(self._intro_filename)
        filenames.append(input_voice_file)
        filenames.extend(input_music_files)
        filenames.append(self._outro_filename)
        self._audio_merger.merge_audio_files(
            filenames=filenames,
            target_file=output_broadcast_file,
        )

    def _create_output_dir(self, output_dir: Path) -> None:
        os.makedirs(output_dir, exist_ok=True)

    def get_file_from_filename(self, filename: str) -> str:
        return os.path.join(self._output_dir, filename)
