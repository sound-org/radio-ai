from src.config.channel_config import ChannelConfig
from src.music_generator.music_generator import MusicGenerator
from src.speaker.speaker import Speaker


class Channel:
    _speaker: Speaker
    _music_generator: MusicGenerator

    def __init__(self, config: ChannelConfig):
        self._speaker = Speaker(config.speaker)
        self._music_generator = MusicGenerator(config.music)

    def _generate_speaker_lines(self) -> str:
        return self._speaker.generate_random_lines()

    def _react_to_email_message(self) -> str:
        return self._speaker.react_to_email_message()

    def _generate_ai_music(self):
        return self._music_generator.generate_ai_music()

    def _generate_algorithmic_music(self):
        return self._music_generator.generate_algorithmic_music()

    def _prepare_broadcast_for_streaming(self):
        pass

    def _compose_broadcast(self):
        pass
