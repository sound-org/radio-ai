import json

from radio.config.radio_config import RadioConfig
from radio.content_creator.content_creator import ContentCreator


def create_content_creator() -> ContentCreator:
    with open("radio_config.json", "r") as f:
        data = json.load(f)
    config = RadioConfig(data)
    return ContentCreator(config)


content_creator: ContentCreator = create_content_creator()


def reload_config():
    global content_creator
    content_creator = create_content_creator()
