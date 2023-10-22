import pyttsx3


class TextToSpeechEngine:
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

    def text_to_speech(self, text: str, say: bool, save: bool, file_name: str) -> None:
        if say:
            self._engine.say(text)
        if save:
            self._engine.save_to_file(text, filename=file_name)
        self._engine.runAndWait()
