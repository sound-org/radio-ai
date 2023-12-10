import os


class TextToSpeechConfig:
    """
    Configuration class for text-to-speech settings.
    """

    audio_data_dir: str = os.path.join(os.getcwd(), "audio_data")
    samples_dir: str = os.path.join(audio_data_dir, "samples")
    generated_dir: str = os.path.join(audio_data_dir, "generated")
    sample_filename_1: str = os.path.join(samples_dir, "sample-1.mp3")
    sample_filename_2: str = os.path.join(samples_dir, "sample-2.mp3")
    generated_voice_filename: str = os.path.join(generated_dir, "text.mp3")
    output_filename: str = os.path.join(generated_dir, "out.mp3")
    broadcast_dir: str = os.path.join(generated_dir, "broadcast")
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
    voice: str = "english"
    """Available voices: https://pyttsx3.readthedocs.io/en/latest/engine.html#pyttsx3.voice.Voice"""
    """['afrikaans', 'aragonese', 'bulgarian', 'bengali', 'bosnian', 'catalan', 'czech', 'welsh',
    'danish', 'german', 'greek', 'default', 'english', 'en-scottish', 'english-north', 'english_rp',
    'english_wmids', 'english-us', 'en-westindies', 'esperanto', 'spanish', 'spanish-latin-am', 'estonian',
    'basque-test', 'Persian+English-UK', 'Persian+English-US', 'persian-pinglish', 'finnish', 'french-Belgium',
    'french', 'irish-gaeilge', 'greek-ancient', 'gujarati-test', 'hindi', 'croatian', 'hungarian', 'armenian',
    'armenian-west', 'interlingua', 'indonesian', 'icelandic', 'italian', 'lojban', 'georgian', 'kannada', 'kurdish',
    'latin', 'lingua_franca_nova', 'lithuanian', 'latvian', 'macedonian', 'malayalam', 'malay', 'nepali', 'dutch',
    'norwegian', 'punjabi', 'polish', 'brazil', 'portugal', 'romanian', 'russian', 'slovak', 'albanian', 'serbian',
    'swedish', 'swahili-test', 'tamil', 'telugu-test', 'turkish', 'vietnam', 'vietnam_hue', 'vietnam_sgn', 'Mandarin', 'cantonese']"""
    rate: int = 180
    volume: float = 1.0
    elevenlabs_voice_id: str = "TX3LPaxmHKxFdv7VOQHJ"
