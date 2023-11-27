from radio.config.music_config import CustomMusicConfig

from ..abstract_generator import AbstractMusicGenerator


class CustomGenerator(AbstractMusicGenerator):
    def __init__(self, config: CustomMusicConfig):
        super().__init__(config)

    def generate(self, n: int):
        raise NotImplementedError
