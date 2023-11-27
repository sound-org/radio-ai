import logging
import os
import random
from typing import List

logger = logging.getLogger(__name__)


class AbstractMusicGenerator:
    def __init__(self, config):
        self.output_dir = config.output_dir

    def get_music(self, n: int) -> List[str]:
        logger.info("Getting %d music files...", n)
        music_files = os.listdir(self.output_dir)
        sampled_files: List[str] = random.sample(music_files, n)
        sampled_files_with_path = [
            os.path.join(self.output_dir, file) for file in sampled_files
        ]
        return sampled_files_with_path

    def generate(self, n: int):
        raise NotImplementedError
