import logging
import logging.config
import os

import dotenv

dotenv.load_dotenv()
from fastapi import FastAPI

from src.content_creator.router import router as content_creator_router
from src.music_generator.router import router as music_router
from src.speaker.gmail.router import router as gmail_router
from src.speaker.speaker_router import router as speaker_router

logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


# at localost:8000/docs you can find swagger documentation
app = FastAPI()

app.include_router(gmail_router)
app.include_router(speaker_router)
app.include_router(music_router)
app.include_router(content_creator_router)

"""
This is the main module of the radio application.

It sets up the FastAPI application and includes various routers for different functionalities.

- gmail_router: Router for handling Gmail-related operations.
- speaker_router: Router for handling speaker-related operations.
- music_router: Router for handling music generation operations.
- content_creator_router: Router for handling content creation operations.

To access the Swagger documentation, visit "localhost:8000/docs".
"""
