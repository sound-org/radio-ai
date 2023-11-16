import logging

from fastapi import APIRouter

from radio.content_creator.content_creator_instance import content_creator

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/speaker", tags=["speaker"])


@router.get(path="/lines")
def get_speaker_lines():
    lines = content_creator.channels[0]._generate_speaker_lines()
    return lines


@router.get(path="/react-to-email")
def react_to_email_message():
    lines = content_creator.channels[0]._react_to_email_message()
    return lines
