import logging
from typing import List, Tuple

from fastapi import APIRouter, Request, Response, status
from langchain.docstore.document import Document

from . import converter as gmail_converter
from .authenticaion_service import AuthenticationService
from .gmail_config import GmailConfig
from .schema import GmailMessageSchema
from .service import GmailService

router = APIRouter(prefix="/gmail", tags=["gmail"])

authentication_service = AuthenticationService(
    secrets_file=GmailConfig.secrets_file,
    scopes=GmailConfig.scopes,
    redirect_uri=GmailConfig.redirect_uri,
    token_file=GmailConfig.token_path,
)


logger = logging.getLogger(__name__)


@router.get(
    path="/auth-url",
    description="This is the first step of the OAuth2 flow. It will return the auth url.",
    status_code=status.HTTP_200_OK,
    response_model=str,
    response_description="Successfully returned auth url",
)
def get_auth_url(response: Response) -> str:
    logger.info(msg="Getting auth url for gmail integration")
    auth_url_state: Tuple[str, str] = authentication_service.get_auth_url()
    # Generate the URL for the user to be redirected to
    auth_url: str = auth_url_state[0]
    logger.info(msg="Successfully returned auth url for gmail integration")
    return auth_url


# this route has to be set in google API console as the redirect_uri:
# https://console.cloud.google.com/apis/credentials/oauthclient/1066059583397-kdr6naj9apkrvrag8807s84tr9bf6r3h.apps.googleusercontent.com?authuser=1&project=casilai-demo
# this should not be called directly, it is called by the redirect_uri
@router.get(
    path=GmailConfig.callbackRoute,
    description="This is the redirect_uri and is only called by google API. It will get and save user access token",
    status_code=status.HTTP_202_ACCEPTED,
    response_description="Successfully saved credentials",
    response_model=str,
)
def callback(request: Request, response: Response):
    logger.info("Callback route was called for gmail integration")
    authentication_service.callback_handler(request=request)
    logger.info("Callback route finished for google drive integration")
    return "Successfully saved credentials"


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


@router.get(
    path="",
    description="Ingest all messages from gmail into a vector database",
    status_code=status.HTTP_200_OK,
    response_description="List of messages successfully ingested",
    response_model=list[GmailMessageSchema],
)
def get_all_messages(response: Response) -> list[GmailMessageSchema]:
    logger.info("Ingesting messages from gmail")
    gmail_integration = GmailService()
    messages: List[Document] = gmail_integration.get_messages()
    messages_schema: List[
        GmailMessageSchema
    ] = gmail_converter.convert_gmail_messages_model_to_schema(gmail_messages=messages)

    logger.info(msg="Successfully saved data to vector store")
    return messages_schema
