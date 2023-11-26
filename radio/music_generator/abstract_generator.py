import os
import random


class AbstractMusicGenerator:
    def __init__(self, config):
        self.output_dir = config.output_dir

    def get_music(self, n: int):
        music_files = os.listdir(self.output_dir)
        sampled_files = random.sample(music_files, n)
        return sampled_files

    def generate(self, n: int):
        raise NotImplementedError
