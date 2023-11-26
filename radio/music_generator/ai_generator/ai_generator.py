from radio.config.music_config import AIMusicConfig

from ..abstract_generator import AbstractMusicGenerator


class AIGenerator(AbstractMusicGenerator):
    def __init__(self, config: AIMusicConfig) -> None:
        super().__init__(config)
        self.theme = config.theme

    def generate(self, n: int):
        pass
