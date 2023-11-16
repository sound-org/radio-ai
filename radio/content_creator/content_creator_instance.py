import json

from radio.config.radio_config import RadioConfig
from radio.content_creator.content_creator import ContentCreator

# TODO: come up with something better
with open("radio_config.json", "r") as f:
    data = json.load(f)


config = RadioConfig(data)
content_creator = ContentCreator(config)
