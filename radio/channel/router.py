import logging

from fastapi import APIRouter

from radio.content_creator.content_creator_instance import content_creator

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/channels", tags=["channel"])


@router.get(path="/prepare-broadcast")
def get_speaker_lines():
    for channel in content_creator.channels:
        # if channel._speaker._tts.get_TTS_driver_name() == "elevenlabs":
        #     continue
        channel.create_broadcast()
    return "OK"
