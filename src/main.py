import logging
import logging.config
import os

import dotenv

dotenv.load_dotenv()
from fastapi import FastAPI

from src.speaker.gmail.router import router as gmail_router
from src.speaker.speaker_router import router as speaker_router

# from src.speaker.speaker_router import router as speaker_router

logging.config.fileConfig("logging.ini", disable_existing_loggers=False)
logger = logging.getLogger(__name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# at localost:8000/docs you can find swagger documentation
app = FastAPI()

app.include_router(gmail_router)
app.include_router(speaker_router)
