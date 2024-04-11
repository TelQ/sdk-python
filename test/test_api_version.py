import os

import pytest
from telq import TelQTelecomAPI
from dotenv import load_dotenv

# path to the environment variables where the App Id and App Key is stored
dotenv_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".env")
)

# load the environment variables
load_dotenv(dotenv_path)

API_ID = os.environ.get("api_id", "")
API_KEY = os.environ.get("api_key", "")
BASE_URL = os.environ.get("base_url", "https://api.telqtele.com")


def test_invalid_api_version_1():
    with pytest.raises(ValueError):
        api = TelQTelecomAPI(base_url=BASE_URL, api_version="3.1")
        api.authenticate(API_ID, API_KEY)


def test_invalid_api_version_2():
    with pytest.raises(ValueError):
        api = TelQTelecomAPI(base_url=BASE_URL, api_version="v2.2")
        api.authenticate(API_ID, API_KEY)


def test_currently_supported_api_version_1():
    api = TelQTelecomAPI(base_url=BASE_URL, api_version="v2.1")
    api.authenticate(API_ID, API_KEY)
    assert True


def test_currently_supported_api_version_2():
    api = TelQTelecomAPI(base_url=BASE_URL)
    api.authenticate(API_ID, API_KEY)
    assert True
