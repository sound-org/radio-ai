import pytest

from src.config import MusicConfig

from .configs import (
    invalid_music_config_missing_output_path_for_custom_generator,
    invalid_music_generator_unknown_type,
    valid_muisc_config_with_multiple_ai_generators,
    valid_music_config,
    valid_music_config_with_single_ai_generator,
)


def test_music_config_complete():
    music_config = MusicConfig(valid_music_config)
    assert isinstance(music_config, MusicConfig)
    assert len(music_config.ai_generators) == 1
    assert len(music_config.algorithmic_generators) == 1
    assert len(music_config.custom_generators) == 1
    assert music_config.ai_generators[0].theme == "theme1"
    assert music_config.ai_generators[0].output_dir == "channels/1/music/ai"
    assert (
        music_config.algorithmic_generators[0].output_dir
        == "channels/1/music/algorithmic"
    )
    assert music_config.custom_generators[0].output_dir == "channels/1/music/custom"


def test_music_config_incomplete_no_output_path_for_custom_generator():
    with pytest.raises(Exception) as excinfo:
        MusicConfig(invalid_music_config_missing_output_path_for_custom_generator)
    assert "Custom music configuration is incomplete" in str(excinfo.value)


def test_music_config_incomplete_unknown_type():
    with pytest.raises(Exception) as excinfo:
        MusicConfig(invalid_music_generator_unknown_type)
    assert "Unknown music generator" in str(excinfo.value)


def test_music_config_with_multiple_ai_generators():
    music_config = MusicConfig(valid_muisc_config_with_multiple_ai_generators)
    assert isinstance(music_config, MusicConfig)
    assert len(music_config.ai_generators) == 2
    assert len(music_config.algorithmic_generators) == 1
    assert len(music_config.custom_generators) == 1
    assert music_config.ai_generators[0].theme == "theme1"
    assert music_config.ai_generators[0].output_dir == "channels/1/music/ai"
    assert music_config.ai_generators[1].theme == "theme2"
    assert music_config.ai_generators[1].output_dir == "channels/1/music/ai"
    assert (
        music_config.algorithmic_generators[0].output_dir
        == "channels/1/music/algorithmic"
    )
    assert music_config.custom_generators[0].output_dir == "channels/1/music/custom"


def test_music_config_with_single_ai_generator():
    music_config = MusicConfig(valid_music_config_with_single_ai_generator)
    assert isinstance(music_config, MusicConfig)
    assert len(music_config.ai_generators) == 1
    assert music_config.ai_generators[0].theme == "theme1"
    assert music_config.ai_generators[0].output_dir == "channels/1/music/ai"
    assert music_config.algorithmic_generators == []
    assert music_config.custom_generators == []
