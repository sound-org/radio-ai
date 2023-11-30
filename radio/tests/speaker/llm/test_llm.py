from src.speaker.llm.llm import LLM
from tests.conftest import RUN_EXTERNAL_API_TESTS


def test_get_random_lines():
    if not RUN_EXTERNAL_API_TESTS:
        assert False
    llm = LLM("test personality, say exacly one word")
    lines = llm.generate_speaker_lines("get next lines")
    assert isinstance(lines, str)
    assert len(lines) > 0


def test_react_to_email_message():
    if not RUN_EXTERNAL_API_TESTS:
        assert False
    llm = LLM("test personality, say exacly one word")
    lines = llm.react_to_email_message("this is random email    ")
    assert isinstance(lines, str)
    assert len(lines) > 0
