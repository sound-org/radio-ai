import os


class TextToSpeechConfig:
    audio_data_dir = os.path.join(os.getcwd(), "audio_data")
    samples_dir = os.path.join(audio_data_dir, "samples")
    generated_dir = os.path.join(audio_data_dir, "generated")
    sample_filename_1 = os.path.join(samples_dir, "sample-1.mp3")
    sample_filename_2 = os.path.join(samples_dir, "sample-2.mp3")
    generated_voice_filename = os.path.join(generated_dir, "text.mp3")
    output_filename = os.path.join(generated_dir, "out.mp3")

    voice: str = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0"
    rate: int = 200
    volume: float = 1.0
