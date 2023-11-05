import os

import pytest

from src.speaker.text_to_speech.service_implementation.text_to_speech_pyttsx3 import (
    TextToSpeechPyttsx3,
)


# Define a fixture for the TTS instance
@pytest.fixture
def tts_instance(tmp_path):
    # Using tmp_path fixture provided by pytest to handle temporary directory
    return TextToSpeechPyttsx3(output_dir=str(tmp_path))


def test_initialization(tts_instance):
    assert tts_instance is not None
    assert tts_instance.get_TTS_driver_name() == "pyttsx3"
    assert isinstance(tts_instance.get_TTS_voice_name(), str)


def test_save(tts_instance, tmp_path):
    # TODO: For some reason file is not creasted
    tts_instance.text_to_speech("Hello world")
    tts_instance.save()
    # Check if the file was created
    files_in_directory = os.listdir(tmp_path)
    assert len(files_in_directory) > 0


def test_get_TTS_driver_name(tts_instance):
    assert tts_instance.get_TTS_driver_name() == "pyttsx3"


def test_get_TTS_voice_name(tts_instance):
    assert isinstance(tts_instance.get_TTS_voice_name(), str)
