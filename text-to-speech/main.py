import os

from audio_merger import merge_audio_files
from text_to_speech import TextToSpeech

prompt: str = "Ladies and gentlemen, welcome to the our radio station, \
your go-to destination for the latest updates, great music, and \
all-around good vibes! I'm your host today and we've got \
something special lined up for you today. Stay tuned!"

if __name__ == '__main__':
    tts = TextToSpeech('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0', 200, 1.0)
    tts.list_available_voices()

    tts.text_to_speech(prompt, say=False, save=True)

    filename_prefix = os.getcwd() + '/text-to-speech/out/'
    merge_audio_files(
        [filename_prefix + 'sample-1.mp3', filename_prefix + 'text.mp3', filename_prefix + 'sample-2.mp3'], 
        filename_prefix + 'out.mp3')
   