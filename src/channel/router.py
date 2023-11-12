import logging

from fastapi import APIRouter

from src.content_creator.content_creator_instance import content_creator

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/channels", tags=["channel"])


@router.get(path="/prepare-broadcast")
def get_speaker_lines():
    content_creator.channels[0]._compose_broadcast()
    return "OK"
