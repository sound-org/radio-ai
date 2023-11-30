import logging

from fastapi import APIRouter

from src.content_creator.content_creator_instance import content_creator

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/music", tags=["mucic"])


@router.get(path="/music/generate")
def generate_music(n: int = 2):
    for channel in content_creator.channels:
        channel._generate_music(n)
    return "OK"
