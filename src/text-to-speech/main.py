import os

from audio_merger import merge_audio_files
from text_to_speech import TextToSpeech

audio_data_dir = os.path.join(os.getcwd(), "audio_data")
samples_dir = os.path.join(audio_data_dir, "samples")
generated_dir = os.path.join(audio_data_dir, "generated")
sample_filename_1 = os.path.join(samples_dir, "sample-1.mp3")
sample_filename_2 = os.path.join(samples_dir, "sample-2.mp3")
generated_voice_filename = os.path.join(generated_dir, "text.mp3")
output_filename = os.path.join(generated_dir, "out.mp3")

prompt = "Ladies and gentlemen, welcome to the our radio station, \
your go-to destination for the latest updates, great music, and \
all-around good vibes! I'm your host today and we've got \
something special lined up for you today. Stay tuned!"

if __name__ == "__main__":
    tts = TextToSpeech(
        "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0",
        200,
        1.0,
    )
    # tts.list_available_voices()

    tts.text_to_speech(prompt, say=False, save=True, file_name=generated_voice_filename)

    merge_audio_files(
        [
            sample_filename_1,
            generated_voice_filename,
            sample_filename_2,
        ],
        output_filename,
    )
