
class AudioFilenameBuilder:
    def __init__(self):
        self.parts = []

    def add(self, part: str):
        self.parts.append(part)
        return self

    def build(self) -> str:
        return "_".join(self.parts) + ".wav"

