import logging
import os
import shutil
import time

import pyttsx3

logger = logging.getLogger(__name__)


class PyTTSx3Engine:
    """
    PyTTSx3Engine is a class that provides text-to-speech functionality using the pyttsx3 library.
    """

    def __init__(self, voice: str, rate: int, volume: float) -> None:
        self._voice: str = voice
        self._rate: int = rate
        self._volume: float = volume

    def _get_engine(self) -> pyttsx3.Engine:
        """
        Private method to get a new pyttsx3 engine instance with the specified voice, rate, and volume settings.

        Returns:
            pyttsx3.Engine: The pyttsx3 engine instance.
        """
        logger.info("Getting new pyttsx3 engine")
        logger.info("Getting pyttsx3 engine")
        engine = pyttsx3.init("espeak")
        engine.setProperty("voice", self._voice)
        engine.setProperty("rate", self._rate)
        engine.setProperty("volume", self._volume)
        return engine

    def text_to_speech(self, text: str, output_dir: str) -> str:
        """
        Converts the given text to speech and saves the resulting audio file in the specified output directory.

        Args:
            text (str): The text to convert to speech.
            output_dir (str): The directory where the audio file should be saved.

        Returns:
            str: The path to the saved audio file.
        """
        filename: str = time.strftime("%Y%m%d-%H%M%S.mp3")
        path: str = os.path.join(output_dir, filename)

        engine: pyttsx3.Engine = (
            self._get_engine()
        )  # NOTE: save_to_file never returns after second call, so we need to create a new engine every time...
        engine.save_to_file(text=text, filename=filename)
        engine.runAndWait()

        while not os.path.exists(filename):
            logger.info("Waiting for file %s to be created...", filename)
            time.sleep(2)

        logger.info("Renaming %s to %s", filename, path)
        # os.renames(
        #     filename, path
        # )
        try:
            shutil.move(
                filename, path
            )  # NOTE: a hack to save the file to correct directory, pyttsx3 don't allow (or just don't work) to save a file to a specific directory...       except Exception as e:
        except Exception as e:
            logger.error("Failed to move file: %s", e)
            raise e
        finally:
            engine.stop()
            del engine

        return path
