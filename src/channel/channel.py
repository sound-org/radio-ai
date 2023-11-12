import logging
import random

from src.channel.audio_merger import AudioMerger
from src.config.channel_config import ChannelConfig
from src.music_generator.music_generator import MusicGenerator
from src.speaker.speaker import Speaker

logger = logging.getLogger(__name__)


class Channel:
    _speaker: Speaker
    _music_generator: MusicGenerator

    def __init__(self, config: ChannelConfig):
        self._speaker = Speaker(config.speaker)
        self._music_generator = MusicGenerator(config.music)

    def _generate_speaker_lines(self) -> tuple[str, str]:
        return self._speaker.generate_random_lines()

    def _react_to_email_message(self) -> tuple[str, str]:
        return self._speaker.react_to_email_message()

    def _generate_ai_music(self):
        # TODO: it's jsut a mock for now

        filenames = [
            "musicgen_1.wav",
            "musicgen_2.wav",
        ]
        return random.choice(filenames)

    def _generate_algorithmic_music(self):
        # TODO: it's jsut a mock for now
        return "algorithm_1.wav"

    def _prepare_broadcast_for_streaming(self):
        pass

    def _get_intro(self):
        return "audio_data/samples/sample-1.mp3"

    def _get_outro(self):
        return "audio_data/samples/sample-2.mp3"

    def _compose_broadcast(self):
        logger.info("Composing broadcast...")

        logger.info("Generating speaker lines...")
        _, speaker_lines_path = self._generate_speaker_lines()
        _, speaker_reaction_to_email_path = self._react_to_email_message()

        logger.info("Generating music...")
        ai_music_path = self._generate_ai_music()
        algorithmic_music_path = self._generate_algorithmic_music()

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

        target_output_path = "broadcast_output.mp3"
        logger.info("Merging audio files and saving to %s", target_output_path)
        AudioMerger.merge_audio_files(paths_to_audio_files, target_output_path)
