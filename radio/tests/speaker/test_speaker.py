import os
import tempfile

from src.config.speaker_config import SpeakerConfig
from src.speaker.speaker import Speaker
from tests.conftest import RUN_EXTERNAL_API_TESTS

speaker_config_json = {
    "name": "speaker1",
    "TTS": "PYTTSX3",
    "voice": "english",
    "personality": "personality1",
    "output_dir": "output_dir1",
}


def test_generate_random_lines():
    if not RUN_EXTERNAL_API_TESTS:
        assert False, "Not running external API tests"
    tmp_dir = tempfile.mkdtemp()
    assert os.path.exists(tmp_dir)
    speaker_config_json["output_dir"] = tmp_dir

    speaker_config = SpeakerConfig(speaker_config_json)
    speaker = Speaker(speaker_config)
    (lines, path) = speaker.generate_random_lines()
    assert isinstance(lines, str)
    assert len(lines) > 0
    assert isinstance(path, str)
    assert len(path) > 0
    assert os.path.exists(path)
    assert path.endswith(".mp3")
    assert os.path.getsize(path) > 0
