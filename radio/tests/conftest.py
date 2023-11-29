import os

import dotenv
import pytest

result = dotenv.load_dotenv("radio/.env")
if result is False:
    cwd = os.getcwd()
    print("Current working directory: " + cwd)
    raise Exception("Failed to load .env file" + cwd)


@pytest.fixture(scope="session", autouse=True)
def change_test_dir(request):
    os.chdir(os.path.dirname("./radio/"))
    yield


RUN_EXTERNAL_API_TESTS = True
