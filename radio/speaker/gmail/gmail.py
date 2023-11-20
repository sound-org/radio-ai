import logging
import re

from langchain.docstore.document import Document

from .connector import GmailConnector

logger: logging.Logger = logging.getLogger(__name__)


class Gmail:
    def __init__(self):
        self._gmail_connector = GmailConnector()

    def _refresh_authentication(self) -> None:
        self._gmail_connector.refresh_authentication()

    def _get_latest_message_and_move_to_bin(self) -> Document:
        self._refresh_authentication()

        try:
            return self._gmail_connector.get_latest_message_and_move_to_bin()
        except Exception:
            logger.info("No message found in inbox, trying trash")
            return self._gmail_connector.get_latest_message_from_trash()

    def _clean_document_text(self, doc: Document) -> Document:
        doc.page_content = re.sub(r"[\n\t\r\s]+", " ", doc.page_content)
        return doc

    def get_latest_message(self) -> str:
        message: Document = self._get_latest_message_and_move_to_bin()
        message = self._clean_document_text(message)
        message.page_content = (
            f"This email title {message.metadata.get('title', 'Unknown')}, "
            f"Sender of this email is {message.metadata.get('from','Unknown')}, "
            f"Recipient of this email is {message.metadata.get('to','Unknown')}, "
            f"This email was received on {message.metadata.get('date','Unknown')}, "
            f"This document's content: {message.page_content}"
        )

        return message.page_content