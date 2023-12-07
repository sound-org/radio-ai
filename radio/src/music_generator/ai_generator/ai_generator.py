import logging
import os
import shutil
import subprocess
import time

import scipy
from transformers import AutoProcessor, MusicgenForConditionalGeneration

from src.config.music_config import AIMusicConfig

from ..abstract_generator import AbstractMusicGenerator

logger = logging.getLogger(__name__)


class AIGenerator(AbstractMusicGenerator):
    """
    A music generator that uses AI to generate music based on a given theme.

    Args:
        config (AIMusicConfig): The configuration for the AI music generator.
        max_new_tokens (int): The maximum number of new tokens to generate.
    """

    def __init__(
        self, config: AIMusicConfig, max_new_tokens: int = 512 * 2 + 128
    ) -> None:
        super().__init__(config)
        self.theme = config.theme
        self.max_new_tokens = max_new_tokens
        self.CACHE_DIR = "model_cache"

    def generate(self, n: int):
        """
        Generate music based on the given theme.

        Args:
            n (int): The number of songs to generate.

        """
        # Check if the cache directory exists, if not, create it
        if not os.path.exists(self.CACHE_DIR):
            os.makedirs(self.CACHE_DIR)
        logger.info("Loading model for music generation for theme %s", self.theme)
        # Check if the model files exist in the cache directory, if not, download them
        if not os.path.exists(os.path.join(self.CACHE_DIR, "processor")):
            logger.info("Model not found, downloading")
            processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
            processor.save_pretrained(os.path.join(self.CACHE_DIR, "processor"))
        else:
            processor = AutoProcessor.from_pretrained(
                os.path.join(self.CACHE_DIR, "processor")
            )

        if not os.path.exists(os.path.join(self.CACHE_DIR, "model")):
            logger.info("Model not found, downloading")
            model = MusicgenForConditionalGeneration.from_pretrained(
                "facebook/musicgen-small"
            )
            model.save_pretrained(os.path.join(self.CACHE_DIR, "model"))
        else:
            model = MusicgenForConditionalGeneration.from_pretrained(
                os.path.join(self.CACHE_DIR, "model")
            )

        # 512 is equivalent to around 10 seconds of audio
        model.generation_config.max_new_tokens = self.max_new_tokens
        logger.info("Generating %d songs with theme %s", n, self.theme)
        inputs = processor(
            text=[self.theme for _ in range(n)],
            padding=True,
            return_tensors="pt",
        )

        start_time_generation = time.time()
        audio_values = model.generate(**inputs)

        end_time_generation = time.time()

        logger.info("generation time: %s", end_time_generation - start_time_generation)
        sampling_rate = model.config.audio_encoder.sampling_rate

        for song in audio_values:
            scipy.io.wavfile.write(
                "musicgen_temp.wav", rate=sampling_rate, data=song[0].numpy()
            )
            human_readable_ts = time.strftime("%Y%m%d-%H%M%S")
            name = str(int(time.time() * 100))

            mp3_file = os.path.join(
                self.output_dir, human_readable_ts + "_" + name + ".mp3"
            )
            ffmpeg_command = "ffmpeg -i musicgen_temp.wav musicgen_temp.mp3"
            subprocess.run(
                args=ffmpeg_command,
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            logger.info(
                "Moving generated song from %s to %s", "musicgen_temp.mp3", mp3_file
            )
            while not os.path.exists("musicgen_temp.mp3"):
                logger.info("Waiting for file %s to be created...", "musicgen_temp")
                time.sleep(2)
            shutil.move("musicgen_temp.mp3", mp3_file)
            os.remove(path="musicgen_temp.wav")
            # os.remove(path="musicgen_temp.mp3")

        del model
        del processor
