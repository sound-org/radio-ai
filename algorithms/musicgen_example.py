# https://huggingface.co/facebook/musicgen-small
# https://huggingface.co/spaces/facebook/MusicGen/tree/main
print("safsad")

import time

start_whole_script = time.time()
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# os.environ["TORCH_CUDA_ARCH_LIST"] = "Turing"
import torch

print(torch.version.cuda)
print(os.environ.get("CUDA_VISIBLE_DEVICES", "Variable not set"))
print(torch.cuda.is_available())
from transformers import AutoProcessor, MusicgenForConditionalGeneration

decive = torch.device("cuda")
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
model.to(decive)

inputs = processor(
    text=[
        "80s pop track with bassy drums and synth",
        # "30s jazz track with piano and saxophone",
    ],
    padding=True,
    return_tensors="pt",
)
# model.generation_config.max_length = (
#     512 * 1  # define sample time (1 second ~= 51, so 512 = 10 seconds)
# )
model.generation_config.max_new_tokens = 512 * 5  # define sample time
# calcualte time


start_time_generatoin = time.time()
print("start time: ", start_time_generatoin)
audio_values = model.generate(**inputs)
end_time_generation = time.time()
print("generatoin time: ", end_time_generation - start_time_generatoin)

import scipy

sampling_rate = model.config.audio_encoder.sampling_rate
scipy.io.wavfile.write(
    "musicgen_out3.wav", rate=sampling_rate, data=audio_values[0, 0].numpy()
)

end_whole_script = time.time()
print("Whole script time: ", end_whole_script - start_whole_script)
