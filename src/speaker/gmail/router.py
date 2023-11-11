import logging
from typing import Tuple

from fastapi import APIRouter, Request, Response, status

from .authenticaion_service import AuthenticationService
from .gmail_config import GmailConfig
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


@router.get(path="/latest-message")
def get_latest_mesage(response: Response):
    logger.info("Getting latest message from gmail")
    gmail_integration = GmailService()
    gmail_message: str = gmail_integration.get_latest_message()

    logger.info("Successfully returned latest message from gmail")
    return gmail_message
