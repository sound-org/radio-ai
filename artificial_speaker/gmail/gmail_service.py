import logging
from typing import List

from langchain.docstore.document import Document

from .connector import GmailConnector

logger: logging.Logger = logging.getLogger(__name__)


class GmailService:
    def __init__(self):
        self._gmail_connector = GmailConnector()

    def get_messages(self) -> List[Document]:
        logger.info(msg="Authenticating to Gmail")
        self._refresh_authentication()

        logger.info(msg="Loading documents from Gmail")
        documents = self._load_documents()

        return documents

    def get_message_by_id(self, message_id: str) -> Document:
        logger.info("Authenticating to Gmail")
        self._refresh_authentication()
        logger.info("Getting message with id %x from Gmail", message_id)
        message: Document = self._get_message_by_id(message_id=message_id)
        if message is None:
            raise Exception("with {message_id} not found")
        return message

    def _refresh_authentication(self) -> None:
        self._gmail_connector.refresh_authentication()

    def _load_documents(self) -> List[Document]:
        return self._gmail_connector.load_messages()

    def _get_message_by_id(self, message_id: str) -> Document:
        return self._gmail_connector.get_message_by_id(message_id=message_id)
