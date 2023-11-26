from radio.config.music_config import AIMusicConfig


class AIGenerator:
    def __init__(self, config: AIMusicConfig) -> None:
        self.config = config
        self.theme = config.theme
        self.output_dir = config.output_dir
