from radio.config.music_config import MusicConfig

from .ai_generator import AIGenerator
from .algorithmic_generator import AlgorithmicGenerator
from .custom_generator import CustomGenerator


class MusicGenerator:
    def __init__(self, config: MusicConfig):
        self.ai_generators = []
        for ai_config in config.ai_generators:
            self.ai_generators.append(AIGenerator(ai_config))

        self.algorithmic_generators = []
        for algorithmic_config in config.algorithmic_generators:
            self.algorithmic_generators.append(AlgorithmicGenerator(algorithmic_config))

        self.custom_generators = []
        for custom_config in config.custom_generators:
            self.custom_generators.append(CustomGenerator(custom_config))

    def generate_ai_music(self):
        pass

    def generate_algorithmic_music(self):
        pass

    def get_music(self, n: int):
        pass
