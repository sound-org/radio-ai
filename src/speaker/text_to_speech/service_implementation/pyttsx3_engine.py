import pyttsx3


class PyTTSx3Engine:
    _engine: pyttsx3.Engine
    _text: str

    def __init__(self, voice: str, rate: int, volume: float) -> None:
        self._engine = pyttsx3.init("espeak")
        # voices = self._engine.getProperty("voices")
        # voices_names = [voice.name for voice in voices]
        self._engine.setProperty("voice", voice)
        self._engine.setProperty("rate", rate)
        self._engine.setProperty("volume", volume)

    def text_to_speech(self, text: str) -> None:
        self._text = text

    def save(self, name: str):
        if self._text is None:
            raise Exception("Tried to save TTS output without generating it first")
        self._engine.save_to_file(text=self._text, filename=name)
        self._engine.runAndWait()
