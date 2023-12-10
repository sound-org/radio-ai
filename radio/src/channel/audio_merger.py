from typing import List

from moviepy.editor import AudioFileClip, concatenate_audioclips


class AudioMerger:
    """
    A utility class for merging audio files.
    """

    @staticmethod
    def merge_audio_files(filenames: List[str], target_file: str) -> None:
        """
        Merges the given audio files into a single file.

        Args:
            filenames (List[str]): List of filenames of the audio files to be merged.
            target_file (str): Filename of the target file to save the merged audio.

        Returns:
            None
        """
        final = concatenate_audioclips(clips=[AudioFileClip(c) for c in filenames])
        final.write_audiofile(target_file)
