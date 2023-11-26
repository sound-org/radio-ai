import logging
import os
import random
import time

from radio.channel.audio_merger import AudioMerger
from radio.config.channel_config import ChannelConfig
from radio.data_storage.create_dir_if_not_exist import create_dir_if_not_exists
from radio.music_generator.music_generator import MusicGenerator
from radio.speaker.speaker import Speaker

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
        ts = str(int(time.time()))
        broadcast_file: str = self._compose_broadcast(timestamp=ts)
        self._prepare_broadcast_for_streaming(
            broadcast_file=broadcast_file, timestamp=ts
        )

    def _generate_music(self, n: int):
        self._music_generator.generate_music(n)

    def _generate_speaker_lines(self) -> tuple[str, str]:
        return self._speaker.generate_random_lines()

    def _react_to_email_message(self) -> tuple[str, str]:
        return self._speaker.react_to_email_message()

    def _get_ai_music(self):
        # TODO: it's just a mock for now

        filenames = [
            "audio_samples/musicgen_1.wav",
            "audio_samples/musicgen_2.wav",
        ]
        return random.choice(filenames)

    def _get_algorithmic_music(self):
        # TODO: it's just a mock for now
        return "audio_samples/algorithm_1.wav"

    def _prepare_broadcast_for_streaming(self, broadcast_file: str, timestamp: str):
        logger.info("Preparing broadcast in file %s for streaming...", broadcast_file)
        output_dir = os.path.join(self._streaming_output_dir, timestamp)
        create_dir_if_not_exists(output_dir)

        os_command = (
            f"ffmpeg -i {broadcast_file} -c:a libmp3lame -b:a 128k "
            f"-map 0:0 -f segment -segment_time 10 "
            f"-segment_list {output_dir}/outputlist.m3u8 "
            f"-segment_format mpegts {output_dir}/output-{timestamp}%03d.ts"
        )
        try:
            os.system(os_command)
        except Exception as e:
            logger.error(f"Error while running command: {os_command}")
            logger.error(f"Error message: {e}")

    def _get_intro(self):
        return "audio_samples/sample-1.mp3"

    def _get_outro(self):
        return "audio_samples/sample-2.mp3"

    def _compose_broadcast(self, timestamp: str) -> str:
        logger.info("Composing broadcast...")

        logger.info("Generating speaker lines...")
        _, speaker_lines_path = self._generate_speaker_lines()
        _, speaker_reaction_to_email_path = self._react_to_email_message()

        logger.info("Generating music...")
        ai_music_path = self._get_ai_music()
        algorithmic_music_path = self._get_algorithmic_music()

        intro_path = self._get_intro()
        outro_path = self._get_outro()

        paths_to_audio_files = [
            intro_path,
            speaker_lines_path,
            speaker_reaction_to_email_path,
            ai_music_path,
            algorithmic_music_path,
            outro_path,
        ]
        output_file = os.path.join(
            self._broadcast_output_dir, f"broadcast-{timestamp}.mp3"
        )

        logger.info("Merging audio files and saving to %s", output_file)
        AudioMerger.merge_audio_files(paths_to_audio_files, output_file)
        return output_file
