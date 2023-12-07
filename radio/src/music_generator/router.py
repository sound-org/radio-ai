import logging

from fastapi import APIRouter

from src.content_creator.content_creator_instance import content_creator

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/music", tags=["mucic"])


@router.get(path="/music/generate")
def generate_music(n: int = 2):
    """
    Generate music for all channels.

    Args:
        n (int): Number of music pieces to generate for each channel.

    Returns:
        str: A string indicating the success of the operation.
    """
    logger.info("Generate music endpoint called")
    for channel in content_creator.channels:
        channel._generate_music(n)
    return "OK"


@router.get(path="/music/generate/{channel}")
def generate_music_for_channel(n: int = 2, channel: int = 0):
    """
    Generate music for a specific channel.

    Args:
        n (int): The number of music pieces to generate.
        channel (int): The channel number.

    Returns:
        str: A string indicating the status of the operation.
    """
    logger.info("Generate music endpoint called")
    content_creator.channels[channel]._generate_music(n)
    return "OK"
