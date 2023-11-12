from unittest.mock import MagicMock

import pytest

from src.speaker.text_to_speech.config import TextToSpeechConfig
from src.speaker.text_to_speech.service_implementation.text_to_speech_elevenlabs import (
    TextToSpeechElevenLabs,
)


# TODO: add REAL check, not some mocks, be we need to call the API
@pytest.fixture
def mock_voice_class(mocker):
    mock = mocker.patch(
        "src.speaker.text_to_speech.service_implementation.text_to_speech_elevenlabs.Voice"
    )
    mock.from_id.return_value = MagicMock(name="MockVoice", id="TX3LPaxmHKxFdv7VOQHJ")
    return mock


@pytest.fixture
def mock_set_api_key(mocker):
    return mocker.patch(
        "src.speaker.text_to_speech.service_implementation.text_to_speech_elevenlabs.set_api_key"
    )


@pytest.fixture
def mock_generate(mocker):
    return mocker.patch(
        "src.speaker.text_to_speech.service_implementation.text_to_speech_elevenlabs.generate"
    )


@pytest.fixture
def mock_save(mocker):
    return mocker.patch(
        "src.speaker.text_to_speech.service_implementation.text_to_speech_elevenlabs.save"
    )


def test_initialization(mock_set_api_key, mock_voice_class):
    tts = TextToSpeechElevenLabs(
        output_dir="/path/to/output", voice_id="TX3LPaxmHKxFdv7VOQHJ"
    )
    mock_set_api_key.assert_called_once_with(
        api_key=TextToSpeechConfig.elevenlabs_api_key
    )
    mock_voice_class.from_id.assert_called_once_with("TX3LPaxmHKxFdv7VOQHJ")
    assert tts._model == "eleven_monolingual_v1"
    assert tts._output_dir == "/path/to/output"


def test_text_to_speech(mock_generate, mock_voice_class):
    tts = TextToSpeechElevenLabs(output_dir="/path/to/output")
    text = "Hello world"
    tts._text_to_speech(text=text)
    mock_generate.assert_called_once_with(
        text=text, voice=mock_voice_class.from_id(), model=tts._model
    )


def test_save_no_audio_generated(mock_save):
    tts = TextToSpeechElevenLabs(output_dir="/path/to/output")
    with pytest.raises(Exception) as excinfo:
        tts._save()
    assert "Tried to save TTS output without generating it first" in str(excinfo.value)


def test_save_audio_generated_and_saved(mock_generate, mock_save, mock_voice_class):
    tts = TextToSpeechElevenLabs(output_dir="/path/to/output")
    tts._text_to_speech(text="Hello world")
    tts._save()
    mock_save.assert_called_once()  # Arguments are not checked here, would need to assert with actual bytes or mock return
    assert tts._generated_audio is None


def test_get_TTS_driver_name(mock_voice_class):
    tts = TextToSpeechElevenLabs(output_dir="/path/to/output")
    assert tts.get_TTS_driver_name() == "elevenlabs"


def test_get_TTS_voice_name(mock_voice_class):
    tts = TextToSpeechElevenLabs(output_dir="/path/to/output")
    print("voice")
    print(tts.get_TTS_voice_name())
    assert tts.get_TTS_voice_name() == mock_voice_class.from_id().name
