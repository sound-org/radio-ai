import os
import shutil
import tempfile

from radio.src.config.music_config import AIMusicConfig
from src.music_generator.ai_generator import AIGenerator

from ..config.configs import valid_ai_generator_config


def test_ai_generator_generate_music():
    config = AIMusicConfig(valid_ai_generator_config)
    config.output_dir = tempfile.mkdtemp()
    generator = AIGenerator(config, 64)
    generator.CACHE_DIR = "../model_cache"
    assert generator is not None
    generator.generate(1)
    print(os.listdir(config.output_dir))
    assert len(os.listdir(config.output_dir)) == 1

    os.remove(os.path.join(config.output_dir, os.listdir(config.output_dir)[0]))
    os.rmdir(config.output_dir)


def test_ai_generator_get_music():
    config = AIMusicConfig(valid_ai_generator_config)
    config.output_dir = tempfile.mkdtemp()
    generator = AIGenerator(config, 64)
    generator.CACHE_DIR = "../model_cache"
    assert generator is not None
    generator.generate(2)
    print(os.listdir(config.output_dir))
    assert len(os.listdir(config.output_dir)) == 2

    music = generator.get_music()
    assert len(music) == 2

    shutil.rmtree(config.output_dir)
