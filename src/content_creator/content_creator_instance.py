import json

from src.config.radio_config import RadioConfig
from src.content_creator.content_creator import ContentCreator

with open("radio_config.json", "r") as f:
    data = json.load(f)


config = RadioConfig(data)
content_creator = ContentCreator(config)
