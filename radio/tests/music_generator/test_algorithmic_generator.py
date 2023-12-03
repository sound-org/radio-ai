import os
import shutil
import tempfile
import time

from radio.src.config.music_config import AlgorithmicMusicConfig
from src.music_generator.algorithmic_generator import AlgorithmicGenerator

from ..config.configs import valid_algorithmic_generator_config


def test_algorithmic_generator_generate_music():
    config = AlgorithmicMusicConfig(valid_algorithmic_generator_config)
    config.output_dir = tempfile.mkdtemp()
    generator = AlgorithmicGenerator(config)
    assert generator is not None
    generator.generate(1)
    print(os.listdir(config.output_dir))
    assert len(os.listdir(config.output_dir)) == 1

    os.remove(os.path.join(config.output_dir, os.listdir(config.output_dir)[0]))
    os.rmdir(config.output_dir)


def test_algorithmic_generator_get_music():
    num_tracks = 3
    config = AlgorithmicMusicConfig(valid_algorithmic_generator_config)

    config.output_dir = tempfile.mkdtemp()
    generator = AlgorithmicGenerator(config)
    assert generator is not None
    generator.generate(num_tracks)
    print(os.listdir(config.output_dir))
    time.sleep(1)
    assert len(os.listdir(config.output_dir)) == num_tracks

    music = generator.get_music()
    assert len(music) == 2

    shutil.rmtree(config.output_dir)
