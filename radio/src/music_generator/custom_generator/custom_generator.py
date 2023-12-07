from src.config.music_config import CustomMusicConfig

from ..abstract_generator import AbstractMusicGenerator


class CustomGenerator(AbstractMusicGenerator):
    """
    A custom music generator that extends the AbstractMusicGenerator class.

    Args:
        config (CustomMusicConfig): The configuration object for the custom generator.
    """

    def __init__(self, config: CustomMusicConfig):
        # Initialize the custom generator
        pass
        super().__init__(config)

    def generate(self, n: int):
        """
        Is not implemented, since custom music doesnt need to be generated.
        It can only be retrieved, if it exists.

        Raises:
            NotImplementedError: This method is not implemented in the base class.
        """
        raise NotImplementedError
