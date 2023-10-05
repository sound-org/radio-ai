from text_to_speech import TextToSpeech
from audio_merger import merge_audio_files

prompt: str = """
    Ladies and gentlemen, welcome to the AI radio station, 
    your go-to destination for the latest updates, great music, 
    and all-around good vibes! I'm your host today and we've 
    got something special lined up for you today. Stay tuned!
"""

if __name__ == '__main__':
    tts = TextToSpeech('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0', 200, 1.0)
    # tts.list_available_voices()

    tts.text_to_speech(prompt, False, True)
    # merge_audio_files('C:/Users/jakub/Desktop/Studia/thesis/radio-ai/sample-1.mp3', 
    #                   'C:/Users/jakub/Desktop/Studia/thesis/radio-ai/output.mp3', 
    #                   'out.mp3')
   