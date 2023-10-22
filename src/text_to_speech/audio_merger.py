from moviepy.editor import AudioFileClip, concatenate_audioclips


class AudioMerger:
    @staticmethod
    def merge_audio_files(filenames: list, target_filename: str) -> None:
        print(target_filename)
        final = concatenate_audioclips(clips=[AudioFileClip(c) for c in filenames])
        final.write_audiofile(target_filename)
        final.write_audiofile(target_filename)
