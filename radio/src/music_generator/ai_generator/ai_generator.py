import logging
import os
import subprocess
import time

import scipy
from transformers import AutoProcessor, MusicgenForConditionalGeneration

from src.config.music_config import AIMusicConfig

from ..abstract_generator import AbstractMusicGenerator

logger = logging.getLogger(__name__)

# Define the cache directory path
CACHE_DIR = "model_cache"

# Check if the cache directory exists, if not, create it
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# Check if the model files exist in the cache directory, if not, download them
if not os.path.exists(os.path.join(CACHE_DIR, "processor")):
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    processor.save_pretrained(os.path.join(CACHE_DIR, "processor"))
else:
    processor = AutoProcessor.from_pretrained(os.path.join(CACHE_DIR, "processor"))

if not os.path.exists(os.path.join(CACHE_DIR, "model")):
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
    model.save_pretrained(os.path.join(CACHE_DIR, "model"))
else:
    model = MusicgenForConditionalGeneration.from_pretrained(
        os.path.join(CACHE_DIR, "model")
    )

# 512 is equivalent to around 10 seconds of audio
model.generation_config.max_new_tokens = 256 * 6 - 128  # 512 * 3 - 128


class AIGenerator(AbstractMusicGenerator):
    def __init__(self, config: AIMusicConfig) -> None:
        super().__init__(config)
        self.theme = config.theme

    def generate(self, n: int):
        logger.info("Generating %d songs with theme %s", n, self.theme)
        inputs = processor(
            text=[theme for theme in [self.theme] * n],
            padding=True,
            return_tensors="pt",
        )

        start_time_generation = time.time()
        audio_values = model.generate(**inputs)

        end_time_generation = time.time()

        print("generation time: ", end_time_generation - start_time_generation)
        sampling_rate = model.config.audio_encoder.sampling_rate

        for song in audio_values:
            scipy.io.wavfile.write(
                "musicgen_temp.wav", rate=sampling_rate, data=song[0].numpy()
            )
            name = str(int(time.time() * 100))
            mp3_file = os.path.join(self.output_dir, name + ".mp3")
            ffmpeg_command = f"ffmpeg -i musicgen_temp.wav {mp3_file}"
            subprocess.run(ffmpeg_command, shell=True, check=True)
            os.remove("musicgen_temp.wav")
