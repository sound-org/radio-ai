import logging

from fastapi import APIRouter

from .content_creator_instance import reload_config

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/content-creator", tags=["content_creator"])


@router.get(path="/reload-config")
def reload_radio_config():
    reload_config()
