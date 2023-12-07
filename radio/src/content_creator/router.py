import logging

from fastapi import APIRouter

from src.content_creator.content_creator_instance import content_creator

from .content_creator_instance import reload_config

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/content-creator", tags=["content_creator"])


@router.get(path="/reload-config")
def reload_radio_config():
    """
    Reloads the radio configuration.
    """
    reload_config()


@router.get(path="/create-broadcast")
def create_broadcast():
    """
    Creates a broadcast for each channel in the content_creator's channels list.

    Returns:
        str: A string indicating the status of the operation ("OK").
    """
    logger.info("Create broadcast endpoint called")
    for channel in content_creator.channels:
        if channel._speaker._tts.get_TTS_driver_name() == "elevenlabs":
            continue
        channel.create_broadcast()
    return "OK"
