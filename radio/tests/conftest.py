import os

import dotenv

result = dotenv.load_dotenv("radio/.env")
if result is False:
    cwd = os.getcwd()
    print("Current working directory: " + cwd)
    raise Exception("Failed to load .env file" + cwd)


RUN_EXTERNAL_API_TESTS = True
