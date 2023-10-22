from moviepy.editor import AudioFileClip, concatenate_audioclips


def merge_audio_files(filenames: list, target_filename: str) -> None:
    final = concatenate_audioclips([AudioFileClip(c) for c in filenames])
    final.write_audiofile(target_filename)
