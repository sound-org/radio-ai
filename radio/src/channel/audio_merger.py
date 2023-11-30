from typing import List

from moviepy.editor import AudioFileClip, concatenate_audioclips


class AudioMerger:
    @staticmethod
    def merge_audio_files(filenames: List[str], target_file: str) -> None:
        final = concatenate_audioclips(clips=[AudioFileClip(c) for c in filenames])
        final.write_audiofile(target_file)
