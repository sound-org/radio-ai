import logging
from typing import Dict, List

from src.data_storage.create_dir_if_not_exist import create_dir_if_not_exists

logger = logging.getLogger(__name__)


class AIMusicConfig:
    """
    Configuration class for AI music generation.

    Args:
        generator_config (Dict[str, str]): A dictionary containing generator configuration parameters.

    Attributes:
        output_dir (str): The output directory for the generated music.
        num_tracks_to_combine (str): The number of tracks to combine.

    Raises:
        Exception: If the algorithmic music configuration is incomplete.
    """

    def __init__(self, generator_config: Dict[str, str]) -> None:
        self.theme = generator_config.get("theme")
        self.num_tracks_to_combine = generator_config.get("num_tracks_to_combine")
        self.output_dir = generator_config.get("output_dir")
        if not all([self.theme, self.output_dir, self.num_tracks_to_combine]):
            logger.error("Failed to create AI music config")
            raise Exception("AI music configuration is incomplete")
        create_dir_if_not_exists(self.output_dir)


class AlgorithmicMusicConfig:
    """
    Configuration class for algorithmic music generation.

    Args:
        generator_config (Dict[str, str]): A dictionary containing generator configuration parameters.

    Attributes:
        output_dir (str): The output directory for the generated music.
        num_tracks_to_combine (str): The number of tracks to combine.

    Raises:
        Exception: If the algorithmic music configuration is incomplete.
    """

    def __init__(self, generator_config: Dict[str, str]) -> None:
        self.output_dir = generator_config.get("output_dir")
        self.num_tracks_to_combine = generator_config.get("num_tracks_to_combine")
        if not all([self.output_dir, self.num_tracks_to_combine]):
            logger.error("Failed to create algorithmic music config")
            raise Exception("Algorithmic music configuration is incomplete")
        create_dir_if_not_exists(self.output_dir)


class CustomMusicConfig:
    """
    Represents the configuration for custom music generation.

    Args:
        generator_config (Dict[str, str]): A dictionary containing the generator configuration.

    Attributes:
        output_dir (str): The output directory for the generated music.
        num_tracks_to_combine (str): The number of tracks to combine.

    Raises:
        Exception: If the custom music configuration is incomplete.
    """

    def __init__(self, generator_config: Dict[str, str]) -> None:
        self.output_dir = generator_config.get("output_dir")
        self.num_tracks_to_combine = generator_config.get("num_tracks_to_combine")
        if not all([self.output_dir, self.num_tracks_to_combine]):
            logger.error("Failed to create custom music config")
            raise Exception("Custom music configuration is incomplete")
        create_dir_if_not_exists(self.output_dir)


class MusicConfig:
    """
    Represents the configuration for music generators.

    Args:
        music_config (Dict[str, str]): The configuration dictionary for music generators.

    Raises:
        Exception: If the speaker configuration is incomplete or if the music generators are not specified as a list.

    Attributes:
        ai_generators (List[AIMusicConfig]): A list of AI music generators configs.
        algorithmic_generators (List[AlgorithmicMusicConfig]): A list of algorithmic music generators configs.
        custom_generators (List[CustomMusicConfig]): A list of custom music generators configs.
    """

    def __init__(self, music_config: Dict[str, str]) -> None:
        music_generators = music_config.get("music_generators")
        if not music_generators:
            raise Exception("Speaker configuration is incomplete, no music generators")
        if not isinstance(music_generators, list):
            raise Exception("Music generators should be a list")

        self.ai_generators: List[AIMusicConfig] = []
        self.algorithmic_generators: List[AlgorithmicMusicConfig] = []
        self.custom_generators: List[CustomMusicConfig] = []
        for music_generator in music_generators:
            music_generator_type = music_generator.get("type")
            if not music_generator_type:
                raise Exception("Music generator type is not specified")

            if music_generator_type == "algorithmic":
                self.algorithmic_generators.append(
                    AlgorithmicMusicConfig(music_generator)
                )
            elif music_generator_type == "ai":
                self.ai_generators.append(AIMusicConfig(music_generator))
            elif music_generator_type == "custom":
                self.custom_generators.append(CustomMusicConfig(music_generator))
            else:
                raise Exception("Unknown music generator")
