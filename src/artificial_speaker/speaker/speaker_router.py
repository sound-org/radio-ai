import logging
from typing import List

from fastapi import APIRouter, Response
from gmail import GmailMessageSchema, GmailService
from gmail import converter as gmail_converter
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.schema import BaseMessage, HumanMessage, SystemMessage

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/speaker", tags=["speaker"])
history: List[BaseMessage] = []
dj_character = SystemMessage(
    content="Hello, I am a DJ speaker. I am a little bit crazyyy. I talk about music, about my life, about my friends. And everything else that comes to my mind."
)
initial_message = SystemMessage(content="Starting talking")
history.append(dj_character)
history.append(initial_message)


# at localost:8000/docs you can find swagger documentation
def get_llm():
    chat = ChatOpenAI()
    message = HumanMessage(content="continue")
    history.append(message)
    response = chat(history)
    history.append(response)
    return response


@router.get("/speaker/lines")
def get_speaker_lines():
    dj_message = get_llm()
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
