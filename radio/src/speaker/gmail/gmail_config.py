import os
from pathlib import Path
from typing import List

# Get the current working directory
current_dir = os.getcwd()

# List the contents of the current working directory
file_list = os.listdir(current_dir)

# Print the file list
print(file_list)


class GmailConfig:
    callbackRoute: str = "/oauth2-callback"
    secrets_file: str = "credentials.json"
    token_path: Path = Path("token_gmail.json")
    scopes: List[str] = ["https://mail.google.com/"]
    host = "localhost"
    port = "8000"
    redirect_uri: str = "http://" + host + ":" + port + "/gmail" + callbackRoute
