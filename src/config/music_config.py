from typing import Dict


class MusicConfig:
    def __init__(self, speaker_config: Dict[str, str]) -> None:
        self.theme = speaker_config.get("theme")
        self.output_dir = speaker_config.get("output_dir")
        if not all([self.theme, self.output_dir]):
            raise Exception("Speaker configuration is incomplete")
