import logging
from typing import List

from google.oauth2.credentials import Credentials
from langchain.docstore.document import Document

from .authenticaion_service import AuthenticationService
from .gmail_config import GmailConfig
from .gmail_reader import GmailReader

logger: logging.Logger = logging.getLogger(__name__)


class GmailConnector:
    def __init__(self) -> None:
        self.authentication_service = AuthenticationService(
            secrets_file=GmailConfig.secrets_file,
            scopes=GmailConfig.scopes,
            redirect_uri=GmailConfig.redirect_uri,
            token_file=GmailConfig.token_path,
        )

    def refresh_authentication(self) -> None:
        self.authentication_service.refresh_credentials()

    def load_messages(self, query="") -> List[Document]:
        credentials: Credentials = self.authentication_service.get_credentials()
        reader = GmailReader(query=query, credentials=credentials)

        documents: List[Document] = reader.load_data()
        if documents is None:
            logger.error("No documents were loaded")
            raise Exception("No documents were loaded")
        return documents

    def get_message_by_id(self, message_id: str, query="") -> Document:
        credentials: Credentials = self.authentication_service.get_credentials()
        reader = GmailReader(query=query, credentials=credentials)
        message: Document = reader.get_message(msg_id=message_id)
        if message is None:
            raise Exception("Message not found")
        return message
