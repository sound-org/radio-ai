import os

import pyttsx3


class TextToSpeech:
    __engine: pyttsx3.Engine

    def __init__(self, voice, rate: int, volume: float) -> None:
        self.__engine = pyttsx3.init()
        if voice:
            self.__engine.setProperty('voice', voice)
        self.__engine.setProperty('rate', rate)
        self.__engine.setProperty('volume', volume)

    def list_available_voices(self) -> None:
        voices: list = self.__engine.getProperty('voices')
        for i, voice in enumerate(voices):
            print(f'{i + 1} {voice.name} [{voice.id}]')

    def text_to_speech(self, text: str, say: bool, save: bool = False, file_name: str = "text.mp3") -> None:
            if say:
                self.__engine.say(text)
                self.__engine.runAndWait()
            if save:
                self.__engine.save_to_file(text, filename=file_name)
                self.__engine.runAndWait()
                try:
                    # Sometimes you have to switch to the extended path
                    # filename_prefix = os.getcwd() + '/text-to-speech/out/'
                    os.rename(file_name, os.getcwd() + "/out/" + file_name)
                except FileNotFoundError:
                    print("Could not change the text-to-speech file path\n")
