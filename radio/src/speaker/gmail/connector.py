import logging
from typing import List

from google.oauth2.credentials import Credentials
from langchain.docstore.document import Document

from .authenticaion_service import AuthenticationService
from .gmail_config import GmailConfig
from .gmail_reader import GmailReader

logger: logging.Logger = logging.getLogger(__name__)


class GmailConnector:
    """
    A class that represents a connector to Gmail.

    This class provides methods to interact with Gmail API, such as refreshing authentication,
    retrieving the latest message from the trash, and retrieving the latest message from the inbox
    and moving it to the bin.

    """

    def __init__(self) -> None:
        self.authentication_service = AuthenticationService(
            secrets_file=GmailConfig.secrets_file,
            scopes=GmailConfig.scopes,
            redirect_uri=GmailConfig.redirect_uri,
            token_file=GmailConfig.token_path,
        )

    def refresh_authentication(self) -> None:
        """
        Refreshes the authentication credentials.
        """
        self.authentication_service.refresh_credentials()

    def get_latest_message_from_trash(self):
        """
        Retrieves the latest message from the trash.

        Returns:
            The latest message from the trash.
        """
        credentials = self.authentication_service.get_credentials()
        reader = GmailReader(query="in:trash", credentials=credentials)
        messages = reader.load_data()
        messages.sort(key=lambda m: m.metadata["date"], reverse=True)
        latest_message_id = messages[0].metadata["message_id"]
        latest_message = reader.get_message(msg_id=latest_message_id)
        return latest_message

    def get_latest_message_and_move_to_bin(self) -> Document:
        """
        Retrieves the latest message from the inbox and moves it to the bin.

        Returns:
            The latest message from the inbox.
        """
        credentials: Credentials = self.authentication_service.get_credentials()
        reader = GmailReader(query="in:inbox", credentials=credentials)
        messages: List[Document] = reader.load_data()
        if not messages:
            raise Exception("No messages found in inbox")
        messages.sort(key=lambda m: m.metadata["date"], reverse=True)
        latest_message_id = messages[0].metadata["message_id"]
        latest_message = reader.get_message(msg_id=latest_message_id)
        reader.move_to_bin(msg_id=latest_message_id)
        return latest_message
