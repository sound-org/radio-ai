from typing import List

from src.config.music_config import MusicConfig

from .ai_generator import AIGenerator
from .algorithmic_generator import AlgorithmicGenerator
from .custom_generator import CustomGenerator


class MusicGenerator:
    def __init__(self, config: MusicConfig):
        self.ai_generators: List[AIGenerator] = []
        for ai_config in config.ai_generators:
            self.ai_generators.append(AIGenerator(ai_config))

        self.algorithmic_generators: List[AlgorithmicGenerator] = []
        for algorithmic_config in config.algorithmic_generators:
            self.algorithmic_generators.append(AlgorithmicGenerator(algorithmic_config))

        self.custom_generators: List[CustomGenerator] = []
        for custom_config in config.custom_generators:
            self.custom_generators.append(CustomGenerator(custom_config))

    def _generate_ai_music(self, n: int):
        for generator in self.ai_generators:
            generator.generate(n)

    def _generate_algorithmic_music(self, n: int):
        for generator in self.algorithmic_generators:
            generator.generate(n)

    def _generate_custom_music(self, n: int):
        for generator in self.custom_generators:
            generator.generate(n)

    def generate_music(self, n: int):
        self._generate_ai_music(n)
        self._generate_algorithmic_music(n)
        self._generate_custom_music(n)

    def get_music(self, n: int) -> List[str]:
        music_files = []
        for generator in self.ai_generators:
            music_files += generator.get_music(n)

        for generator in self.algorithmic_generators:
            music_files += generator.get_music(n)

        for generator in self.custom_generators:
            music_files += generator.get_music(n)

        return music_files
