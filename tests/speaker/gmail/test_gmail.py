from radio.speaker import gmail
from tests.conftest import RUN_EXTERNAL_API_TESTS


def test_get_latest_message():
    if not RUN_EXTERNAL_API_TESTS:
        assert False
    gmail_instance = gmail.Gmail()
    message = gmail_instance.get_latest_message()
    assert isinstance(message, str)
    assert len(message) > 0
    assert len(message) > 0
