from pathlib import Path
from typing import List


class GmailConfig:
    """
    Configuration class for Gmail integration.
    """

    callbackRoute: str = "/oauth2-callback"
    secrets_file: str = "credentials.json"
    token_path: Path = Path("token_gmail.json")
    scopes: List[str] = ["https://mail.google.com/"]
    host = "localhost"
    port = "8000"
    redirect_uri: str = "http://" + host + ":" + port + "/gmail" + callbackRoute
