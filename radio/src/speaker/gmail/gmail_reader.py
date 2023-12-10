import logging
from typing import List

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from langchain.docstore.document import Document

from .gmail_message_parser import GmailMessageParser

logger = logging.getLogger(__name__)


class GmailReader:
    """
    GmailReader class for loading and interacting with Gmail messages.

    Args:
        query (str): The query string used to filter the emails.
        credentials (Credentials): The credentials used to authenticate the Gmail API.

    """

    def __init__(
        self,
        query: str,
        credentials: Credentials,
    ):
        self.query: str = query
        self.credentials = credentials
        self.gmail_message_parser = GmailMessageParser()
        self.service = None

    def load_data(self) -> List[Document]:
        """Load emails from the user's account.

        Returns:
            List[Document]: A list of Document objects representing the loaded emails.
        """
        if not self.service:
            self.service = build("gmail", "v1", credentials=self.credentials)

        messsages: List[Document] = self._search_messages()

        return messsages

    def get_message(self, msg_id: str) -> Document:
        """Get a Message with given ID.

        Args:
            msg_id (str): The ID of the message to retrieve.

        Returns:
            Document: The Document object representing the retrieved message.
        """
        try:
            if not self.service:
                self.service = build("gmail", "v1", credentials=self.credentials)
            message = (
                self.service.users().messages().get(userId="me", id=msg_id).execute()
            )
            document = self.gmail_message_parser.parse_message(message=message)
            document.metadata["message_id"] = msg_id

            return document
        except Exception as error:
            logger.error(msg=f"An error occurred: {error}")
            raise error

    def move_to_bin(self, msg_id: str) -> None:
        """Move a Message with given ID to the bin.

        Args:
            msg_id (str): The ID of the message to move to the bin.
        """
        try:
            if not self.service:
                self.service = build("gmail", "v1", credentials=self.credentials)
            self.service.users().messages().trash(userId="me", id=msg_id).execute()
            logger.info(msg=f"Message with ID {msg_id} moved to bin.")
        except Exception as error:
            logger.error(msg=f"An error occurred: {error}")

    def _search_messages(self) -> List[Document]:
        """Search for messages based on the query.

        Returns:
            List[Document]: A list of Document objects representing the searched messages.
        """
        query = self.query

        results = self.service.users().messages().list(userId="me", q=query).execute()
        messages = results.get("messages", [])
        documents: List[Document] = []
        for message_info in messages:
            msg_id = message_info["id"]
            document = self.get_message(msg_id=msg_id)
            if document:
                documents.append(document)

        return documents
