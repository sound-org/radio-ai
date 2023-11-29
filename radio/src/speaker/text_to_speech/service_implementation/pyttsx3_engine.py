import logging
import os
import shutil
import time

import pyttsx3

logger = logging.getLogger(__name__)


class PyTTSx3Engine:
    def __init__(self, voice: str, rate: int, volume: float) -> None:
        self._voice: str = voice
        self._rate: int = rate
        self._volume: float = volume

    def _get_engine(self) -> pyttsx3.Engine:
        logger.info("Getting new pyttsx3 engine")
        logger.info("Getting pyttsx3 engine")
        engine = pyttsx3.init("espeak")
        engine.setProperty("voice", self._voice)
        engine.setProperty("rate", self._rate)
        engine.setProperty("volume", self._volume)
        return engine

    def text_to_speech(self, text: str, output_dir: str) -> str:
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
        # )  # NOTE: a hack to save the file to correct directory, pyttsx3 don't allow (or just don't work) to save a file to a specific directory...
        try:
            shutil.move(filename, path)
        except Exception as e:
            logger.error("Failed to move file: %s", e)
            raise e
        finally:
            engine.stop()
            del engine

        return path
