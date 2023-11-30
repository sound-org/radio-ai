import logging
import os
from pathlib import Path
from typing import List, Tuple, cast

import google.auth.transport.requests
from fastapi import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

logger: logging.Logger = logging.getLogger(__name__)


class AuthenticationService:
    def __init__(
        self, secrets_file: str, scopes: List[str], redirect_uri: str, token_file: Path
    ):
        self.token_file: Path = (
            token_file  # it's a given users token file with user specific credentials
        )
        self.scopes: List[str] = scopes

        print("cwd", os.getcwd())
        print("000000000000000000000000000000000000000000000")
        self.flow: Flow = Flow.from_client_secrets_file(
            client_secrets_file=secrets_file, scopes=scopes, redirect_uri=redirect_uri
        )

    def callback_handler(self, request: Request):
        logger.info(msg="Getting credentials from request")
        credentials = self.get_credentials_from_request(request=request)
        logger.info(msg="Saving credentials")
        self.save_credentials(credentials=credentials)

    def get_credentials(self) -> Credentials:
        logger.info("Loading credentials")
        credentials: Credentials = self._load_credentials()
        if not self._is_credentials_valid(credentials=credentials):
            self._refresh_token(credentials=credentials)
        return credentials

    def refresh_credentials(self) -> None:
        logger.info("Refreshing credentials")
        credentials: Credentials = self._load_credentials()
        if not self._is_credentials_valid(credentials=credentials):
            self._refresh_token(credentials=credentials)

    def get_auth_url(self) -> Tuple[str, str]:
        logger.info("Getting auth url for scopes: %s", self.scopes)
        auth_url = self.flow.authorization_url(prompt="consent")
        # return self.flow.authorization_url(prompt="consent")
        if auth_url is None:
            raise Exception("Failed to get auth url")
        return auth_url

    def get_credentials_from_request(self, request: Request) -> Credentials:
        logger.info("Getting credentials from request")
        authorization_response = str(request.url)
        self.flow.fetch_token(authorization_response=authorization_response)
        if self.flow.credentials is None:
            raise Exception("Failed to fetch auth token")
        credentials: Credentials = cast(Credentials, self.flow.credentials)
        return credentials

    def save_credentials(self, credentials: Credentials) -> None:
        logger.info("Saving credentials")
        # TODO: save it to the database
        with open(file=self.token_file, mode="w") as file:
            file.write(credentials.to_json())

    def _load_credentials(self) -> Credentials:
        try:
            credentials: Credentials = Credentials.from_authorized_user_file(
                filename=self.token_file
            )
        except Exception as exception:
            logger.error("Error while loading credentials: %s", exception)
            raise Exception("Failed to load credentials from file")
        return credentials

    def _refresh_token(self, credentials: Credentials) -> Credentials:
        try:
            request = google.auth.transport.requests.Request()
            credentials.refresh(request=request)
            self.save_credentials(credentials=credentials)
            return credentials

        except Exception as exception:
            logger.error("Error while refreshing token: %s", exception)
            raise exception

    def _is_credentials_valid(self, credentials: Credentials) -> bool:
        return credentials.valid and not credentials.expired
