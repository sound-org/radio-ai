import os

import dotenv

result = dotenv.load_dotenv("../.env")
if result is False:
    cwd = os.getcwd()
    print("Current working directory: " + cwd)
    raise Exception("Failed to load .env file")

RUN_EXTERNAL_API_TESTS = True
