import logging
from typing import List

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from langchain.docstore.document import Document

from .gmail_message_parser import GmailMessageParser

SCOPES: List[str] = ["https://www.googleapis.com/auth/gmail.readonly"]

logger = logging.getLogger(__name__)


class GmailReader:
    def __init__(
        self,
        query: str,
        credentials: Credentials,
        service=None,
    ):
        self.query: str = query
        self.credentials = credentials
        self.service = service
        self.gmail_message_parser = GmailMessageParser()

    def load_data(self) -> List[Document]:
        """Load emails from the user's account"""

        if not self.service:
            self.service = build("gmail", "v1", credentials=self.credentials)

        messsages: List[Document] = self.__search_messages()

        return messsages

    def get_message(self, msg_id: str) -> Document:
        """Get a Message with given ID."""
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

    def __search_messages(self) -> List[Document]:
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
