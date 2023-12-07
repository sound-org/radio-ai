import logging
import re

from langchain.docstore.document import Document

from .connector import GmailConnector

logger: logging.Logger = logging.getLogger(__name__)


class Gmail:
    """
    A class representing a Gmail client.

    This class provides methods to interact with Gmail API and retrieve the latest email message.

    """

    def __init__(self):
        self._gmail_connector = GmailConnector()

    def _refresh_authentication(self) -> None:
        """
        Refreshes the authentication token for the Gmail connector.
        """
        self._gmail_connector.refresh_authentication()

    def _get_latest_message_and_move_to_bin(self) -> Document:
        """
        Retrieves the latest email message and moves it to the bin.

        Returns:
            Document: The latest email message as a Document object.
        """
        self._refresh_authentication()

        try:
            return self._gmail_connector.get_latest_message_and_move_to_bin()
        except Exception:
            logger.info("No message found in inbox, trying trash")
            return self._gmail_connector.get_latest_message_from_trash()

    def _clean_document_text(self, doc: Document) -> Document:
        """
        Cleans the text content of a Document object.

        Args:
            doc (Document): The Document object to clean.

        Returns:
            Document: The cleaned Document object.
        """
        doc.page_content = re.sub(r"[\n\t\r\s]+", " ", doc.page_content)
        return doc

    def get_latest_message(self) -> str:
        """
        Retrieves the latest email message and returns its content as a string.

        Returns:
            str: The content of the latest email message.
        """
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
