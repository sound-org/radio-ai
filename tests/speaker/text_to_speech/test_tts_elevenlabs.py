from unittest.mock import MagicMock, Mock, patch

import pytest

from src.speaker.text_to_speech.config import TextToSpeechConfig  # noqa: F401
from src.speaker.text_to_speech.service_implementation.text_to_speech_elevenabs import (
    TextToSpeechElevenLabs,
)

path: str = "src.speaker.text_to_speech.service_implementation.text_to_speech_elevenabs"


@pytest.fixture
def mock_voice():
    mock = Mock()
    mock.name = "MockVoice"
    return mock


@pytest.fixture
def mock_elevenlabs_api():
    with patch(path + ".set_api_key") as mock_set_api_key, patch(
        "elevenlabs.Voice.from_id"
    ) as mock_from_id:
        # Configure the Mock object to return a fake voice when from_id is called
        fake_voice = MagicMock()
        fake_voice.name = "FakeVoiceName"
        mock_from_id.return_value = fake_voice

        # Use your real API key in testing environment or a dummy if you're only testing the logic
        mock_set_api_key.return_value = None
        yield fake_voice


@pytest.fixture
def tts_elevenlabs_instance(mock_voice):
    with patch(path + ".set_api_key") as mock_set_api_key:
        instance = TextToSpeechElevenLabs(
            output_dir="/fake/dir", voice_id="fake_voice_id"
        )
    instance._voice = mock_voice  # Set the mock voice object
    return instance


def test_initialization(tts_elevenlabs_instance, mock_voice):
    assert tts_elevenlabs_instance._output_dir == "/fake/dir"
    assert tts_elevenlabs_instance._voice == mock_voice
    assert tts_elevenlabs_instance._model == "eleven_monolingual_v1"


def test_text_to_speech(tts_elevenlabs_instance):
    with patch(path + ".generate") as mock_generate:
        tts_elevenlabs_instance.text_to_speech("test text")
        mock_generate.assert_called_once_with(
            text="test text",
            voice=tts_elevenlabs_instance._voice,
            model=tts_elevenlabs_instance._model,
        )


def test_save_without_generation(tts_elevenlabs_instance):
    with pytest.raises(Exception) as excinfo:
        tts_elevenlabs_instance.save()
    assert "Tried to save TTS output without generating it first" in str(excinfo.value)


def test_save_with_generation(tts_elevenlabs_instance):
    tts_elevenlabs_instance._generated_audio = b"fake_audio_data"
    with patch("your_module.text_to_speech_elevenlabs.save") as mock_save:
        tts_elevenlabs_instance.save()
        mock_save.assert_called_once_with(
            audio=b"fake_audio_data", filename=tts_elevenlabs_instance._output_dir
        )
    assert tts_elevenlabs_instance._generated_audio is None


def test_get_TTS_driver_name(tts_elevenlabs_instance):
    assert tts_elevenlabs_instance.get_TTS_driver_name() == "elevenlabs"


def test_get_TTS_voice_name(tts_elevenlabs_instance, mock_voice):
    assert tts_elevenlabs_instance.get_TTS_voice_name() == mock_voice.name
