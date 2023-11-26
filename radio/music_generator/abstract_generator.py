from typing import List


class AbstractMusicGenerator(object):
    """
    Abstract class for music generator.
    """

    def __init__(self):
        pass

    def generate(self) -> None:
        """
        Generate music.
        """
        pass

    def get_music(self, n: int) -> List[str]:
        """
        Get a list of files with music.
        """
        pass
