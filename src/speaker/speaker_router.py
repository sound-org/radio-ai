import logging
from pathlib import Path
from typing import List

from fastapi import APIRouter, Response
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.schema import BaseMessage, HumanMessage, SystemMessage

from src.gmail import GmailMessageSchema, GmailService
from src.gmail import converter as gmail_converter
from src.radio_broadcast import RadioBroadcastService

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/speaker", tags=["speaker"])
history: List[BaseMessage] = []
dj_character = SystemMessage(
    content="Hello, I am a DJ speaker. I am a little bit crazyyy. I talk about music, about my life, about my friends. And everything else that comes to my mind. Don't make your speech too long, at most 3 sentences"
)
initial_message = SystemMessage(content="Starting talking")
history.append(dj_character)
history.append(initial_message)

radio_broadcast_service = RadioBroadcastService()


def get_next_speaker_line():
    chat = ChatOpenAI()
    message = HumanMessage(content="continue")
    history.append(message)
    response = chat(history)
    history.append(response)
    return response


@router.get(path="/speaker/line")
def get_speaker_lines() -> str:
    dj_message: BaseMessage = get_next_speaker_line()
    logger.info("Generating voice for message %s", dj_message.content)
    path_to_broadcast: Path = radio_broadcast_service.create_broadcast(
        speaker_text=dj_message.content,
        music_files=["algorithms/musicgen_out3.wav"],
    )
    logger.info(
        "Successfully generated voice for message %s in dir %s",
        dj_message.content,
        path_to_broadcast,
    )
    return dj_message.content


@router.get(
    path="/{message_id}",
    description="",
    status_code=200,
    response_model=GmailMessageSchema,
)
def get_message(response: Response, message_id: str) -> GmailMessageSchema:
    logger.info("Getting message from gmail with id %s", message_id)
    gmail_integration = GmailService()
    gmail_message: Document = gmail_integration.get_message_by_id(message_id=message_id)
    gmail_message_schema: GmailMessageSchema = (
        gmail_converter.convert_gmail_message_model_to_schema(
            gmail_message=gmail_message
        )
    )
    logger.info("Successfully returned message from gmail with id %s", message_id)
    return gmail_message_schema
