import os
import tempfile

from src.channel.channel import Channel
from src.config.channel_config import ChannelConfig

from ..config.configs import valid_channel_config
from ..conftest import RUN_EXTERNAL_API_TESTS


def test_channel_create_broadcast():
    if not RUN_EXTERNAL_API_TESTS:
        assert False, "Not running external API tests"
    config: ChannelConfig = ChannelConfig(valid_channel_config)
    config.broadcast_output_dir = tempfile.mkdtemp()
    config.streaming_output_dir = tempfile.mkdtemp()
    config.speaker.output_dir = tempfile.mkdtemp()
    config.music.algorithmic_generators[0].output_dir = tempfile.mkdtemp()

    channel = Channel(config)
    channel._get_intro = lambda: ("../audio_samples/sample-1.mp3")
    channel._get_outro = lambda: ("../audio_samples/sample-2.mp3")
    channel.create_broadcast()

    assert len(os.listdir(config.broadcast_output_dir)) == 1
    assert len(os.listdir(config.streaming_output_dir)) == 1
    stream_dir = os.listdir(config.streaming_output_dir)[0]
    stream_dir = os.path.join(config.streaming_output_dir, stream_dir)
    ts_files = [f for f in os.listdir(stream_dir) if f.endswith(".ts")]
    m3u8_files = [f for f in os.listdir(stream_dir) if f.endswith(".m3u8")]
    assert len(ts_files) > 0
    assert len(m3u8_files) == 1
