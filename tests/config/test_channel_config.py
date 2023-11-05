import pytest

from src.config import ChannelConfig, SpeakerConfig

from .configs import incomplete_channel_config, valid_channel_config


def test_channel_config_complete():
    channel_config = ChannelConfig(valid_channel_config)
    assert channel_config.id == 1
    assert channel_config.name == "Channel1"
    assert channel_config.description == "This is channel 1"
    assert channel_config.broadcast_output_dir == "broadcast_output_dir"
    assert channel_config.streaming_output_dir == "streaming_output_dir"
    assert isinstance(channel_config.speaker, SpeakerConfig)


def test_channel_config_incomplete():
    with pytest.raises(Exception) as excinfo:
        ChannelConfig(incomplete_channel_config)
    assert "Channel configuration is incomplete" in str(excinfo.value)
