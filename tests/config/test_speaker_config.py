import pytest

from radio.config import SpeakerConfig, TTSEnum

from .configs import incomplete_speaker_config, valid_speaker_config


def test_speaker_config_complete():
    speaker_config = SpeakerConfig(valid_speaker_config)
    assert speaker_config.name == "Speaker1"
    assert speaker_config.voice == "Voice1"
    assert speaker_config.TTS == TTSEnum.ELEVENLABS
    assert speaker_config.personality == "Friendly"
    assert speaker_config.output_dir == "output_dir"


def test_speaker_config_incomplete():
    with pytest.raises(Exception) as excinfo:
        SpeakerConfig(incomplete_speaker_config)
    assert "Speaker configuration is incomplete" in str(excinfo.value)
