from pydub import AudioSegment

def merge_audio_files(filename1: str, filename2: str, target_filename: str, crossfade: int = 1500) -> None:
    sound1 = AudioSegment.from_mp3(filename1)
    sound2 = AudioSegment.from_mp3(filename2)

    sound = sound1.append(sound2, crossfade = crossfade)
    sound.export(target_filename, format="mp3")
