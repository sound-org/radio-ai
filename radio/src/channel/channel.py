import logging
import os
import subprocess
import time
from typing import List

from src.channel.audio_merger import AudioMerger
from src.config.channel_config import ChannelConfig
from src.data_storage.create_dir_if_not_exist import create_dir_if_not_exists
from src.music_generator.music_generator import MusicGenerator
from src.speaker.speaker import Speaker

logger = logging.getLogger(__name__)


class Channel:
    _speaker: Speaker
    _music_generator: MusicGenerator

    def __init__(self, config: ChannelConfig):
        self._speaker = Speaker(config=config.speaker)
        self._music_generator = MusicGenerator(config=config.music)
        self._name: str = config.name
        self._description: str = config.description
        self._broadcast_output_dir: str = config.broadcast_output_dir
        self._streaming_output_dir: str = config.streaming_output_dir
        create_dir_if_not_exists(self._broadcast_output_dir)
        create_dir_if_not_exists(self._streaming_output_dir)

    def create_broadcast(self):
        """
        Creates a broadcast by generating a timestamp and filename,
        composing the broadcast file, and preparing it for streaming.
        """
        ts = int(time.time())
        filename: str = time.strftime("%Y%m%d-%H%M%S")
        broadcast_file: str = self._compose_broadcast(
            filename=filename, timestamp=str(ts)
        )
        self._prepare_broadcast_for_streaming(
            broadcast_file=broadcast_file,
            human_readable_timestamp=filename,
            timestamp=str(ts),
        )

    def _generate_music(self, n: int):
        self._music_generator.generate_music(n)

    def _generate_speaker_lines(self) -> tuple[str, str]:
        return self._speaker.generate_random_lines()

    def _react_to_email_message(self) -> tuple[str, str]:
        return self._speaker.react_to_email_message()

    def _get_music(self) -> List[str]:
        return self._music_generator.get_music()

    def _prepare_broadcast_for_streaming(
        self, broadcast_file: str, human_readable_timestamp: str, timestamp: str
    ):
        logger.info("Preparing broadcast in file %s for streaming...", broadcast_file)
        output_dir = os.path.join(self._streaming_output_dir, timestamp)
        create_dir_if_not_exists(output_dir)

        os_command = (
            f"ffmpeg -i {broadcast_file} -c:a libmp3lame -b:a 128k "
            f"-map 0:0 -f segment -segment_time 10 "
            f"-segment_list {output_dir}/outputlist.m3u8 "
            f"-segment_format mp3 {output_dir}/output-{timestamp}%03d.ts"
        )
        try:
            subprocess.run(
                args=os_command,
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception as e:
            logger.error(f"Error while running command: {os_command}")
            logger.error(f"Error message: {e}")

    def _get_intro(self):
        return "audio_samples/sample-1.mp3"

    def _get_outro(self):
        return "audio_samples/sample-2.mp3"

    def _compose_broadcast(self, filename: str, timestamp: str) -> str:
        logger.info("Composing broadcast...")

        logger.info("Generating speaker lines...")
        _, speaker_lines_path = self._generate_speaker_lines()
        _, speaker_reaction_to_email_path = self._react_to_email_message()

        logger.info("Generating music...")
        music_paths: List[str] = self._get_music()

        intro_path = self._get_intro()
        outro_path = self._get_outro()

        paths_to_audio_files: List[str] = []
        paths_to_audio_files.append(intro_path)
        paths_to_audio_files.append(speaker_lines_path)
        paths_to_audio_files.append(speaker_reaction_to_email_path)
        paths_to_audio_files.extend(music_paths)
        # paths_to_audio_files.append(outro_path)

        output_file = os.path.join(
            self._broadcast_output_dir,
            f"broadcast-{filename}-{timestamp}.mp3",
        )
        logger.info("Merging audio files and saving to %s", output_file)
        for path in paths_to_audio_files:
            logger.info("Path: %s", path)

        logger.info("Merging audio files and saving to %s", output_file)
        AudioMerger.merge_audio_files(paths_to_audio_files, output_file)
        return output_file
