import json
import logging

from src.config.radio_config import RadioConfig
from src.content_creator.content_creator import ContentCreator

logger = logging.getLogger(__name__)


def create_content_creator(config_path="../radio_config.json") -> ContentCreator:
    logger.info("Creating content creator with config path: " + config_path)
    with open(config_path, "r") as f:
        data = json.load(f)
    config = RadioConfig(data)
    return ContentCreator(config)


content_creator: ContentCreator = create_content_creator()


def reload_config():
    global content_creator
    content_creator = create_content_creator()
