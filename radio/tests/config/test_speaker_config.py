import pytest

from src.config import SpeakerConfig, TTSEnum

from .configs import incomplete_speaker_config, valid_speaker_config


def test_speaker_config_complete():
    speaker_config = SpeakerConfig(valid_speaker_config)
    assert speaker_config.name == "Bob"
    assert speaker_config.voice == "english"
    assert speaker_config.TTS == TTSEnum.PYTTSX3
    assert (
        speaker_config.personality
        == "You are and radio DJ, you love good hard rock music, the harder the better music, you are definitely crazy"
    )
    assert speaker_config.output_dir == "channels/test/speaker"


def test_speaker_config_incomplete():
    with pytest.raises(Exception) as excinfo:
        SpeakerConfig(incomplete_speaker_config)
    assert "Speaker configuration is incomplete" in str(excinfo.value)
