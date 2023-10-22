import logging
import uuid
from typing import List

from fastapi import APIRouter, Response
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.schema import BaseMessage, HumanMessage, SystemMessage

from src.gmail import GmailMessageSchema, GmailService
from src.gmail import converter as gmail_converter
from src.text_to_speech import TextToSpeechService

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/speaker", tags=["speaker"])
history: List[BaseMessage] = []
dj_character = SystemMessage(
    content="Hello, I am a DJ speaker. I am a little bit crazyyy. I talk about music, about my life, about my friends. And everything else that comes to my mind."
)
initial_message = SystemMessage(content="Starting talking")
history.append(dj_character)
history.append(initial_message)

text_to_speech_service = TextToSpeechService()


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
    uid = str(uuid.uuid4())
    text_to_speech_service.prepare_audition(
        text=dj_message.content, voice_file_name=f"voice_{uid}.mp3"
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
