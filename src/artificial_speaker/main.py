import logging
import os

from fastapi import FastAPI
from gmail.gmail_router import router as gmail_router
from speaker.speaker_router import router as speaker_router

logger = logging.getLogger(__name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


os.environ["OPENAI_API_KEY"] = "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"
app = FastAPI()
app.include_router(gmail_router)
app.include_router(speaker_router)
