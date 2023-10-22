import pyttsx3


class TextToSpeech:
    _engine: pyttsx3.Engine

    def __init__(self, voice, rate: int, volume: float) -> None:
        self._engine = pyttsx3.init()
        if voice:
            self._engine.setProperty("voice", voice)
        self._engine.setProperty("rate", rate)
        self._engine.setProperty("volume", volume)

    def list_available_voices(self) -> None:
        voices: list = self._engine.getProperty("voices")
        for i, voice in enumerate(voices):
            print(f"{i + 1} {voice.name} [{voice.id}]")

    def text_to_speech(
        self, text: str, say: bool, save: bool = False, file_name: str = "text.mp3"
    ) -> None:
        if say:
            self._engine.say(text)
            self._engine.runAndWait()
        if save:
            print(file_name)
            # try:
            #     os.remove(file_name)
            # except Exception as e:
            #     pass
            self._engine.save_to_file(text, filename=file_name)
            self._engine.runAndWait()
