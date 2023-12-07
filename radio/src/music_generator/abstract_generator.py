import logging
import os
import random
from typing import List

logger = logging.getLogger(__name__)


class AbstractMusicGenerator:
    def __init__(self, config):
        """
        Initializes the AbstractGenerator class.

        Args:
            config (Config): The configuration object containing the generator settings.
        """
        self.output_dir = config.output_dir
        self.num_tracks_to_combine = config.num_tracks_to_combine

    def get_music(self) -> List[str]:
        """
        Retrieves a list of music files to be used for generating music.

        Returns:
            A list of file paths to the sampled music files.
        """
        logger.info("Getting %d music files...", self.num_tracks_to_combine)
        music_files = os.listdir(self.output_dir)
        if len(music_files) < self.num_tracks_to_combine:
            sampled_files = music_files
        else:
            sampled_files = random.sample(music_files, self.num_tracks_to_combine)
        sampled_files_with_path = [
            os.path.join(self.output_dir, file) for file in sampled_files
        ]
        return sampled_files_with_path

    def generate(self, n: int):
        raise NotImplementedError
