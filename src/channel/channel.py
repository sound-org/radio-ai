from src.config.channel_config import ChannelConfig
from src.music_generator.music_generator import MusicGenerator
from src.speaker.speaker import Speaker
from src.text_to_speech.interface import TextToSpeechInterface


class Channel:
    speaker: Speaker
    music_generator: MusicGenerator
    tts: TextToSpeechInterface

    def __init__(self, config: ChannelConfig):
        self.speaker = Speaker(config.speaker)
        self.music_generator = MusicGenerator(config.music_theme)
        self.tts = TextToSpeechInterface()  # TODO: add config
